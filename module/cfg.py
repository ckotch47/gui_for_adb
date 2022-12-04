import os
from pathlib import Path


def check_config_ini():
    if os.path.exists(f'{Path.home()}/temp/gadb/config.ini'):
        pass
    else:
        create_config_ini()
    pass


def create_config_ini():
    try:
        os.system('mkdir ~/temp/gadb')
    except FileExistsError:
        pass
    f = open(f'{Path.home()}/temp/gadb/config.ini', 'w+')
    f.write(f'[DEFAULT]\n'
            f'use_theme = no\n'
            f'theme_name = arc\n'
            f'adb_path = /\n'
            f'locale = en\n'
            )
    f.close()


def get_path_config():
    return f'{Path.home()}/temp/gadb/config.ini'
