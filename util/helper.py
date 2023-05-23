import json
from util.logger import logger


def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def stringify(dict_obj):
    return json.dumps(dict_obj)


def is_valid_dict_string(string):
    try:
        obj = json.loads(string)
        if isinstance(obj, dict) or isinstance(obj, list):
            return True
    except ValueError:
        logger.info(f'String is not an instance of dict or list, parsing skipped.\n{string}')
    return False


def print_command_title(rpc_call, command, symbol):
    rpc_call_len = len(rpc_call)
    even = rpc_call_len % 2 == 0
    hashtag = 2 * symbol if even else symbol
    line = f'\n{(rpc_call_len * 2) * symbol}{hashtag}\n'
    half_line = f'{int(rpc_call_len / 2) * symbol}'
    cli_command = ' '.join(command)
    underline = f'{(len(cli_command) + 8) * "_"}\n'
    logger.info(f"Executing rpc [{rpc_call}]{(28 - rpc_call_len) * '.'}\n\n"
                f"{line}"  # upper title wrapper
                f"{half_line} {rpc_call.upper()} {half_line}"  # uppercase command title
                f"{line}"  # under title wrapper
                f"{underline}"
                f"Cli Command:\n"  # command label
                f"\t{cli_command}\n"  # actual executed command
                f"{underline}")
