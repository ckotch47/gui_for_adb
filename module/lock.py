import os


def lock_activate():
    os.environ['app_lock'] = 'yes'


def lock_deactivate():
    os.environ['app_lock'] = 'no'


def is_lock():
    if os.getenv('app_lock') == 'yes':
        return True
    else:
        return False
