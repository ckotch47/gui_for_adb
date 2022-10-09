import sys


class hotkey_class:
    copy = 'Control-c'
    start = 'Control-Return'
    enter = 'Return'
    select_all = 'Control-KeyRelease-a'
    stop = 'Control-x'

    def __init__(self):
        if sys.platform == 'darwin':
            self.copy = 'Command-c'
            self.start = 'Command-Return'
            self.select_all = 'Command-KeyRelease-a'
            self.stop = 'Command-x'

hotkey = hotkey_class()
