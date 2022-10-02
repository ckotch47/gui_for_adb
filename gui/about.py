from tkinter import Toplevel, Frame, Label
from text import *


def show():
        __root = Toplevel()
        __root.geometry("600x200")
        __root.wm_title(text_about_window.title)
        frame = Frame(__root)
        label = Label(frame, text=text_about_window.text)
        label.pack(pady=20)

        label = Label(frame, text=text_about_window.github)
        label.pack(pady=20)

        frame.pack(expand=1, fill='both')
