import subprocess
from tkinter import messagebox

import pyperclip

from text.text_en import *


class service:
    def __init__(self, adb_path='', table=None):
        self.count = 0
        self.popen = None
        self.ADB_Path = adb_path
        self.table = table
        self.input_query = None

    # placeholder
    def clean_placeholder(self, *args):
        if self.input_query.get() == '' or self.input_query.get() == text_tab_one.placeholder_text:
            self.input_query.delete(0, 'end')
            self.input_query.config(foreground='black')

    def show_placeholder(self, *args):
        if self.input_query.get() == '':
            self.input_query.delete(0, 'end')
            self.input_query.config(foreground='gray')
            self.input_query.insert(0, text_tab_one.placeholder_text)

    def bind_placeholder(self, entry_search):
        self.input_query = entry_search
        self.input_query.delete(0, 'end')
        self.input_query.config(foreground='gray')
        self.input_query.insert(0, text_tab_one.placeholder_text)
        entry_search.bind("<FocusIn>", self.clean_placeholder)
        entry_search.bind("<FocusOut>", self.show_placeholder)

    # placeholder end
    def logcat_command(self):
        self.popen = subprocess.Popen([self.ADB_Path + "adb", "shell", "ps", "-Af"], shell=False,
                                      stdout=subprocess.PIPE)
        try:
            next(iter(self.popen.stdout.readline, b""))
        except StopIteration:
            messagebox.showwarning(
                main_text.warning_not_found_device.get('title'),
                main_text.warning_not_found_device.get('text')
            )
            return []
        return iter(self.popen.stdout.readline, b"")

    # format and adding proccess
    def logcat_result(self):
        iid_dict = []
        for line in self.logcat_command():
            i = self.return_value_from_string(line)
            if i[0].find('u0_') != -1 and i[1] not in iid_dict:
                iid_dict.append(i[1])
                self.count += 1
                self.table.insert(parent='', index='end', iid=i[1],
                                  values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], ''))
            else:
                continue

    @staticmethod
    def return_value_from_string(str_is):
        p = str(str_is).replace("b'", "").replace("'", "").split('\\')[0].split(' ')
        return [x for x in p if x]

    @staticmethod
    def clear_all(tree):
        tree.delete(*tree.get_children())

    def tabOneRefreshBTN(self):
        self.clear_all(self.table)
        self.logcat_result()

    def find_by_query(self, query):
        i = 0
        for child in self.table.get_children():
            i += 1
            if query in self.table.item(child).get("values")[7]:
                self.table.selection_set(child)
                self.table.yview_moveto((i - 1) / self.count)
        return True

    def register_for_find(self, input_t, tab):
        reg_find_by_query = tab.register(self.find_by_query)
        input_t.config(validate='key', validatecommand=(reg_find_by_query, '%P'))

    def copy_pid(self, event=None):
        temp_string = ''
        for i in self.table.selection():
            temp = self.table.item(i)['values']
            temp_string = str(temp[1])
            break
        pyperclip.copy(temp_string)

    @staticmethod
    def select_all_input(event=None):
        event.widget.select_range(0, 'end')
        event.widget.icursor('end')
