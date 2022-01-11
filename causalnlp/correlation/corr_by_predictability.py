def get_scorer(task_type='regression'):
    if task_type == 'regression':
        return RegressionScorer()
    else:
        return ClassificationScorer()


class Scorer:
    def __init__(self):
        pass

    @staticmethod
    def check_significance(this_results: list, baseline_results: list, P_VALUE_THRES=0.05):
        from scipy import stats
        import numpy as np

        score, p_value = stats.ttest_ind(this_results, np.array(baseline_results), equal_var=False)
        if_sign = p_value <= P_VALUE_THRES
        return if_sign


class RegressionScorer(Scorer):
    def __init__(self):
        super().__init__()
    def get_scores(self, y_true, y_pred):
        from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_squared_log_error
        mean_absolute_error(y_true, y_pred)
    def get_adjusted_r2(self):


class ClassificationScorer(Scorer):
    def __init__(self):
        super().__init__()
