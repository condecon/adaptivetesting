from typing import List
import numpy as np
from ..models.algorithm_exception import AlgorithmException


class MLEstimator:
    def __init__(self, response_pattern: List[int], item_difficulties: List[float]):
        """This class can be used to estimate the current ability level
        of a respondent given the response pattern and the corresponding
        item difficulties.
        The estimation is based on maximum likelihood estimation and the
        Rasch model.

        Args:
            response_pattern (List[int]): list of response patterns (0: wrong, 1:right)

            item_difficulties (List[float]): list of item difficulties
        """
        self.response_pattern = np.array(response_pattern)
        self.item_difficulties = np.array(item_difficulties)

    def get_maximum_likelihood_estimation(self) -> float:
        """Estimate the current ability level by searching
        for the maximum of the likelihood function.
        A line-search algorithm is used.

        Returns:
            float: ability estimation
        """
        return self._find_max()

    def d1_log_likelihood(self, ability: np.ndarray) -> float:
        """First derivative of the log-likelihood function.

        Args:
            ability (np.ndarray): ability level

        Returns:
            float: log-likelihood value of given ability value
        """
        item_term: np.ndarray = self.response_pattern - 1 + (
            1 / (1 + np.exp(ability - self.item_difficulties))
        )

        return float(np.cumsum(item_term)[-1])

    def _find_max(self) -> float:
        """
        Starts gradient descent algorithm.
        Do not call directly.
        Instead, use get_maximum_likelihood_estimation.

        Returns:
            float: ability estimation
        """
        return self.__step_1()

    def __step_1(self) -> float:
        """Line search algorithm with step length 0.1
        If no maximum can be found, a AlgorithmException is raised.

        Returns:
            float: ability estimation
        """
        previ_abil = -10

        for ability in np.arange(previ_abil, 10.1, 0.1):
            calculated_likelihood = self.d1_log_likelihood(ability)

            if calculated_likelihood <= 0:
                return self.__step_2(ability)

            else:
                previ_abil = ability

        raise AlgorithmException()

    def __step_2(self, last_max_ability: float) -> float:
        """Line search algorithm with step length -0.01
        If no maximum can be found, a AlgorithmException is raised.

        Args:
            last_max_ability (float): ability value that is the value before the last calculated ability level

        Returns:
            float: ability estimation
        """
        previ_abil = last_max_ability

        for ability in np.arange(last_max_ability, last_max_ability - 1, -0.01):
            calculated_likelihood = self.d1_log_likelihood(ability)

            if calculated_likelihood >= 0:
                return self.__step_3(ability)

            else:
                previ_abil = ability

        raise AlgorithmException()

    def __step_3(self, last_max_ability: float) -> float:
        """Line search algorithm with step length 0.0001
        If no maximum can be found, a AlgorithmException is raised.

        Args:
            last_max_ability (float): ability value that is the value before the last calculated ability level

        Returns:
            float: ability estimation
        """
        previ_abil = last_max_ability

        for ability in np.arange(last_max_ability, last_max_ability + 0.5, 0.0001):
            calculated_likelihood = self.d1_log_likelihood(ability)

            if calculated_likelihood <= 0:
                return previ_abil

            else:
                previ_abil = ability
        raise AlgorithmException()
