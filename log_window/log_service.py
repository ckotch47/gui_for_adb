"""
service for logGui window
"""
import os
import subprocess
import threading
import pyperclip

from tkinter import messagebox, SEL, INSERT

import module.lock as app_lock

from text import *
from module.check_device import device


class LogGuiService:
    """
    service class
    """

    def __init__(self, table=None, text_box=None):
        """
        function for init class
        """
        self.ADB_Path = device.get_adb_path()

        self.input_find = None
        self.table = table
        self.text_box = text_box

        self.subprocess_is_open = False
        self.subprocess_val = None

        self.print_log = False
        self.thread = None

    def clear_logcat(self):
        """
        clear all log on device
        """
        self.stop_log()
        if device.check_device():
            device_sh = ['-s', f'{device.get_current_device()}'] if device.get_current_device() else ['', '']
            os.system(self.ADB_Path + f'adb {device_sh[0]} {device_sh[1]} logcat -c')
            self.clear_all(self.table)

    # placeholder for search
    def clean_placeholder(self, *args):
        """
        clear placeholder where user focusin input
        """
        if self.input_find.get() == '' or self.input_find.get() == LogText.placeholder_text:
            self.input_find.delete(0, 'end')
            self.input_find.config(foreground='black')

    def show_placeholder(self, *args):
        """
        print tip in input
        """
        if self.input_find.get() == '':
            self.input_find.delete(0, 'end')
            self.input_find.config(foreground='gray')
            self.input_find.insert(0, LogText.placeholder_text)

    def bind_placeholder(self, entry_search):
        """
        bind state focus in and focus out on input
        """
        self.input_find = entry_search
        self.input_find.delete(0, 'end')
        self.input_find.config(foreground='gray')
        self.input_find.insert(0, LogText.placeholder_text)
        entry_search.bind("<FocusIn>", self.clean_placeholder)
        entry_search.bind("<FocusOut>", self.show_placeholder)

    # placeholder for search end

    # callback for entry
    def callback_start_btn(self, event=None):
        """
        before start log. Split str where enter user
        """
        temp: str = self.input_find.get()
        if device.check_device():
            if temp != LogText.placeholder_text:
                if temp.find('pid:') == 0 and temp.find('tag:') == -1 and temp.find('re:') == -1 and temp.find(
                        'type:') == -1:
                    tmp = temp.replace('pid:', '')
                    self.main_log(f'--pid={tmp}')
                elif temp.find('pid:') == -1 and temp.find('tag:') == 0 and temp.find('re:') == -1 and temp.find(
                        'type:') == -1:
                    tmp = temp.replace('tag:', '')
                    self.main_log('-s', tmp)
                elif temp.find('pid:') == -1 and temp.find('tag:') == -1 and temp.find('re:') == 0 and temp.find(
                        'type:') == -1:
                    tmp = temp.replace('re:', '')
                    self.main_log('-e', tmp)
                elif temp == 'all' or temp == '*' or temp == '':
                    self.main_log('', '')
                elif temp.find('pid:') == -1 and temp.find('tag:') == -1 and temp.find('re:') == -1 and temp.find(
                        'type:') == 0:
                    tmp = temp.replace('type:', '')
                    self.main_log(f'*:{tmp.upper()}')
            else:
                self.main_log('', '')

    # print log
    def main_log(self, method='', param=''):
        """
        get log from device
        """
        self.stop_log()
        device_sh = ['-s', f'{device.get_current_device()}'] if device.get_current_device() else ['', '']
        self.subprocess_val = subprocess.Popen([self.ADB_Path + "adb", device_sh[0], device_sh[1], "logcat",
                                                f'{method}', f'{param}'], shell=False,
                                               stdout=subprocess.PIPE)
        self.print_log = True
        app_lock.lock_activate()  # loc app
        self.thread = threading.Thread(target=self.print_log_func)
        self.thread.start()

    def print_log_func(self):
        """
        add row into table
        """
        self.clear_all(self.table)
        temp = iter(self.subprocess_val.stdout.readline, b"")
        for i in temp:
            if self.print_log:
                temp_str = self.return_format_string(i)
                if temp_str:
                    self.table.insert(parent='', index='end',
                                      values=(temp_str[1], temp_str[2], temp_str[3],
                                              temp_str[4], temp_str[5], temp_str[6]))
                    self.table.yview_moveto(1)
        temp=None

    # print log end

    # stop all log
    def stop_log(self, event=None):
        """
        function where stop all process logging
        """
        if self.print_log:
            self.print_log = False
            try:
                os.kill(self.subprocess_val.pid, 1)
            except:
                messagebox.showwarning(
                    MainText.error_close_subprocess.get('title'),
                    MainText.error_close_subprocess.get('text')
                )
            self.thread.join(timeout=1)
            app_lock.lock_deactivate()

    # stop all log end

    # insert text into msg box
    def on_double_click_row(self, event):
        """
        activate double click on table row -> add message text into msg_text
        """
        item = self.table.selection()[0]
        tmp_text = self.table.item(item)['values'][-1]
        self.text_box.delete(1.0, 'end')
        self.text_box.insert(1.0, tmp_text)

    def copy_value(self, event):
        """
        copy message value into clip
        """
        temp_string = ''
        for i in self.table.selection():
            temp = self.table.item(i)['values']
            temp_string += str(temp[0]) + ' ' + str(temp[1]) + ' ' + str(temp[2]) + ' ' + \
                           str(temp[3]) + ' ' + str(temp[5]) + '\n'
        pyperclip.copy(temp_string)

    @staticmethod
    def select_all_input(event=None):
        """
        select all into input
        """
        event.widget.select_range(0, 'end')
        event.widget.icursor('end')

    @staticmethod
    def select_all_text(event=None):
        """
        select all text into msg_text
        """
        event.widget.tag_add(SEL, "1.0", 'end')
        event.widget.mark_set(INSERT, "1.0")
        event.widget.see(INSERT)

    @staticmethod
    def return_format_string(string):
        """
        slit string to dict for table
        """
        temp = str(string).replace("b'", "").replace("'", "").split('\\')[0].split(' ')
        for i in temp:
            if i == ' ' or i == '' or i == ',':
                temp.remove(i)

        if len(temp) > 6:
            i = 6
            string = ''
            while i < len(temp):
                string += temp[i] + ' '
                i += 1
            temp[6] = string.replace(':', '', 1)
            return temp
        else:
            return False

    @staticmethod
    def clear_all(tree):
        """
        clear all row in log table
        """
        tree.delete(*tree.get_children())
