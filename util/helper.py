import ast


def to_dict(string_representation_of_dict):
    # string_representation_of_dict.replace('\n', '')
    return ast.literal_eval(string_representation_of_dict)
