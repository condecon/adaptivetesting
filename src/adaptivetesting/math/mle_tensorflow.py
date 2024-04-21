import numpy as np
from ..models.algorithm_exception import AlgorithmException


class MLE_Tensorflow:
    """Make maximum likelihood estimations with tensorflow"""

    def __init__(self, response_pattern: np.ndarray, item_difficulties: np.ndarray):
        self.response_pattern = response_pattern
        self.item_difficulties = item_difficulties

    def log_likelihood(self, ability: np.ndarray) -> np.ndarray:
        """
        Log-Likelihood function. Value is calculated for the given ability level.
        Ability level is converted to tensor internally.
        Args:
            ability:

        Returns:

        """

        item_terms = (self.response_pattern * (ability - self.item_difficulties) -
                      np.log(1 + np.exp(ability - self.item_difficulties)))

        log_likelihood = np.cumsum(item_terms)[len(item_terms) - 1]

        return log_likelihood

    def find_max(self) -> float:
        """
        Find maximum of likelihood function

        Returns: ability level (float)

        """
        return self.__step_1()

    def __step_1(self) -> float:
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
        previ_lik = float("-inf")
        previ_abil = last_max_ability

        for ability in np.arange(last_max_ability, last_max_ability + 0.5, 0.001):
            calculated_likelihood = self.log_likelihood(ability)

            if calculated_likelihood <= previ_lik:
                return previ_abil

            else:
                # update lik
                previ_lik = calculated_likelihood
                previ_abil = ability
        raise AlgorithmException()
