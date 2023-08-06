from easyvalidator import base_rules
import re
REGEX_EXTRACT_ARGUMENTS = r'\((.+?)\)'

def extract_class_name(rule_name):
    return rule_name.split("(")[0]

def convert_to_dict(str_parameters):
    result = {}
    parameters_array = str_parameters.split(",")
    for parameter in parameters_array:
        split = parameter.split("=")
        key = split[0].strip()
        value = split[1].strip()
        result[key] = value
    return result

def extract_parameters(rule_name):
    try:
        str_parameters = re.findall(REGEX_EXTRACT_ARGUMENTS, rule_name)[0]
        dict_parameters = convert_to_dict(str_parameters)
        return dict_parameters
    except Exception as e:
        return {}

def create_rule(rule_name):
    class_name = extract_class_name(rule_name)
    parameters = extract_parameters(rule_name)
    class_ = getattr(base_rules, class_name)
    return class_(**parameters)