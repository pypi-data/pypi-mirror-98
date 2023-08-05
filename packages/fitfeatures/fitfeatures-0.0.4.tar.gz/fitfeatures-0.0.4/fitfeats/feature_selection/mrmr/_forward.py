import numpy as np

from fitfeats.feature_selection.mrmr._base import MRMRBase


class ForwardMRMR(MRMRBase):

    def __init__(
        self,
        number_features: (int, float) = None,
        association_method: str = "DCD",
    ):
        MRMRBase.__init__(self, number_features, association_method)

    def get_initial_features_fitness(self):
        return np.array([]).astype(int), []

    def cycle_condition(self, selected_features, i):
        return len(selected_features) < self.number_features and i <= self.features.shape[1]

    @staticmethod
    def process_selected_feature(selected_features, selected_feature):
        return np.append(selected_features, selected_feature)

    def get_x_y_axis(self, i, fitness_array):
        x = np.arange(i)
        y = np.array(fitness_array)

        return x, y

    @staticmethod
    def get_x_ticks(x):
        return None

    def get_fitness(self, selected_features):
        return np.array(
            list(
                map(
                    lambda feature: self.calculate_subset_fitness(feature, selected_features),
                    np.arange(self.features.shape[1])
                )
            )
        )

    def calculate_subset_fitness(self, feature, selected_features):

        if feature in selected_features:
            return 0

        chromosome = np.zeros(self.features.shape[1])
        chromosome[[*selected_features, feature]] = 1

        return self.mrmr_score(chromosome)
