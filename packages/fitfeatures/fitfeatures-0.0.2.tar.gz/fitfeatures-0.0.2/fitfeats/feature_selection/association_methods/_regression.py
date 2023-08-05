import numpy as np

from dcor import distance_correlation, distance_covariance
from scipy.stats import pearsonr, spearmanr, kendalltau
from sklearn.feature_selection import mutual_info_regression, f_regression
from sklearn.metrics.pairwise import cosine_similarity
from pyitlib.discrete_random_variable import information_mutual


regression_association_methods = {
    "DCD": {
        "association_method": distance_correlation,
        "relation": "difference"
    },
    "DCQ": {
        "association_method": distance_correlation,
        "relation": "quotient"
    },
    "DCVD": {
        "association_method": distance_covariance,
        "relation": "difference"
    },
    "DCVQ": {
        "association_method": distance_covariance,
        "relation": "quotient"
    },
    "PCD": {
        "association_method": lambda x, y: np.abs(pearsonr(x, y)[0]),
        "relation": "difference",
    },
    "PCQ": {
        "association_method": lambda x, y: np.abs(pearsonr(x, y)[0]),
        "relation": "quotient",
    },
    "SCD": {
        "association_method": lambda x, y: np.abs(spearmanr(x, y)[0]),
        "relation": "difference",
    },
    "SCQ": {
        "association_method": lambda x, y: np.abs(spearmanr(x, y)[0]),
        "relation": "quotient",
    },
    "KTD": {
        "association_method": lambda x, y: np.abs(kendalltau(x, y)[0]),
        "relation": "difference",
    },
    "KTQ": {
        "association_method": lambda x, y: np.abs(kendalltau(x, y)[0]),
        "relation": "quotient",
    },
    "CSD": {
        "association_method": lambda x, y: np.abs(cosine_similarity(x.reshape(1, -1), y.reshape(1, -1))[0]),
        "relation": "difference",
    },
    "CSQ": {
        "association_method": lambda x, y: np.abs(kendalltau(x, y)[0]),
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
    "MID": {
        "association_method": lambda x, y: mutual_info_regression(x.reshape(-1, 1), y)[0],
        "relation": "difference",
    },
    "MIQ": {
        "association_method": lambda x, y: mutual_info_regression(x.reshape(-1, 1), y)[0],
        "relation": "quotient",
    },
    "FRD": {
        "association_method": lambda x, y: f_regression(x.reshape(-1, 1), y)[0][0],
        "relation": "difference",
    },
    "FRQ": {
        "association_method": lambda x, y: f_regression(x.reshape(-1, 1), y)[0][0],
        "relation": "quotient",
    }
}
