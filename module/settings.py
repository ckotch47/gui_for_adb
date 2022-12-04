import os


def check_config_ini():
    if os.path.exists('~/documents/adb_gui/config.ini'):
        pass
    else:
        os.makedirs('~/documents/adb_gui', exist_ok=True)
        open('~/documents/adb_gui/config.ini', 'w')
    pass


def create_config_ini():
    pass
