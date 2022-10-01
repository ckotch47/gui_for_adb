import os
import sys
from tkinter import messagebox, Tk
from configparser import ConfigParser
from tabone.tabone_gui import *
from tabtwo.tabtwo_gui import *

from text.text_en import *
import module.lock as app_lock

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

        self.init_tab()
        self._root.mainloop()

    def init_tab(self):
        frame = ttk.Frame(self._root)
        gui_tab_two.tabTwo_init(frame)
        frame.pack(expand=1, fill="both")


    @staticmethod
    def on_closing():
        if app_lock.is_lock():
            messagebox.showwarning(
                main_text.warning_stop_log_before_close_app.get('title'),
                main_text.warning_stop_log_before_close_app.get('text')
            )
            return False
        else:
            os.system("adb kill-server")
            sys.exit(0)


gui = main_gui()

