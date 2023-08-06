from datetime import datetime
from logging import Logger, LoggerAdapter
from typing import List, Optional, Union
from urllib.parse import urljoin

from requests import Response, Session
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError

from .. import OptimizationProblem, optimization
from ..interface import ProgressInterface
from ..version import VERSION
from .authenticate import AccessToken
from .exceptions import InvalidResponseStructure, RequestFailed, ResponseParsingError
from .request_mapper import SocratesRequestMapper
from .response_mapper import SocratesResponseMapper


class SocratesAPIClient(object):
    def __init__(
        self, api_url: str, customer_token: str, logger: Union[Logger, LoggerAdapter]
    ):
        """
        Instantiate a new API client.
        :param api_url: url of the api
        :param customer_token: string containing the customer credentials
        """
        self.__url = api_url
        self.__session = Session()
        self.__customer_token = customer_token
        self.__access_token: Optional[AccessToken] = None
        self.__logger = logger

        # https://2.python-requests.org/en/master/api/#requests.adapters.HTTPAdapter
        retry_adapter = HTTPAdapter(max_retries=5)
        self.__session.mount("http://", retry_adapter)
        self.__session.mount("https://", retry_adapter)

        self.__session.headers.update(
            {
                "Accept-Charset": "utf-8",
                "Content-Type": "application/json",
                "User-Agent": "paretos/{}".format(VERSION),
            }
        )

    @staticmethod
    def __get_versioned_path(path: str, version: str = "v1") -> str:
        return f"{version}/{path}"

    def __request(
        self,
        path: str,
        version: str,
        contains_sensitive_data: bool,
        data: dict = None,
        method: str = "POST",
        access_token: str = None,
    ):
        if method not in ["POST", "GET"]:
            raise ValueError("Invalid Request method chosen.")

        path = self.__get_versioned_path(path, version)

        if access_token is not None:
            auth_header = "Bearer {}".format(access_token)
            self.__session.headers["Authorization"] = auth_header
        else:
            if "Authorization" in self.__session.headers:
                del self.__session.headers["Authorization"]

        url = urljoin(self.__url, path)

        self.__log_request(
            url=url,
            method=method,
            data=data,
            contains_sensitive_data=contains_sensitive_data,
        )

        try:
            response = self.__session.request(method, url, json=data)
        except ConnectionError:
            self.__logger.error(
                "Unable to connect to Socrates API.", extra={"url": url}
            )

            raise RuntimeError("Unable to connect to Socrates API.")

        self.__log_response(
            contains_sensitive_data=contains_sensitive_data, response=response
        )

        try:
            response_json = response.json()
        except ValueError:
            self.__logger.error("Unable to parse Socrates API response json.")
            raise ResponseParsingError()

        if "status" not in response_json:
            self.__logger.error("Unexpected Socrates API response.")
            raise InvalidResponseStructure()

        if response_json["status"] != "success":
            self.__logger.error(
                "Socrates API request failed.", extra={"response": response_json}
            )

            raise RequestFailed()

        return response_json["data"]

    def __update_access_token_if_necessary(self):
        if self.__access_token is None or self.__access_token.is_token_expired():
            self.__access_token = self.__authenticate(self.__customer_token)

    def __authenticated_request(
        self,
        path: str,
        version: str,
        contains_sensitive_data: bool,
        data: dict = None,
        method: str = "POST",
    ):
        self.__update_access_token_if_necessary()

        access_token_string = self.__access_token.get_access_token()

        return self.__request(
            path=path,
            version=version,
            contains_sensitive_data=contains_sensitive_data,
            data=data,
            method=method,
            access_token=access_token_string,
        )

    def __log_request(self, url: str, method: str, data, contains_sensitive_data: bool):
        details = {"url": url, "method": method}

        if not contains_sensitive_data:
            details["data"] = data

        self.__logger.debug("Socrates API request.", extra=details)

    def __log_response(self, contains_sensitive_data: bool, response: Response):
        details = {"status": response.status_code}

        if not contains_sensitive_data:
            details["data"] = response.text

        self.__logger.debug("Socrates API response.", extra=details)

    def __authenticate(self, customer_token: str, version: str = "v1") -> AccessToken:
        response = self.__request(
            path="authenticate",
            version=version,
            data={"customerToken": customer_token},
            access_token=None,
            contains_sensitive_data=True,
        )

        access_token = response["accessToken"]
        expiration_iso8601 = response["accessTokenExpiration"]
        expiration_date = datetime.fromisoformat(expiration_iso8601)

        return AccessToken(access_token=access_token, expires=expiration_date)

    def __problem_request(
        self,
        path: str,
        version: str,
        problem: OptimizationProblem,
        evaluations: optimization.Evaluations,
        additional_data: dict = None,
    ):
        if additional_data is None:
            additional_data = {}

        request_evaluations = SocratesRequestMapper.evaluations_to_request(evaluations)
        request_problem = SocratesRequestMapper.problem_to_request(problem)

        problem_data = {
            "problem": request_problem,
            "evaluations": request_evaluations,
        }

        data = {**problem_data, **additional_data}

        return self.__authenticated_request(
            path=path, version=version, contains_sensitive_data=False, data=data
        )

    # API methods
    def predict_design(
        self,
        problem: OptimizationProblem,
        evaluations: optimization.Evaluations,
        quantity: int,
        version: str = "v1",
    ) -> optimization.design.Designs:
        response = self.__problem_request(
            "design/predict", version, problem, evaluations, {"quantity": quantity}
        )

        designs = SocratesResponseMapper.predict_response_to_designs(
            problem=problem, response_data=response
        )

        return designs

    def track_progress(
        self,
        problem: OptimizationProblem,
        evaluations: optimization.Evaluations,
        version: str = "v1",
    ) -> ProgressInterface:
        response = self.__problem_request(
            "progress/track", version, problem, evaluations
        )

        progress = SocratesResponseMapper.track_response_to_progress(
            response_data=response
        )

        return progress

    def get_pareto_optimal_evaluation_ids(
        self,
        problem: OptimizationProblem,
        evaluations: optimization.Evaluations,
        version: str = "v1",
    ) -> List[str]:
        response = self.__problem_request(
            "result/analyze", version, problem, evaluations
        )

        optimal_ids = []

        for evaluation_data in response["evaluations"]:
            evaluation_id = evaluation_data["evaluationId"]
            is_optimal = evaluation_data["isParetoOptimal"]

            if is_optimal:
                optimal_ids.append(evaluation_id)

        return optimal_ids
