from typing import List, Optional, Tuple

from .. import optimization
from . import data_model
from .data_model import Parameter, Simulation
from .enums import ParameterOptions, ParameterTypes, ProjectStatusEnum
from .sqlite_database import SQLiteDatabase


class SQLitePersistenceProjectLoader:
    def __init__(self, database: SQLiteDatabase):
        self.__database = database

    def load_project_data_by_name(
        self, project_name: str
    ) -> Tuple[Optional[optimization.Project], optimization.Evaluations]:
        session = self.__database.begin()

        db_project = (
            session.query(data_model.Project)
            .filter_by(name=project_name)
            .order_by(data_model.Project.time_created.desc())
            .first()
        )

        if db_project is None:
            return None, optimization.Evaluations([])

        design_parameters, kpi_parameters = self.map_db_parameters(db_project.parameter)

        design_space = optimization.design.DesignSpace(design_parameters)
        kpi_space = optimization.kpi.KpiSpace(kpi_parameters)

        problem = optimization.OptimizationProblem(
            design_space=design_space, kpi_space=kpi_space
        )

        db_project_status = (
            session.query(data_model.ProjectStatus)
            .filter_by(id=db_project.statusCodeId)
            .one_or_none()
        )

        if db_project_status is None:
            raise ValueError("Unable to get Project status.")

        if db_project_status.name == ProjectStatusEnum.set.value:
            status = optimization.project_status.Done()
        else:
            status = optimization.project_status.Ready()

        project = optimization.Project(
            uuid=db_project.id,
            name=db_project.name,
            problem=problem,
            status=status,
        )

        evaluations = self.map_db_evaluations(
            project=project, problem=problem, db_evaluations=db_project.simulation
        )

        return project, optimization.Evaluations(evaluations)

    def map_db_parameters(
        self, db_paramters: List[Parameter]
    ) -> Tuple[
        List[optimization.design.DesignParameter], List[optimization.kpi.KpiParameter]
    ]:
        design_parameters = []
        kpi_parameters = []

        for db_parameter in db_paramters:
            if db_parameter.type.name == ParameterTypes.design.value:
                minimum = None
                maximum = None

                for option in db_parameter.options:
                    if option.type.name == ParameterOptions.minimum.value:
                        minimum = option.number_value
                    elif option.type.name == ParameterOptions.maximum.value:
                        maximum = option.number_value

                if minimum is None or maximum is None:
                    raise ValueError(
                        "Incomplete boundary specification for design parameter."
                    )

                design_parameter = optimization.design.DesignParameter(
                    name=db_parameter.name,
                    uuid=db_parameter.id,
                    minimum=minimum,
                    maximum=maximum,
                )

                design_parameters.append(design_parameter)

            elif db_parameter.type.name == ParameterTypes.kpi.value:
                goal = None

                for option in db_parameter.options:
                    if option.type.name == ParameterOptions.goal.value:
                        if goal is not None:
                            raise ValueError("Invalid goals: Multiple goals.")

                        if option.string_value == "minimum":
                            goal = optimization.goals.Minimum()
                        elif option.string_value == "maximum":
                            goal = optimization.goals.Maximum()

                if goal is None:
                    raise ValueError("Invalid goal specification for KPI parameter.")

                kpi_parameter = optimization.kpi.KpiParameter(
                    name=db_parameter.name, uuid=db_parameter.id, goal=goal
                )

                kpi_parameters.append(kpi_parameter)

        return design_parameters, kpi_parameters

    def map_db_evaluations(
        self,
        project: optimization.Project,
        problem: optimization.OptimizationProblem,
        db_evaluations: List[Simulation],
    ) -> List[optimization.Evaluation]:

        design_space = problem.get_design_space()
        kpi_space = problem.get_kpi_space()
        status = project.get_status()

        evaluations = []

        for db_evaluation in db_evaluations:
            evaluation_design_values = []
            evaluation_kpi_values = []

            for db_evaluation_value in db_evaluation.values:
                if db_evaluation_value.parameter is None:
                    raise ValueError("Could not read evaluation parameter.")

                db_parameter_id = db_evaluation_value.parameter.id
                db_parameter_type = db_evaluation_value.parameter.type.name
                db_parameter_value = db_evaluation_value.number_value

                if db_parameter_type == ParameterTypes.design.value:
                    design_parameter = design_space.get_parameter_by_id(db_parameter_id)
                    evaluation_design_values.append(
                        optimization.parameter.ParameterValue(
                            parameter=design_parameter, value=db_parameter_value
                        )
                    )
                elif db_parameter_type == ParameterTypes.kpi.value:
                    kpi_parameter = kpi_space.get_parameter_by_id(db_parameter_id)
                    evaluation_kpi_values.append(
                        optimization.parameter.ParameterValue(
                            parameter=kpi_parameter, value=db_parameter_value
                        )
                    )
                else:
                    raise ValueError("Unexpected parameter type.")

            kpi_values = None

            if len(evaluation_kpi_values) > 0:
                kpi_values = optimization.kpi.KpiValues(evaluation_kpi_values)

            is_pareto = None

            if isinstance(status, optimization.project_status.Done):
                is_pareto = db_evaluation.is_pareto

            evaluation = optimization.Evaluation(
                uuid=db_evaluation.id,
                design=optimization.design.DesignValues(evaluation_design_values),
                kpis=kpi_values,
                is_pareto_optimal=is_pareto,
            )

            evaluations.append(evaluation)

        return evaluations
