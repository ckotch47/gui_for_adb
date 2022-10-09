from configparser import ConfigParser

config_path = 'tmp/lock.tmp'

config = ConfigParser()
config.read(config_path)


def lock_activate():
    config['DEFAULT']['app_lock'] = 'yes'
    config.write(open(config_path, 'w'))

def lock_deactivate():
    config['DEFAULT']['app_lock'] = 'no'
    config.write(open(config_path, 'w'))


def is_lock():
    temp = config.get('DEFAULT', 'app_lock')
    if temp == 'yes':
        return True
    else:
        return False






