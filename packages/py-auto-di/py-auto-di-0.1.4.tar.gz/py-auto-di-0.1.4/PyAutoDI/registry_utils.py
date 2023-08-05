from inspect import signature, getmembers
import re

def get_all_constructor_dependencies(dependency_class):
    parameters = signature(dependency_class.__init__).parameters
    parameter_names = []

    for parameter in parameters:
        parameter_names.append(parameter)

    return parameter_names[1:]


def strip_leading_underscores(string_to_clean):
    return re.sub("^(_)+", "", string_to_clean)


def get_dependency_name(dependency_class):
    member_list = getmembers(dependency_class)
    class_name = dependency_class.__name__

    dependency_name = re.sub("([A-Z])", "_\\1", class_name).lower()

    return strip_leading_underscores(dependency_name)


def build_dependency_definition(dependency_class, interface):
    dependency_names = get_all_constructor_dependencies(dependency_class)

    return {
        "dependency_class": dependency_class,
        "dependency_names": dependency_names,
        "interface": interface
    }

