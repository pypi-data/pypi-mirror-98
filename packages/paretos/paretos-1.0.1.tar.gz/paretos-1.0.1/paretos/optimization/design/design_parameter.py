from typing import Optional

from ..parameter import Parameter


class DesignParameter(Parameter):
    """
    Class describing a single design parameter including its options
    """

    def __init__(
        self, name: str, minimum: float, maximum: float, uuid: Optional[str] = None
    ):
        super().__init__(
            name=name,
            uuid=uuid,
        )

        self.__minimum = minimum
        self.__maximum = maximum

    def get_minimum(self) -> float:
        return self.__minimum

    def get_maximum(self) -> float:
        return self.__maximum
