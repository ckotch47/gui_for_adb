import os
import sys
from pathlib import Path

folder_path = ''
if sys.platform == 'darwin' or sys.platform == 'win32':
    folder_path = f'{Path.home()}/documents/gadb'
else:
    folder_path = f'{Path.home()}/temp/gadb'
def check_config_ini():
    if os.path.exists(f'{folder_path}/config.ini'):
        pass
    else:

        create_config_ini()
    pass


def create_config_ini():
    os.system(f'mkdir {folder_path}')
    f = open(f'{folder_path}/config.ini', 'w+')
    f.write(f'[DEFAULT]\n'
            f'use_theme = no\n'
            f'theme_name = arc\n'
            f'adb_path = /\n'
            f'locale = en\n'
            )
    f.close()


def get_path_config():
    return f'{folder_path}/config.ini'
