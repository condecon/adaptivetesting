from ...services.__estimator_interface import IEstimator

class BayesModal(IEstimator):
    def __init__(self, response_pattern, item_difficulties, prior):
        super().__init__(response_pattern, item_difficulties)


    def get_estimation(self):
        pass