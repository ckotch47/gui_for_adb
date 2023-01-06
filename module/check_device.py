"""
check available device adb
"""
import os
import subprocess
from tkinter import *
from tkinter import messagebox

from module.mouse_btn import mouse_btn
from text import *
from gui import settings
import module.cfg as cfg


class Devices:
    """
    class for check available device
    """

    def __init__(self):
        """
        init class
        """
        self.m_btn = mouse_btn
        self.__root = None
        self.list_device_listbox = None
        self.popen = None
        self.ADB_Path = self.get_adb_path_from_config()

    def check_device(self):
        """
        function for get all device from adb
        """
        try:
            if self.get_current_device():  # device is select
                device_sh = ['-s', f'{self.get_current_device()}'] if self.get_current_device() else ['', '']
                self.popen = subprocess.Popen([self.ADB_Path + "adb", device_sh[0], device_sh[1], "shell", "ps", "-Af"],
                                              shell=False,
                                              stdout=subprocess.PIPE)
            else:
                self.popen = subprocess.Popen([self.ADB_Path + "adb", "shell", "ps", "-Af"],
                                              shell=False,
                                              stdout=subprocess.PIPE)
            try:  # try get info device
                next(iter(self.popen.stdout.readline, b""))
                return True
            except StopIteration:
                messagebox.showwarning(
                    MainText.warning_not_found_device.get('title'),
                    MainText.warning_not_found_device.get('text')
                )
                os.kill(self.popen.pid, 1)
                return False
        except FileNotFoundError:
            messagebox.showwarning(
                MainText.error_not_found_adb.get('title'),
                MainText.error_not_found_adb.get('text')
            )
            settings.select_folder()  # folder to adb
            self.ADB_Path = self.get_adb_path_from_config()

    def get_adb_path(self):
        """
        return path to adb
        """
        return self.ADB_Path

    def select_device_window(self):
        """
        window for select device
        TODO rework on listbox
        """
        if not self.check_device():
            return False

        self.__root = Toplevel()
        self.__root.attributes("-topmost", True)
        # __root.geometry("300x400")
        self.__root.wm_title(SelectDeviceText.title)
        frame = Frame(self.__root)
        label = Label(frame, text=SelectDeviceText.label)
        label.pack()
        frame.pack(expand=1, fill='both')

        list_device = self.get_list_devices()
        self.list_device_listbox = Listbox(frame, listvariable=Variable(value=list_device))
        self.list_device_listbox.pack(anchor=NW, fill='y', padx=5, pady=5)
        self.list_device_listbox.bind(f'<{self.m_btn.double_left}>', self.select_device_btn_callback)
        frame = Frame(self.__root)
        frame.pack(expand=1, fill='both')

        cancel_btn = Button(frame, text=SelectDeviceText.cancel_btn, command=self.cancel_btn_callback)
        cancel_btn.pack(side='left', anchor='s')

        ok_btn = Button(frame, text=SelectDeviceText.ok_btn, command=self.select_device_btn_callback)
        ok_btn.pack(side='right', anchor='s')

    def get_list_devices(self):
        """
        return all connected device
        """
        self.popen = subprocess.Popen([self.ADB_Path + "adb", "devices"], shell=False,
                                      stdout=subprocess.PIPE)
        next(iter(self.popen.stdout.readline, b""))
        res = []
        for i in iter(self.popen.stdout.readline, b""):
            if i != b'\n':
                res.append(i.decode('utf-8').split('\t')[0])

        return res

    def select_device_btn_callback(self, event=None):
        """
        select device into findow
        """
        selection = self.list_device_listbox.curselection()
        cur_device = self.list_device_listbox.get(selection[0])
        self.save_select_device(cur_device)
        self.__root.destroy()

    @staticmethod
    def save_select_device(select_device):
        """
        save device id into env
        """
        os.environ['select_device'] = select_device

    @staticmethod
    def del_select_device():
        """
        delete device id into env
        """
        os.environ['select_device'] = 'no'

    def cancel_btn_callback(self):
        """
        clos app where device not select
        """
        temp = self.get_list_devices()[0]
        if temp:
            self.save_select_device(temp)
        self.__root.destroy()

    @staticmethod
    def get_current_device():
        """
        return current device id
        """
        if os.getenv('select_device') != 'no':
            return os.getenv('select_device')
        else:
            return None

    @staticmethod
    def get_adb_path_from_config():
        """
        get path to adb from config
        """
        config = ConfigParser()
        config.read(cfg.get_path_config())
        if config.get('DEFAULT', 'adb_path') != 'no':
            temp = str(config.get('DEFAULT', 'adb_path'))
        else:
            temp = 'adb/'
        return temp


device = Devices()
