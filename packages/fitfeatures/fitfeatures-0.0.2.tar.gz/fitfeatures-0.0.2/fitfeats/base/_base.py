from typing import Sequence

import numpy as np
from sklearn.base import is_regressor, is_classifier

from fitfeats.metrics import regression_metrics, classification_metrics
from fitfeats.utils.exceptions_messages import exception_messages


class Base:

    def __init__(self):

        self.features = None
        self.target = None
        self.columns = None
        self.columns_to_index = None
        self.feature_subset_include = None
        self.feature_subset_exclude = None
        self.allowed_mutation_genes = None
        self.metrics = None
        self.scoring = None
        self.selected_features_ = None

    def set_input_variables(
        self,
        features,
        target,
        feature_subset_include: Sequence = None,
        feature_subset_exclude: Sequence = None,
    ):
        try:
            if target.ndim != 1:
                target = target.flatten()

            if target.shape[0] != features.shape[0]:
                raise Exception(f"Invalid target variable, it must be a vector with same dimensions as features.")

            if features.ndim == 1:
                features = features.reshape(-1, 1)
        except AttributeError:
            raise Exception('Input features / target must be a numpy array')

        try:
            self.columns = features.columns
            self.columns_to_index = {column: i for i, column in enumerate(self.columns)}
        except AttributeError:
            pass

        self.features = np.array(features)
        self.target = np.array(target)

        self.check_feature_subsets(feature_subset_include, 'feature_subset_include')
        self.check_feature_subsets(feature_subset_exclude, 'feature_subset_exclude')

    def check_feature_subsets(self, feature_subset, feature_subset_type):
        if feature_subset is not None:
            if not isinstance(feature_subset, (list, tuple, np.ndarray)):
                raise Exception('feature_subset_include must be a sequence of features by column or index')

            if self.columns is None:
                for column in feature_subset:
                    if not isinstance(column, (int, np.integer)):
                        raise Exception('feature_subset_include must be a sequence of features by index')

                setattr(self, feature_subset_type, feature_subset)

                self.allowed_mutation_genes = [
                    item
                    for item in self.allowed_mutation_genes
                    if item not in feature_subset
                ]

            else:
                feature_subset_indices = []
                for column in feature_subset:
                    if not isinstance(column, (int, str, np.integer)):
                        raise Exception(exception_messages["InvalidFeatureSubset"])

                    if isinstance(column, str):
                        try:
                            column = self.columns_to_index[column]
                        except KeyError:
                            raise Exception(exception_messages["InvalidFeatureSubset"])

                    feature_subset_indices.append(column)

                setattr(self, feature_subset_type, feature_subset_indices)

                self.allowed_mutation_genes = [
                    item
                    for item in self.allowed_mutation_genes
                    if item not in feature_subset_indices
                ]

    def check_input(self, estimator, scoring):
        if is_regressor(estimator):

            self.metrics = regression_metrics

            if scoring is None:
                self.scoring = 'r2'
            elif scoring not in regression_metrics:
                raise Exception(f"The Provided scoring method is not an allowed option. "
                                f"Must be one of {', '.join(key for key in regression_metrics.keys())}.")

        elif is_classifier(estimator):

            self.metrics = classification_metrics

            if scoring is None:
                self.scoring = 'accuracy'
            elif scoring not in classification_metrics:
                raise Exception(f"The Provided scoring method is not an allowed option. "
                                f"Must be one of {', '.join(key for key in classification_metrics.keys())}.")

        else:
            raise Exception("The estimator must be a Regressor or a Classifier.")

    def fit(self, X, y, feature_subset_include, feature_subset_exclude):
        """
        Fits the data and finds the optimal subset of features.

        :param X: {array-like, sparse matrix} of shape (n_samples, n_features)
            Training data

        :param y: array-like of shape (n_samples,) or (n_samples, n_targets)

        :param feature_subset_include: List[int, string], optional. Default: None
            Feature subset to always include in the optimal feature subset.
            Can be an array of ints or strings if X is a pandas dataframe. If
            feature is in both include and exclude subsets, the include subset
            has priority.

        :param feature_subset_exclude: List[int, string], optional. Default: None
            Feature subset to always exclude from the optimal feature subset.
            Can be an array of ints or strings if X is a pandas dataframe. If
            feature is in both include and exclude subsets, the include subset
            has priority.

        :return: None
        """
        pass

    def transform(self, X):
        """
        Transforms the input data into the fitted optimal features subset.
        Errors if the data hasn't been fitted yet.

        :param X: {array-like, sparse matrix} of shape (n_samples, n_features)
            Must have the same number of columns as the fitted data.

        :return: {array-like, sparse matrix} of shape (n_samples, best_features)
            Returns the optimal feature subset of the input data.
        """

        features = self.selected_features_

        if features is None:
            raise Exception("Data must be fitted before calling this method.")

        assert X.shape[1] == self.features.shape[1], \
            "Dimensions mismatch between fitted features and provided X"

        try:
            return X[:, self.selected_features_]
        except TypeError:
            return X.loc[:, self.selected_features_]

    def fit_transform(self, X, y, feature_subset_include: Sequence = None, feature_subset_exclude: Sequence = None):
        """
        Calls the fit and transform methods in one go.

        :param X: {array-like, sparse matrix} of shape (n_samples, n_features)
            Training data

        :param y: array-like of shape (n_samples,) or (n_samples, n_targets)

        :param feature_subset_include: List[int, string], optional. Default: None
            Feature subset to always include in the optimal feature subset.
            Can be an array of ints or strings if X is a pandas dataframe. If
            feature is in both include and exclude subsets, the include subset
            has priority.

        :param feature_subset_exclude: List[int, string], optional. Default: None
            Feature subset to always exclude from the optimal feature subset.
            Can be an array of ints or strings if X is a pandas dataframe. If
            feature is in both include and exclude subsets, the include subset
            has priority.

        :return: {array-like, sparse matrix} of shape (n_samples, best_features)
            Returns the optimal feature subset of the input data.
        """

        self.fit(X, y, feature_subset_include, feature_subset_exclude)

        return self.transform(X)