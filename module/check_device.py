import os
import subprocess
from configparser import ConfigParser
from tkinter import *
from tkinter import messagebox

from module.mouse_btn import mouse_btn
from text import *


class devices:
    def __init__(self):
        self.m_btn = mouse_btn
        self.__root = None
        self.list_device_listbox = None
        self.popen = None
        config = ConfigParser()
        config.read('config.ini')
        if config.get('DEFAULT', 'adb_path') != 'no':
            self.ADB_Path = str(config.get('DEFAULT', 'adb_path'))
        else:
            self.ADB_Path = 'adb/'

    def check_device(self):
        if self.get_current_device():
            device_sh = ['-s', f'{self.get_current_device()}'] if self.get_current_device() else ['', '']
            self.popen = subprocess.Popen([self.ADB_Path + "adb", device_sh[0], device_sh[1], "shell", "ps", "-Af"],
                                          shell=False,
                                          stdout=subprocess.PIPE)
        else:
            self.popen = subprocess.Popen([self.ADB_Path + "adb",  "shell", "ps", "-Af"],
                                          shell=False,
                                          stdout=subprocess.PIPE)
        try:
            next(iter(self.popen.stdout.readline, b""))
            return True
        except StopIteration:
            messagebox.showwarning(
                main_text.warning_not_found_device.get('title'),
                main_text.warning_not_found_device.get('text')
            )
            os.kill(self.popen.pid, 1)
            return False

    def get_adb_path(self):
        return self.ADB_Path

    def select_device_window(self):
        if not self.check_device():
            return False

        self.__root = Toplevel()
        # __root.geometry("300x400")
        self.__root.wm_title(text_select_device.title)
        frame = Frame(self.__root)
        label = Label(frame, text=text_select_device.label)
        label.pack()
        frame.pack(expand=1, fill='both')

        list_device = self.get_list_devices()
        self.list_device_listbox = Listbox(frame, listvariable=Variable(value=list_device))
        self.list_device_listbox.pack(anchor=NW, fill='y', padx=5, pady=5)
        self.list_device_listbox.bind(f'<{self.m_btn.double_left}>', self.select_device_btn_callback)
        frame = Frame(self.__root)
        frame.pack(expand=1, fill='both')

        cancel_btn = Button(frame, text=text_select_device.cancel_btn, command=self.cancel_btn_callback)
        cancel_btn.pack(side='left', anchor='s')

        ok_btn = Button(frame, text=text_select_device.ok_btn, command=self.select_device_btn_callback)
        ok_btn.pack(side='right', anchor='s')

    def get_list_devices(self):
        self.popen = subprocess.Popen([self.ADB_Path + "adb", "devices"], shell=False,
                                      stdout=subprocess.PIPE)
        next(iter(self.popen.stdout.readline, b""))
        res = []
        for i in iter(self.popen.stdout.readline, b""):
            if i != b'\n':
                res.append(i.decode('utf-8').split('\t')[0])

        return res

    def select_device_btn_callback(self, event=None):
        selection = self.list_device_listbox.curselection()
        cur_device = self.list_device_listbox.get(selection[0])
        self.save_select_device(cur_device)
        self.__root.destroy()

    @staticmethod
    def save_select_device(select_device):
        config = ConfigParser()
        config.read('tmp/temp.tmp')
        config['DEFAULT']['select_device'] = select_device
        config.write(open('tmp/temp.tmp', 'w'))

    @staticmethod
    def del_select_device():
        config = ConfigParser()
        config.read('tmp/temp.tmp')
        config['DEFAULT']['select_device'] = 'no'
        config.write(open('tmp/temp.tmp', 'w'))

    def cancel_btn_callback(self):
        temp = self.get_list_devices()[0]
        if temp:
            self.save_select_device(temp)
        self.__root.destroy()

    @staticmethod
    def get_current_device():
        config = ConfigParser()
        config.read('tmp/temp.tmp')
        if config.get('DEFAULT', 'select_device') != 'no':
            return config.get('DEFAULT', 'select_device')
        else:
            return None

device = devices()
