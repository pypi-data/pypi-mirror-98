import numpy as np

from fitfeats.feature_selection.mrmr._base import MRMRBase


class BackwardMRMR(MRMRBase):

    def __init__(
        self,
        number_features: (int, float) = None,
        association_method: str = "DCD",
    ):
        MRMRBase.__init__(self, number_features, association_method)

    def get_initial_features_fitness(self):
        selected_features = np.arange(self.features.shape[1])
        return selected_features, [self.mrmr_score(np.ones(len(selected_features)))]

    def cycle_condition(self, selected_features, i):
        return len(selected_features) > self.number_features and i <= self.features.shape[1]

    @staticmethod
    def process_selected_feature(selected_features, selected_feature):
        return np.delete(selected_features, selected_feature)

    def get_x_y_axis(self, i, fitness_array):
        x = np.flip(np.arange(self.features.shape[1] - i, self.features.shape[1] + 1))
        y = np.flip(np.array(fitness_array))

        return x, y

    @staticmethod
    def get_x_ticks(x):

        interval = max(x.size // 10, 1)

        return x[::interval], np.flip(x)[::interval]

    def get_fitness(self, selected_features):
        return np.array(
            list(
                map(
                    lambda feature: self.calculate_subset_fitness(feature, selected_features),
                    selected_features
                )
            )
        )

    def calculate_subset_fitness(self, feature, selected_features):

        chromosome = np.zeros(self.features.shape[1])
        chromosome[selected_features] = 1
        chromosome[feature] = 0

        return self.mrmr_score(chromosome)
