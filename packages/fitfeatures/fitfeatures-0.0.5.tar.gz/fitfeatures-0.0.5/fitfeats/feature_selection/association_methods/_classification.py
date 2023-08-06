import numpy as np
from dcor import distance_correlation
from scipy.stats import pearsonr

from sklearn.feature_selection import mutual_info_classif, f_classif
from pyitlib.discrete_random_variable import information_mutual


regression_association_methods = {
    "DCD": {"association_method": distance_correlation, "relation": "difference"},
    "DCQ": {"association_method": distance_correlation, "relation": "quotient"},
    "PCD": {
        "association_method": lambda x, y: np.abs(pearsonr(x, y)[0]),
        "relation": "difference",
    },
    "PCQ": {
        "association_method": lambda x, y: np.abs(pearsonr(x, y)[0]),
        "relation": "quotient",
    },
    "MID": {
        "association_method": lambda x, y: mutual_info_classif(x.reshape(-1, 1), y)[0],
        "relation": "difference",
    },
    "MIQ": {
        "association_method": lambda x, y: mutual_info_classif(x.reshape(-1, 1), y)[0],
        "relation": "quotient",
    },
    "MD": {
        "association_method": lambda x, y: max(0, information_mutual(x, y)),
        "relation": "difference",
    },
    "MQ": {
        "association_method": lambda x, y: max(0, information_mutual(x, y)),
        "relation": "quotient",
    },
    "FRD": {
        "association_method": lambda x, y: f_classif(x.reshape(-1, 1), y)[0][0],
        "relation": "difference",
    },
    "FRQ": {
        "association_method": lambda x, y: f_classif(x.reshape(-1, 1), y)[0][0],
        "relation": "quotient",
    }
}
