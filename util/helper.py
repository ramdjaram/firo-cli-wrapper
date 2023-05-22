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


def print_command_title(rpc_call, command):
    rpc_call_len = len(rpc_call)
    even = rpc_call_len % 2 == 0
    hashtag = "||" if even else "|"
    line = f'\n{(rpc_call_len * 2) * "|"}{hashtag}\n'
    half_line = f'{int(rpc_call_len / 2) * "|"}'
    cli_command = ' '.join(command)
    underline = f'{(len(cli_command)+13) * "_"}\n'
    print(f"{line}{half_line} {rpc_call.upper()} {half_line}{line}{underline}Cli Command:\n\t{cli_command}\n")