from tkinter import Menu

from gui import settings, about
from module.check_device import device
from text import *


def init_top_menu(root, class_gui):
    top = root.winfo_toplevel()
    menuBar = Menu(top)
    top['menu'] = menuBar

    subMenu1 = Menu(menuBar)
    menuBar.add_cascade(label=text_menu_top.file, menu=subMenu1)
    subMenu1.add_command(label=text_menu_top.select_device, command=device.select_device_window)
    subMenu1.add_command(label=text_menu_top.exit, command=class_gui.on_closing)

    subMenu = Menu(menuBar)
    menuBar.add_cascade(label=text_menu_top.settings, menu=subMenu)
    subMenu.add_command(label=text_menu_top.performance, command=settings.show)
    subMenu.add_command(label=text_menu_top.about, command=about.show)