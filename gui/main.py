"""
main window settings and show
"""
from tkinter import messagebox, Tk
import os
import sys

from log_window.log_gui import *
from gui.topmenu import *
from text import *
from module.check_device import device
import module.cfg as cfg
import module.lock as app_lock

# TODO rework configParser into one file
config = ConfigParser()
config.read(cfg.get_path_config())
is_theme = False

if config.get('DEFAULT', 'use_theme') == 'yes':
    is_theme = True

try:
    from ttkthemes.themed_tk import ThemedTk
except:
    is_theme = False


class MainGui:
    """
    class for main process
    """
    def __init__(self):
        """
        function call init class
        """
        self._tabControl = None
        self._root = None

        self.m_btn = mouse_btn
        self.style = None

    def init_root(self):
        """
        init function
        """
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

        init_top_menu(self._root, MainGui)

        self.init_window()

        self._root.mainloop()

    def init_window(self):
        """
        init start frame
        """
        frame = ttk.Frame(self._root)
        log_gui.log_gui_init(frame)
        frame.pack(expand=1, fill="both")
        device.select_device_window()

    @staticmethod
    def on_closing():
        """
        function calling where app trigger close
        """
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


gui = MainGui()
