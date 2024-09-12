"""
mouse btn
"""
import sys


class MouseBtn:
    """
    if os is linux or window
    """
    left = 'Button-1'
    right = 'Button-3'
    center = 'Button-2'
    double_left = 'Double-1'
    double_right = 'Double-2'

    def __init__(self):
        """
        if MacOs
        """
        if sys.platform == 'darwin':
            self.left = 'Button-1'
            self.right = 'Button-2'
            self.center = 'Button-3'
            self.double_left = 'Double-1'
            self.double_right = 'Double-2'



mouse_btn = MouseBtn()
