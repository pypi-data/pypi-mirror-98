import numpy as np

from fitfeats.feature_selection.mrmr import BackwardMRMR
from fitfeats.feature_selection.wrappers._base import BaseMRMRWrapper


class BackwardMRMRWrapper(BaseMRMRWrapper, BackwardMRMR):

    def __init__(
        self,
        estimator,
        scoring: str = None,
        association_method: str = "DCD",
    ):
        BaseMRMRWrapper.__init__(self)
        BackwardMRMR.__init__(self, association_method=association_method)

        self.scoring = scoring

        self.check_input(estimator, scoring)

        self.estimator = estimator
        self.scores = [-np.inf]
        self.ylabel = self.metrics[self.scoring]["name"]

        self.number_features = 0
        self.last_selected_feature = None

    def process_selected_feature(self, selected_features, selected_feature):

        self.last_selected_feature = selected_features[selected_feature]

        return super(BackwardMRMRWrapper, self).process_selected_feature(selected_features, selected_feature)

    def get_selected_features(self, selected_features):
        return np.append(selected_features, self.last_selected_feature)

    def cycle_condition(self, selected_features, i):
        return BackwardMRMR.cycle_condition(self, selected_features, i) \
            and not BaseMRMRWrapper.cycle_condition(self, selected_features, i)

    def get_x_y_axis(self, i, fitness_array):
        x = np.flip(np.arange(self.features.shape[1] - i + 1, self.features.shape[1] + 1))
        y = np.flip(np.array(self.scores[1:]))

        return x, y

    @staticmethod
    def get_x_ticks(x):

        interval = max(x.size // 10, 1)

        return x[::interval], np.flip(x)[::interval]
