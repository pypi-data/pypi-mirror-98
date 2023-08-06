class DesignParameter:
    """
    Class describing a single design parameter including its options
    """

    def __init__(
        self,
        name: str,
        minimum: float,
        maximum: float,
    ):
        if not minimum < maximum:
            raise ValueError(
                "Design parameter maximum has to be greater than the design parameter "
                "minimum. "
            )

        self.__name = name
        self.__minimum = minimum
        self.__maximum = maximum

    def get_name(self) -> str:
        return self.__name

    def get_minimum(self) -> float:
        return self.__minimum

    def get_maximum(self) -> float:
        return self.__maximum
