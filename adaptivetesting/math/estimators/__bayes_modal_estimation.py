from typing import List, Tuple, Literal, cast
import numpy as np
from ...services.__estimator_interface import IEstimator
from ...models.__test_item import TestItem
from .__functions.__bayes import maximize_posterior
from .__prior import Prior
from .__test_information import test_information_function, poly_test_information_function
from .__functions.__poly.__gpcm import GPCM
from .__functions.__poly.__grm import GRM


class BayesModal(IEstimator):
    def __init__(self,
                 response_pattern: List[int] | np.ndarray,
                 items: list[TestItem],
                 prior: Prior,
                 optimization_interval: Tuple[float, float] = (-10, 10),
                 model: Literal["GRM", "GPCM"] | None = None,):
        """This class can be used to estimate the current ability level
            of a respondent given the response pattern and the corresponding
            item difficulties.
            
            This type of estimation finds the maximum of the posterior distribution.


            Args:
                response_pattern (List[int] | np.ndarray ): list of response patterns (0: wrong, 1:right)

                items (list[TestItem]): list of answered items
            
                prior (Prior): prior distribution

                optimization_interval (Tuple[float, float]): interval used for the optimization function

                model (Literal["GRM", "GPCM"], optional): model type (required for polytomous models)
            """
        super().__init__(response_pattern, items, optimization_interval)

        self.prior = prior

        # decide type of model used
        if all([isinstance(item.b, list) for item in items]):
            self.type: Literal["poly", "dich"] = "poly"
            self.model = model
        else:
            self.type = "dich"

    def get_estimation(self) -> float:
        """Estimate the current ability level using Bayes Modal.
        The `bounded` optimizer is used
        to get the ability estimate.
        
        Raises:
            AlgorithmException: Raised when maximum could not be found.
        
        Returns:
            float: ability estimation
        """
        if self.type == "dich":
            return maximize_posterior(self.a,
                                      self.b,
                                      self.c,
                                      self.d,
                                      self.response_pattern,
                                      self.prior,
                                      optimization_interval=self.optimization_interval)
    
        if self.type == "poly":
            if self.model == "GRM":
                grm = GRM()
                return grm.maximize_posterior(
                    self.a_params,
                    self.thresholds_list,
                    cast(list[int], self.response_pattern.tolist()),
                    self.prior,
                    self.optimization_interval
                )
                
            if self.model == "GPCM":
                gpcm = GPCM()
                return gpcm.maximize_posterior(
                    self.a_params,
                    self.thresholds_list,
                    cast(list[int], self.response_pattern.tolist()),
                    self.prior,
                    self.optimization_interval
                )
        raise ValueError("model and/or type have not been correctly specified")

    def get_standard_error(self, estimation: float) -> float:
        """Calculates the standard error for the given estimated ability level.

        Args:
            estimation (float): currently estimated ability level

        Returns:
            float: standard error of the ability estimation
        """
        if self.type == "dich":
            test_information = test_information_function(
                np.array(estimation, dtype=float),
                a=self.a,
                b=self.b,
                c=self.c,
                d=self.d,
                prior=self.prior,
                optimization_interval=self.optimization_interval
            )

        else:
            if self.model is None:
                raise ValueError("model cannot be None")
            else:
                test_information = poly_test_information_function(
                    mu=estimation,
                    a_params=self.a_params,
                    thresholds_list=self.thresholds_list,
                    model_type=self.model,
                    optimization_interval=self.optimization_interval,
                    prior=self.prior
                )

        sd_error = 1 / np.sqrt(test_information)
        return float(sd_error)
