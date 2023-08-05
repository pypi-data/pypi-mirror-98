from typing import List


from . import DesignParameter
from ..parameter import ParameterSpace


class DesignSpace(ParameterSpace[DesignParameter]):
    def __init__(self, parameters: List[DesignParameter] = None):
        super().__init__(parameters)
