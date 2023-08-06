from itertools import product

import numpy as np
from numba import njit


def feature_polynomials(x, degree, intercept=False, only_self_terms=False):
    """
    Maps the original features up to the chosen degree.
    Example for initial features a and b and chosen order of 3:
    [a b a^2 ab b^2 a^3 a^2b ab^2 b^3]
    :param x: array like object of m examples by n features
    :param degree: order of the polynomial expansion mapping to perform
    :param intercept: If return array should include the intercept column
    :param only_self_terms: if should only include polynomial terms (eg: x, x2, x3, etc)
    :return: array with mapped features
    """

    X = np.array(x).copy()

    n_features = X.shape[1] if len(X.shape) > 1 else 1
    features = [i for i in range(n_features)]

    for i in range(2, degree + 1):

        if only_self_terms:

            for j in features:
                X = np.c_[X, X[:, j] ** i]

        else:
            product_cases = list(product(features, repeat=i))

            product_cases = [tuple(sorted(t)) for t in product_cases]
            product_cases = [list(comb) for comb in set(product_cases)]

            X = get_new_variables(X, np.array(product_cases))

    if intercept:
        X = np.c_[np.ones(X.shape[0]), X]

    return X


@njit
def get_new_variables(X, product_cases):

    for case in product_cases:

        columns = X[:, case].T
        columns_prod = columns[0:2, :]
        for column in columns[1:, :]:
            columns_prod = columns_prod * column

        X = np.hstack((X, columns_prod.T))[:, :-1]

    return X