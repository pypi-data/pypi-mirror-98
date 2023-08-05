import pandas as pd
import numpy as np


def X2y(X, with_error=True):

    # functional form of the dependence between y and X
    y_star = X['linear'] + \
             X['nonlinear_square'] ** 2 + \
             np.sin(3 * X['nonlinear_sin']) + \
             (X['interaction_1'] * X['interaction_2'] * X['interaction_3'])

    # add random error called epsilon (this will be used for creating y)
    if with_error:
        np.random.seed(0)
        epsilon = np.random.normal(0, .1, len(y_star))
        return y_star + epsilon

    else:
        return y_star


feature_names = [
    'linear',            # 1
    'nonlinear_square',  # 2
    'nonlinear_sin',     # 3
    'interaction_1',     # 4
    'interaction_2',     # 5
    'interaction_3',     # 6
    'noise_1',           # 7
    'noise_2',           # 8
    'noise_3',           # 9
    'noise_4',           # 10
    'noise_5',           # 11
    'noise_6',           # 12
    'noise_7',           # 13
    'noise_8',           # 14
    'noise_9',           # 15
    'noise_10'           # 16
]


# make X and y
np.random.seed(0)

X = pd.DataFrame(np.random.normal(size=(20_000, len(feature_names))), columns=feature_names)
y = X2y(X, with_error=True)
