"""
log window
"""
from tkinter import ttk, NO, CENTER, Text, Variable, Listbox

from module.mouse_btn import mouse_btn
from text import *
from module.hotkey import hotkey
from activity.activiti_gui import activiti_gui

import log_window.log_service as tab_two_service


class LogGui:
    """
    class for setting and show log window
    """

    def __init__(self):
        """
        init class
        """
        self.tab = None
        self.service = None
        self.m_btn = mouse_btn
        self.table = None
        self.msg_text = None

    def log_gui_init(self, tab):
        """
        initialization function
        """
        self.tab = tab
        # config tab row, col
        self.tab.rowconfigure(1, weight=2)
        self.tab.columnconfigure(1, weight=1)

        # row 1
        self.setting_table()

        # row 2
        self.setting_msg_text()

        # init service
        self.service = tab_two_service.LogGuiService(table=self.table, text_box=self.msg_text)

        self.setting_devices_list()

        # row 0
        self.settings_input()
        self.setting_start_btn()
        self.settings_clear_btn()
        self.settings_stop_btn()
        self.settings_activiti_btn()

        self.setting_hotkey()

    # setting block start
    def settings_input(self):
        """
        initialization input
        """
        input_find = ttk.Entry(self.tab, width=70)
        input_find.grid(row=0, column=1, sticky="nwe", padx=(5, 0), ipady=0, pady=5, columnspan=2)
        # register service and bind
        self.service.bind_placeholder(input_find)

        # bind hotkey
        input_find.bind(f'<{hotkey.start}>', self.service.callback_start_btn)
        input_find.bind(f'<{hotkey.enter}>', self.service.callback_start_btn)
        input_find.bind(f'<{hotkey.select_all}>', self.service.select_all_input)

    def setting_start_btn(self):
        """
        init start btn
        """
        # add btn start
        start_btn = ttk.Button(self.tab, text=LogText.start_btn, command=self.service.callback_start_btn)
        start_btn.grid(row=0, column=3, sticky='nwe', padx=(5, 0), pady=5)

    def settings_clear_btn(self):
        """
        init clear btn
        """
        clear_btn = ttk.Button(self.tab, text=LogText.clear_btn, command=self.service.clear_logcat)
        clear_btn.grid(row=0, column=4, sticky='nwe', padx=5, pady=5)

    def settings_stop_btn(self):
        """
        init stop btn
        """
        stop_btn = ttk.Button(self.tab, text=LogText.stop_btn, command=self.service.stop_log)
        stop_btn.grid(row=0, column=5, sticky='nwe', pady=5)

    def settings_activiti_btn(self):
        """
        init ps btn
        """
        activity_btn = ttk.Button(self.tab, text=LogText.activity_btn, command=activiti_gui.show)
        activity_btn.grid(row=0, column=6, sticky='nwe', padx=5, pady=5)

    def setting_devices_list(self):
        """
        init and get devices list
        """
        languages = ["device1", "device2", "device", "device"]
        languages_var = Variable(value=languages)
        languages_listbox = Listbox(self.tab, listvariable=languages_var, width=30)
        languages_listbox.grid(row=0, column=0, sticky="nsew", padx=(5, 0), ipady=0, pady=5, rowspan=5)

    def setting_table(self):
        """
        init table
        """
        self.table = ttk.Treeview(self.tab, selectmode='extended')
        self.table['columns'] = ['TIME', 'PID', 'PPID', 'TYPE', 'LIBRARY', 'MESSAGE']

        # config table head
        self.log_gui_table_column_settings(self.table)

        # add scrollbar
        y_scrollbar_log = ttk.Scrollbar(self.tab, orient='vertical', command=self.table.yview)
        self.table.configure(yscrollcommand=y_scrollbar_log.set)
        y_scrollbar_log.configure(command=self.table.yview)

        # scrollbar
        y_scrollbar_log.grid(row=1, column=6, sticky='nse', rowspan=4)

        # row 1
        self.table.grid(row=1, column=1, padx=(5, 20), pady=5, sticky="nsew", rowspan=3, columnspan=6)

    def setting_msg_text(self):
        """
        init text box for message
        """
        self.msg_text = Text(self.tab, padx=10, pady=10, height=8)
        self.msg_text.grid(row=4, column=1, sticky="nsew", padx=(5, 20), pady=5, rowspan=1, columnspan=6)

    def setting_hotkey(self):
        """
        bind hotkey
        """
        self.table.bind(f'<{self.m_btn.double_left}>', self.service.on_double_click_row)
        self.table.bind(f'<{hotkey.copy}>', self.service.copy_value)
        self.table.bind(f'<{hotkey.stop}>', self.service.stop_log)

        self.tab.bind(f'<{hotkey.stop}>', self.service.stop_log)

        self.msg_text.bind(f'<{hotkey.select_all}>', self.service.select_all_text)
    # setting block end

    @staticmethod
    def log_gui_table_column_settings(table):
        """
        setting table header
        """
        table.column("#0", width=0, stretch=NO)
        table.column('TIME', anchor=CENTER, width=100, stretch=NO)
        table.column('PID', anchor=CENTER, width=50, stretch=NO)
        table.column('PPID', anchor=CENTER, width=50, stretch=NO)
        table.column('TYPE', anchor=CENTER, width=40, stretch=NO)
        table.column('LIBRARY', anchor='w', width=150, stretch=NO)
        table.column('MESSAGE', anchor='w', width=80, )

        table.heading("#0", text="", anchor=CENTER)

        table.heading("#0", text="", anchor=CENTER)
        table.heading('TIME', text="TIME", anchor=CENTER)
        table.heading('PID', text="PID", anchor=CENTER)
        table.heading('PPID', text="PPID", anchor=CENTER)
        table.heading('TYPE', text="TYPE", anchor=CENTER)
        table.heading('LIBRARY', text="LIBRARY", anchor=CENTER)
        table.heading('MESSAGE', text="MESSAGE", anchor=CENTER)


log_gui = LogGui()
