from .optimization import ParameterValues


def parameter_values_as_dict(parameter_values: ParameterValues):
    dict_data = {}

    for parameter_value in parameter_values:
        name = parameter_value.get_parameter().get_name()
        float_value = parameter_value.get_value()

        dict_data[name] = float_value

    return dict_data
