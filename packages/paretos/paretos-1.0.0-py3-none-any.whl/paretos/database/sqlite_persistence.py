from typing import List, Tuple, Optional

from sqlalchemy.orm import Session

from . import data_model
from .exceptions import ProjectAlreadyExists
from .sqlite_database import SQLiteDatabase
from .enums import ProjectStatusEnum, ParameterTypes, ParameterOptions

from .. import optimization


class SQLitePersistence:
    def __init__(self, database: SQLiteDatabase):
        self.__database = database

    def __project_exists(self, session: Session, project_name: str):
        count = session.query(data_model.Project) \
            .filter(data_model.Project.name == project_name) \
            .count()

        return count > 0

    def save_project(self, project: optimization.Project):
        session = self.__database.begin()
        project_name = project.get_name()
        project_id = project.get_id()

        if self.__project_exists(session=session, project_name=project_name):
            raise ProjectAlreadyExists()

        self.__database.add_project(
            session=session,
            project_name=project_name,
            project_id=project_id
        )

        problem = project.get_optimization_problem()

        self.__database.add_project_meta(
            session=session,
            project_id=project_id,
            problem=problem
        )

        session.commit()
        session.close()

    def save_planned_evaluations(
        self,
        evaluations: List[optimization.Evaluation],
        project: optimization.Project
    ):
        session = self.__database.begin()

        for evaluation in evaluations:
            project_id = project.get_id()
            simulation_id = evaluation.get_id()
            design = evaluation.get_design()
            kpis = evaluation.get_kpis()

            self.__database.add_simulation_design(
                session=session,
                project_id=project_id,
                simulation_id=simulation_id,
                design_values=design
            )

            if kpis is not None:
                self.__database.add_simulation_kpis(
                    session=session,
                    simulation_id=simulation_id,
                    kpi_values=kpis
                )

        session.commit()
        session.close()

    def update_project_status(self, project):
        session = self.__database.begin()
        project_id = project.get_id()

        if isinstance(project.get_status(), optimization.project_status.Done):
            status = ProjectStatusEnum.set.value
        else:
            raise RuntimeError("Unexpected new Project status.")

        self.__database.update_project_status(
            session,
            project_id=project_id,
            status=status
        )

        session.commit()
        session.close()

    def update_evaluation_add_kpis(self, evaluation):
        session = self.__database.begin()
        simulation_id = evaluation.get_id()
        kpi_values = evaluation.get_kpis()

        if kpi_values is None:
            raise RuntimeError("No KPIs to update.")

        self.__database.add_simulation_kpis(
            session=session,
            simulation_id=simulation_id,
            kpi_values=kpi_values
        )

        session.commit()
        session.close()

    def update_evaluation_pareto_states(
        self,
        evaluations: optimization.Evaluations
    ):
        session = self.__database.begin()

        for evaluation in evaluations.get_evaluations():
            db_evaluation = self.__database.get_simulation(session, evaluation.get_id())
            db_evaluation.is_pareto = evaluation.is_pareto_optimal()

        session.commit()
        session.close()

    def load_project_data_by_name(
        self,
        project_name: str
    ) -> Tuple[Optional[optimization.Project], optimization.Evaluations]:
        session = self.__database.begin()

        db_project = session.query(data_model.Project) \
            .filter_by(name=project_name) \
            .order_by(data_model.Project.time_created.desc()) \
            .first()

        if db_project is None:
            return None, optimization.Evaluations([])

        design_parameters = []
        kpi_parameters = []

        for db_parameter in db_project.parameter:
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
                    maximum=maximum
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
                    raise ValueError(
                        "Invalid goal specification for KPI parameter."
                    )

                kpi_parameter = optimization.kpi.KpiParameter(
                    name=db_parameter.name,
                    uuid=db_parameter.id,
                    goal=goal
                )

                kpi_parameters.append(kpi_parameter)

        design_space = optimization.design.DesignSpace(design_parameters)
        kpi_space = optimization.kpi.KpiSpace(kpi_parameters)

        problem = optimization.OptimizationProblem(
            design_space=design_space,
            kpi_space=kpi_space
        )

        db_project_status = session.query(data_model.ProjectStatus) \
            .filter_by(id=db_project.statusCodeId) \
            .one_or_none()

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

        evaluations = []

        for db_evaluation in db_project.simulation:
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
                            parameter=design_parameter,
                            value=db_parameter_value
                        )
                    )
                elif db_parameter_type == ParameterTypes.kpi.value:
                    kpi_parameter = kpi_space.get_parameter_by_id(db_parameter_id)
                    evaluation_kpi_values.append(
                        optimization.parameter.ParameterValue(
                            parameter=kpi_parameter,
                            value=db_parameter_value
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
                is_pareto_optimal=is_pareto
            )

            evaluations.append(evaluation)

        return project, optimization.Evaluations(evaluations)

    def get_evaluations(self, project_id: str) -> optimization.Evaluations:
        pass
