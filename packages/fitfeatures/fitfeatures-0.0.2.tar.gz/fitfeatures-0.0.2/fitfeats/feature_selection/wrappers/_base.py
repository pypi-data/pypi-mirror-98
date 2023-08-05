from sklearn.model_selection import cross_val_score


class BaseMRMRWrapper:

    def __init__(self):
        self.scoring = None
        self.features = None
        self.target = None
        self.estimator = None
        self.scores = None
        self.number_features = None

    def cycle_condition(self, selected_features, i):

        feature_subset = self.features[:, selected_features]

        break_condition = False
        if feature_subset.shape[1] >= 1:

            scores_cv = cross_val_score(
                self.estimator,
                feature_subset,
                self.target,
                cv=5,
                scoring=self.scoring,
                n_jobs=-1
            )

            score = scores_cv.mean()

            if score >= self.scores[-1]:
                self.scores.append(score)
            else:
                break_condition = True

        return break_condition
