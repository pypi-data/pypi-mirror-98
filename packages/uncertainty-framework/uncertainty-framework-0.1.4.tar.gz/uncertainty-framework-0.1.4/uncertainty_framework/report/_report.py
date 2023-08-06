import abc
import numpy as np

class Report(abc.ABC):
    """Base class for all Reports"""
    def __init__(self, result: np.ndarray):
        self.result = result
    
    @abc.abstractmethod
    def render(self, **kwargs):
        pass

    def __call__(self, **kwargs):
        return self.render(**kwargs)