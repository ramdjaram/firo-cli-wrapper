import configparser
import inspect
import os
import json
from pathlib import Path


def locate_file(dir_path, file):
    file_path = None
    for path in Path(dir_path).rglob(file):
        file_path = path
    if not file_path:
        print(
            f"ConfigFile [{file}] doesn't exist inside [{dir_path}] directory structure. Logger defaults will be used.")
    return file_path


def load_config(directory=Path(os.getcwd()).parent):
    file_path = locate_file(directory, 'firo.ini')
    if file_path:
        config = configparser.ConfigParser()
        config.read(file_path)
        return config
    return None


def get_all_methods_and_properties(clazz):
    return [name for name, value in inspect.getmembers(clazz)]


def get_methods_and_properties(clazz, dont=False, starts_with=''):
    if starts_with == '':
        return [name for name, value in inspect.getmembers(clazz)]
    if not dont:
        return [name for name, value in inspect.getmembers(clazz) if name.startswith(starts_with)]
    else:
        return [name for name, value in inspect.getmembers(clazz) if not name.startswith(starts_with)]


def stringify(dict_obj):
    return json.dumps(dict_obj)


def is_valid_dict_string(string):
    try:
        obj = json.loads(string)
        if isinstance(obj, dict) or isinstance(obj, list):
            return True
    except ValueError:
        print(f'String is not an instance of dict or list, parsing skipped.\n{string}')
    return False


def print_command_title(rpc_call, command, symbol):
    rpc_call_len = len(rpc_call)
    even = rpc_call_len % 2 == 0
    hashtag = 2 * symbol if even else symbol
    line = f'\n{(rpc_call_len * 2) * symbol}{hashtag}\n'
    half_line = f'{int(rpc_call_len / 2) * symbol}'
    cli_command = ' '.join(command)
    underline = f'{(len(cli_command) + 4) * "_"}\n'
    print(f"{line}{half_line} {rpc_call.upper()} {half_line}{line}{underline}Cli Command:\n\t{cli_command}\n")


def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


config = load_config()


if __name__ == '__main__':
    print('Log level: ', config['LOGGER']['level'])
    print('Logs location: ', config['LOGGER']['logs_absolute_path'])
