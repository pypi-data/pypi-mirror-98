import numpy as np
import pandas as pd

from pipedown.nodes.base.metric import Metric
from pipedown.utils.urls import get_node_url


class MedianAbsolutePercentageError(Metric):
    CODE_URL = get_node_url("metrics/median_absolute_percentage_error.py")

    def run(self, y_pred: pd.Series, y_true: pd.Series):
        return 100 * np.nanmedian(np.abs(y_pred - y_true) / y_true)

    def get_metric_name(self):
        return "median_absolute_percentage_error"
