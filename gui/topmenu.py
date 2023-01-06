"""
setting topmenu
"""
from tkinter import Menu
from gui import settings, about
from module.check_device import device
from text import *


def init_top_menu(root, class_gui):
    """
    setting top menu
    """
    top = root.winfo_toplevel()
    menu_bar = Menu(top)
    top['menu'] = menu_bar

    sub_menu_file = Menu(menu_bar)
    menu_bar.add_cascade(label=text_menu_top.file, menu=sub_menu_file)
    sub_menu_file.add_command(label=text_menu_top.select_device, command=device.select_device_window)
    sub_menu_file.add_command(label=text_menu_top.exit, command=class_gui.on_closing)

    sub_menu_settings = Menu(menu_bar)
    menu_bar.add_cascade(label=text_menu_top.settings, menu=sub_menu_settings)
    sub_menu_settings.add_command(label=text_menu_top.performance, command=settings.show)
    sub_menu_settings.add_command(label=text_menu_top.about, command=about.show)
