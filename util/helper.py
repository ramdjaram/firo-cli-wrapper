import json


def stringify(dict_obj):
    return json.dumps(dict_obj)


def is_valid_dict_string(string):
    try:
        obj = json.loads(string)
        if isinstance(obj, dict) or isinstance(obj, list):
            return True
    except ValueError:
        print(f'String({string})\nis not an instance of dict or list, parsing skipped')
    return False


def print_command_title(call, command):
    call_length = len(call)
    even = call_length % 2 == 0
    hashtag = "##" if even else "#"
    line = f'\n{(call_length * 2) * "#"}{hashtag}\n'
    half_line = f'{int(call_length / 2) * "#"}'
    cli_command = ' '.join(command)
    print(f"{line}{half_line} {call.upper()} {half_line}{line}\nCli Command: [{cli_command}]")