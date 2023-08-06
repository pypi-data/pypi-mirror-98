from typing import List, Optional
from uuid import uuid4

from .design import DesignValues
from .kpi import KpiValues


class Evaluation:
    """
    Class for a single evaluation with matching design and kpis
    """

    def __init__(
        self,
        design: DesignValues,
        kpis: KpiValues = None,
        is_pareto_optimal: Optional[bool] = None,
        uuid: str = None,
    ):
        self.__id = uuid or str(uuid4())
        self.__design = design
        self.__kpis = kpis
        self.__is_pareto_optimal = is_pareto_optimal

    def add_result(self, kpis: KpiValues):
        self.__kpis = kpis

    def get_id(self) -> str:
        return self.__id

    def get_design(self) -> DesignValues:
        return self.__design

    def get_kpis(self) -> Optional[KpiValues]:
        return self.__kpis

    def is_pareto_optimal(self) -> Optional[bool]:
        return self.__is_pareto_optimal

    def update_pareto_optimality(self, is_pareto_optimal: bool):
        self.__is_pareto_optimal = is_pareto_optimal


class Evaluations:
    """
    Class containing all evaluations
    """

    def __init__(self, evaluation: List[Evaluation] = None):
        if evaluation is None:
            evaluation = []
        self.__evaluations = evaluation

    def get_evaluations(self) -> List[Evaluation]:
        return self.__evaluations

    def add_evaluation(self, evaluation: Evaluation):
        self.__evaluations.append(evaluation)

    def get_pareto_optimal_evaluations(self) -> List[Evaluation]:
        pareto_optima = []

        for evaluation in self.__evaluations:
            if evaluation.is_pareto_optimal():
                pareto_optima.append(evaluation)

        return pareto_optima
