import configparser
import os

from paretos import (
    DesignParameter,
    DesignSpace,
    KpiParameter,
    KpiSpace,
    OptimizationProblem,
    Evaluations,
    Minimize
)
from paretos.logger import DefaultLogger

from paretos.socrates.client import SocratesAPIClient

init_config = configparser.ConfigParser()
config_file = os.path.realpath(os.path.join(os.getcwd(), "env.ini"))
init_config.read(config_file)

client = SocratesAPIClient(
    init_config["DEVELOP"]["SOCRATES_URL"].strip('"'),
    init_config["DEVELOP"]["CUSTOMER_TOKEN"].strip('"'),
    logger=DefaultLogger()
)
design_1 = DesignParameter("x", minimum=-5, maximum=5)
design_2 = DesignParameter("y", minimum=-5, maximum=5)

design_space = DesignSpace([design_1, design_2])

kpi_1 = KpiParameter("f1", Minimize())
kpi_2 = KpiParameter("f2")

kpi_space = KpiSpace([kpi_1, kpi_2])

optimization_space = OptimizationProblem(design_space, kpi_space)
resp = client.predict_design(
    optimization_space,
    Evaluations(),
    1000,
)
designs = client.predict_design(
    optimization_space,
    Evaluations(),
    10000,
)

print(len(designs.get_designs()))
