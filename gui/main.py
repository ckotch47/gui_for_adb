import os
from tkinter import messagebox, Tk, Menu
from gui import about, settings
from log_window.log_gui import *
from gui.topmenu import *
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

        init_top_menu(self._root, main_gui)

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
