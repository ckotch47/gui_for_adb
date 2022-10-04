import os
import sys
from tkinter import messagebox, Tk, Menu
from configparser import ConfigParser
from activity.activity_gui import *
from gui import about, settings
from log_window.log_gui import *

from text import *
import module.lock as app_lock
from module.check_device import device

config = ConfigParser()
config.read('config.ini')
is_theme = False

if config.get('DEFAULT', 'use_theme') == 'yes':
    is_theme = True

try:
    from ttkthemes.themed_tk import ThemedTk
except:
    is_theme = False


class main_gui:
    def __init__(self):
        self._tabControl = None
        self._root = None

        self.m_btn = mouse_btn
        self.style = None

    def init_root(self):
        theme = config.get('DEFAULT', 'theme_name')
        if is_theme and theme != '':
            try:
                self._root = ThemedTk(theme=theme)
            except:
                self._root = Tk()
        else:
            self._root = Tk()

        self._root.title(main_text.title)
        self._root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self._root.geometry("900x540")

        top = self._root.winfo_toplevel()
        menuBar = Menu(top)
        top['menu'] = menuBar

        subMenu1 = Menu(menuBar)
        menuBar.add_cascade(label=text_menu_top.file, menu=subMenu1)
        subMenu1.add_command(label=text_menu_top.select_device, command=device.select_device_window)
        subMenu1.add_command(label=text_menu_top.exit, command=self.on_closing)

        subMenu = Menu(menuBar)
        menuBar.add_cascade(label=text_menu_top.settings, menu=subMenu)
        subMenu.add_command(label=text_menu_top.performance, command=settings.show)
        subMenu.add_command(label=text_menu_top.about, command=about.show)

        self.init_window()

        self._root.mainloop()

    def init_window(self):
        frame = ttk.Frame(self._root)
        gui_tab_two.tabTwo_init(frame)
        frame.pack(expand=1, fill="both")
        device.select_device_window()



    @staticmethod
    def on_closing():
        if app_lock.is_lock():
            messagebox.showwarning(
                main_text.warning_stop_log_before_close_app.get('title'),
                main_text.warning_stop_log_before_close_app.get('text')
            )
            return False
        else:
            device.del_select_device()
            os.system("adb kill-server")
            sys.exit(0)


gui = main_gui()
