"""
lock app
"""
import os


def lock_activate():
    """
    activate app lock
    """
    os.environ['app_lock'] = 'yes'


def lock_deactivate():
    """
    deactivate app lock
    """
    os.environ['app_lock'] = 'no'


def is_lock():
    """
    return true is app lock or return false
    """
    if os.getenv('app_lock') == 'yes':
        return True
    else:
        return False
