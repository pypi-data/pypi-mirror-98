import hashlib
from functools import reduce
from itertools import combinations

import numpy as np
import matplotlib.pyplot as plt

from fitfeats.feature_selection.association_methods import regression_association_methods
from fitfeats.base import Base


class MRMRBase(Base):

    def __init__(
        self,
        number_features: (int, float) = None,
        association_method: str = "DCD",
    ):
        Base.__init__(self)

        self.selected_features_ = None

        self.number_features = None

        self.check_input_mrmr(number_features, association_method)

        self.features = None
        self.target = None

        self.feature_comb = {}

        self.association_method = regression_association_methods[association_method]["association_method"]
        self.relation = regression_association_methods[association_method]["relation"]

        self.ylabel = "mRMR score"

    def check_input_mrmr(self, number_features, association_method):

        if isinstance(number_features, float) and 0 < number_features < 1:
            self.number_features = np.round(number_features * self.features.shape[1])
        elif isinstance(number_features, int):
            self.number_features = number_features
        elif number_features is None:
            self.number_features = None
        else:
            raise Exception(f"{number_features} is not a valid input for number_features")

        if association_method not in regression_association_methods:
            raise Exception(
                f"Invalid method, must be one of {', '.join(regression_association_methods)}."
                f" Check the documentation for more details."
            )

    def mrmr_score(self, individual):

        on_features = np.arange(self.features.shape[1])[individual == 1]

        cardinality = on_features.size

        if cardinality == 0:
            return 0

        relevance = reduce(
            lambda prev, feature: prev
            + self.calculate_relation(
                self.features[:, feature],
                self.target,
                np.array([feature, self.features.shape[1]])),
            on_features,
            0,
        )

        redundancy = reduce(
            lambda prev, case: prev
            + self.calculate_relation(
                self.features[:, case[0]],
                self.features[:, case[1]],
                np.array([case[0], case[1]])),
            combinations(on_features, 2),
            0,
        )

        try:
            if self.relation == "difference":
                return relevance / cardinality - redundancy / (cardinality ** 2)
            else:
                if redundancy == 0:
                    return 0
                return np.nan_to_num((relevance / cardinality) / (redundancy / (cardinality ** 2)))
        except ZeroDivisionError:
            return 0

    def calculate_relation(self, feature, target, hash_comb):

        arr_hash = hashlib.sha1(hash_comb).hexdigest()

        if arr_hash in self.feature_comb:
            return self.feature_comb[arr_hash]

        result = np.nan_to_num(
            self.association_method(
                feature, target
            )
        )

        self.feature_comb[arr_hash] = result

        return result

    @staticmethod
    def get_selected_features(selected_features):
        return selected_features

    def fit(self, X, y, *args):

        self.set_input_variables(X, y)

        selected_features, fitness_array = self.get_initial_features_fitness()

        if self.number_features is None:
            self.number_features = self.features.shape[1]

        i = 0
        while self.cycle_condition(selected_features, i):

            i += 1

            fitness = self.get_fitness(selected_features)

            selected_feature = np.argmax(fitness)

            selected_features = self.process_selected_feature(selected_features, selected_feature)

            fitness_array.append(fitness[selected_feature])

        self.selected_features_ = self.get_selected_features(selected_features)

        x, y = self.get_x_y_axis(i, fitness_array)

        x_ticks = self.get_x_ticks(x)

        self.plot_scores(x, y, x_ticks)

    def get_initial_features_fitness(self):
        raise NotImplementedError

    def cycle_condition(self, selected_features, i):
        raise NotImplementedError

    def get_fitness(self, selected_features):
        raise NotImplementedError

    @staticmethod
    def process_selected_feature(selected_features, selected_feature):
        raise NotImplementedError

    def get_x_y_axis(self, i, fitness_array):
        raise NotImplementedError

    @staticmethod
    def get_x_ticks(x):
        raise NotImplementedError

    def calculate_subset_fitness(self, feature, selected_features):
        raise NotImplementedError

    def plot_scores(self, x, fitness, x_ticks=None):
        """
        Plots the evolution of the mean and max fitness of the population

        :param x: array with x axis points
        :param fitness: array of fitness for each generation
        :param x_ticks: x axis ticks. Optional. Default: None
        :return: None
        """

        plt.figure(figsize=(7, 7))

        plt.plot(x, fitness, label="mRMR score")

        plt.xlabel("Number of Features")
        plt.ylabel(self.ylabel)

        if x_ticks:
            plt.xticks(*x_ticks)

        plt.show()
