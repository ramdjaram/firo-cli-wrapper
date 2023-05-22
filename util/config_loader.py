import os
import configparser
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
        cfg = configparser.ConfigParser()
        cfg.read(file_path)
        return cfg
    return None


config = load_config()


if __name__ == '__main__':
    print('Log level: ', config['LOGGER']['level'])
    print('Logs location: ', config['LOGGER']['logs_absolute_path'])
