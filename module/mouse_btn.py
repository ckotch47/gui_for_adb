import sys


class m_button:
    left = 'Button-1'
    right = 'Button-3'
    center = 'Button-2'
    double_left = 'Double-1'
    double_right = 'Double-2'

    def __init__(self):
        if sys.platform == 'darwin':
            self.left = 'Button-0'
            self.right = 'Button-2'
            self.center = 'Button-1'
            self.double_left = 'Double-0'
            self.double_right = 'Double-1'



mouse_btn = m_button()
