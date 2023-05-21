import ast


def json_str_to_dict(string_representation_of_dict):
    return ast.literal_eval(string_representation_of_dict)
