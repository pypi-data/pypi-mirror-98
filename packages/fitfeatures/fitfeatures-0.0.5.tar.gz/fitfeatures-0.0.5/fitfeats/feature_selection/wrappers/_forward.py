import numpy as np

from fitfeats.feature_selection.mrmr import ForwardMRMR
from fitfeats.feature_selection.wrappers._base import BaseMRMRWrapper


class ForwardMRMRWrapper(BaseMRMRWrapper, ForwardMRMR):

    def __init__(
        self,
        estimator,
        scoring: str = None,
        association_method: str = "DCD",
    ):
        BaseMRMRWrapper.__init__(self)
        ForwardMRMR.__init__(self, association_method=association_method)

        self.scoring = scoring

        self.check_input(estimator, scoring)

        self.estimator = estimator
        self.scores = [-np.inf]
        self.ylabel = self.metrics[self.scoring]["name"]

        self.last_selected_feature = None

    def process_selected_feature(self, selected_features, selected_feature):

        self.last_selected_feature = selected_feature

        return super(ForwardMRMRWrapper, self).process_selected_feature(selected_features, selected_feature)

    def get_selected_features(self, selected_features):
        return np.delete(selected_features, np.argwhere(selected_features == self.last_selected_feature)[0][0])

    def cycle_condition(self, selected_features, i):
        return ForwardMRMR.cycle_condition(self, selected_features, i) \
            and not BaseMRMRWrapper.cycle_condition(self, selected_features, i)

    def get_x_y_axis(self, i, fitness_array):
        x = np.arange(1, i)
        y = self.scores[1:]

        return x, y

    @staticmethod
    def get_x_ticks(x):

        interval = max(x.size // 10, 1)

        return x[::interval], x[::interval]
