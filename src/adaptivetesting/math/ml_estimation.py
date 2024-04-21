from .mle_tensorflow import MLE_Tensorflow
from typing import List
import numpy as np
class MLEstimator(MLE_Tensorflow):
    def __init__(self, ResponsePattern: List[int], ItemDifficulties: List[float]):
        super().__init__(np.array(ResponsePattern, dtype="float64"), 
                         np.array(ItemDifficulties, dtype="float64"))

    def get_maximum_likelihood_estimation(self) -> float:
        return self.find_max()

    def likelihood(self, ability: float) -> float:
        return self.log_likelihood(np.array([ability], dtype="float64"))
