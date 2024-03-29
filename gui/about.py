"""
about window
"""
from tkinter import Toplevel, Frame, Label
from text import *


def show():
    """
    setting and show about gui
    """
    _root_about = Toplevel()
    _root_about.geometry("600x200")
    _root_about.wm_title(AboutGuiText.title)

    frame = Frame(_root_about)

    label = Label(frame, text=AboutGuiText.text)
    label.pack(pady=20)

    label = Label(frame, text=AboutGuiText.github)
    label.pack(pady=20)

    frame.pack(expand=1, fill='both')
