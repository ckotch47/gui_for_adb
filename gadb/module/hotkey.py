"""
hotkey into app
"""
import sys


class HotKey:
    """
    if os linux or window
    """
    copy = 'Control-c'
    start = 'Control-Return'
    enter = 'Return'
    select_all = 'Control-KeyRelease-a'
    stop = 'Control-x'

    def __init__(self):
        """
        if MacOs
        """
        if sys.platform == 'darwin':
            self.copy = 'Command-c'
            self.start = 'Command-Return'
            self.select_all = 'Command-KeyRelease-a'
            self.stop = 'Command-x'


hotkey = HotKey()
