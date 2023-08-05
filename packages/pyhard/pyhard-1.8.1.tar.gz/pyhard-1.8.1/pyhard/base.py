from abc import ABC, abstractmethod
from typing import Union, Optional

import pandas as pd
import numpy as np


class BaseMeasures(ABC):
    """
    Base class for measures (aka meta-features). Each measure should be implemented as a separate method.
    """

    _measures_dict = dict()

    @property
    def logger(self):
        raise NotImplementedError

    def _call_method(self, name, **kwargs):
        return getattr(self, name)(**kwargs)

    def calculate_all(self, measures_list=None):
        if measures_list is None:
            measures_list = self._measures_dict.keys()
        elif isinstance(measures_list, list):
            measures_list = list(set(measures_list) & set(self._measures_dict.keys()))
        else:
            raise TypeError(f"Expected type list for parameter 'measures_list', not '{type(measures_list)}'")

        results = {}
        for k in measures_list:
            self.logger.info(f"Calculating measure {repr(k)}")
            results[k] = self._call_method(self._measures_dict[k])

        df_measures = pd.DataFrame(results)
        return df_measures.add_prefix('feature_')


class BaseLearner(ABC):
    """
    Base class for learners (algorithms). This class provides methods for assessing performance in a pool of learners.
    """

    @staticmethod
    def _call_function(module, name, **kwargs):
        return getattr(module, name)(**kwargs)

    @abstractmethod
    def score(self, metric: str, y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        """
        Returns an array with scores for each instance
        """
        pass

    @abstractmethod
    def estimate_ih(self) -> np.ndarray:
        """
        Estimates the Instance Hardness value.
        """
        pass

    @abstractmethod
    def run(self, algo, metric: str, n_folds: int, n_iter: int, hyper_param_optm: bool, hpo_evals: int,
            hpo_timeout: int, hpo_name: str, verbose: bool, **kwargs) -> Union[np.ndarray, np.ndarray]:
        """
        Evaluates a single learner. Should return an array with mean score per instance, and an array with mean proba
        per instance (from sklearn method `predict_proba`).
        """
        pass

    @abstractmethod
    def run_all(self, metric: str, n_folds: int, n_iter: int, algo_list: Optional[list], parameters: Optional[list],
                hyper_param_optm: bool, hpo_evals: int, hpo_timeout: int, verbose: bool) -> pd.DataFrame:
        """
        Evaluates a pool of learners. Should return a dataframe whose columns are the algorithms and rows are the
        instances. Columns names must have the prefix `algo_`.
        """
        pass
