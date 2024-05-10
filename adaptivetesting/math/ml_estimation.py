from typing import List
import numpy as np
from ..models.algorithm_exception import AlgorithmException


class MLEstimator:
    def __init__(self, ResponsePattern: List[int], ItemDifficulties: List[float]):
        """This class can be used to estimate the current ability level
        of a respondent given the response pattern and the corresponding
        item difficulties.
        The estimation is based on maximum likelihood estimation and the
        Rasch model.

        Args:
            ResponsePattern (List[int]): list of response patterns (0: wrong, 1:right)
            ItemDifficulties (List[float]): list of item difficulties
        """
        self.response_pattern = np.array(ResponsePattern)
        self.item_difficulties = np.array(ItemDifficulties)

    def get_maximum_likelihood_estimation(self) -> float:
        """Estimate the current ability level by searching
        for the maximum of the likelihood function.
        Therefore, a line-search algorithm is used.

        Returns:
            float: ability estimation
        """
        return self._find_max()

    def log_likelihood(self, ability: np.ndarray) -> np.ndarray:
        """
        Log-Likelihood function. Value is calculated for the given ability level.

        Args:
            ability (np.ndarray): ability level

        Returns:
            np.ndarray: Log-Likelihood of the response pattern and item difficulties
            given the ability level
        """

        item_terms = (self.response_pattern * (ability - self.item_difficulties) -
                      np.log(1 + np.exp(ability - self.item_difficulties)))

        log_likelihood = np.cumsum(item_terms)[len(item_terms) - 1]

        return log_likelihood

    def _find_max(self) -> float:
        """
        Stars line search algorithm.
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
        previ_lik = float("-inf")

        for ability in np.arange(previ_abil, 10.1, 0.1):
            calculated_likelihood = self.log_likelihood(ability)

            if calculated_likelihood <= previ_lik:
                return self.__step_2(ability)

            else:
                # update lik
                previ_lik = calculated_likelihood
                previ_abil = ability

        raise AlgorithmException()

    def __step_2(self, last_max_ability: float) -> float:
        """Line search algorithm with step length -0.01
        If no maximum can be found, a AlgorithmException is raised.

        Returns:
            float: ability estimation
        """
        previ_lik = float("-inf")
        previ_abil = last_max_ability

        for ability in np.arange(last_max_ability, last_max_ability - 1, -0.01):
            calculated_likelihood = self.log_likelihood(ability)

            if calculated_likelihood <= previ_lik:
                return self.__step_3(ability)

            else:
                # update lik
                previ_lik = calculated_likelihood
                previ_abil = ability

        raise AlgorithmException()

    def __step_3(self, last_max_ability: float) -> float:
        """Line search algorithm with step length 0.0001
        If no maximum can be found, a AlgorithmException is raised.

        Returns:
            float: ability estimation
        """
        previ_lik = float("-inf")
        previ_abil = last_max_ability

        for ability in np.arange(last_max_ability, last_max_ability + 0.5, 0.0001):
            calculated_likelihood = self.log_likelihood(ability)

            if calculated_likelihood <= previ_lik:
                return previ_abil

            else:
                # update lik
                previ_lik = calculated_likelihood
                previ_abil = ability
        raise AlgorithmException()