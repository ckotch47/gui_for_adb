"""
    init window for activiti process monitor
"""
from tkinter import ttk, NO, CENTER, W, Toplevel, Frame

from module.mouse_btn import mouse_btn
from text import *
from module.hotkey import hotkey

import activity.activiti_service as activiti_service


class ActivitiGui:
    """
    class for activiti window
    """
    def __init__(self):
        """
        init class
        """
        self.tab = None
        self.service = None
        self.m_btn = mouse_btn

    def activiti_gui_init(self, tab):
        """
        init gui window
        """
        self.tab = tab
        self.tab.rowconfigure(1, weight=2)
        self.tab.columnconfigure(0, weight=1)

        self.settings_table()

        # add input and btn
        self.settings_input()
        self.settings_refresh_btn()

    # setting block start
    def settings_input(self):
        """
        add input for search
        """
        input_query = ttk.Entry(self.tab)
        input_query.grid(row=0, column=0, sticky="nwe", padx=5, ipady=0, pady=5)
        self.service.register_for_find(input_query, self.tab)
        self.service.bind_placeholder(input_query)
        input_query.bind(f'<{hotkey.select_all}>', self.service.select_all_input)

    def settings_refresh_btn(self):
        """
        add refresh button
        """
        refresh_btn = ttk.Button(self.tab, text=text_tab_one.refresh_btn, command=self.service.activiti_gui_refresh_btn)
        refresh_btn.grid(row=0, column=1, sticky='nwe', padx=5, pady=5)

    def settings_table(self):
        """
        add table and scrollbar
        """
        # init table
        table = ttk.Treeview(self.tab, selectmode='extended')
        table['columns'] = ['UID', 'PID', 'PPID', 'C', 'STIME', 'TTY', 'TIME', 'CMD', 'SD']

        # init service
        self.service = activiti_service.ActivitiService(table=table)

        # config scrollbar
        y_scrollbar = ttk.Scrollbar(self.tab, orient='vertical', command=table.yview)
        table.configure(yscrollcommand=y_scrollbar.set)

        # add scrollbar
        y_scrollbar.configure(command=table.yview)

        # add table and scrollbar
        table.grid(row=1, column=0, padx=(5, 20), pady=5, sticky="nsew", columnspan=2)
        y_scrollbar.grid(row=1, column=1, sticky='nse', rowspan=1)

        # register service and bind
        self.activiti_gui_column_settings(table)

        # get first's result
        self.service.logcat_result()

        # bind ctrl+c to table
        table.bind(f'<{hotkey.copy}>', self.service.copy_pid)

    # setting block end

    def show(self):
        """
        show gui
        """
        _root_activiti = Toplevel()
        _root_activiti.geometry('900x350')
        _root_activiti.wm_title(text_tab_one.title)
        frame = Frame(_root_activiti)
        self.activiti_gui_init(frame)
        frame.pack(expand=1, fill='both')

    @staticmethod
    def activiti_gui_column_settings(table):
        """
        setting column table
        """
        # --column start
        table.column("#0", width=0, stretch=NO)
        table.column('UID', anchor=CENTER, width=80, stretch=NO)
        table.column('PID', anchor=CENTER, width=60, stretch=NO)
        table.column('PPID', width=0, stretch=NO)
        table.column('C', width=0, stretch=NO)
        table.column('STIME', width=0, stretch=NO)
        table.column('TTY', width=0, stretch=NO)
        table.column('TIME', anchor='w', width=80, stretch=NO)
        table.column('CMD', anchor=W, width=360)
        table.column('SD', width=0, stretch=NO)
        # --column end
        table.heading("#0", text="", anchor=CENTER)
        table.heading("UID", text="UID", anchor=CENTER)
        table.heading("PID", text="PID", anchor=CENTER)
        table.heading("PPID", text="", anchor=CENTER)
        table.heading("C", text="", anchor=CENTER)
        table.heading("STIME", text="", anchor=CENTER)
        table.heading("TTY", text="", anchor=CENTER)
        table.heading("TIME", text="TIME", anchor=CENTER)
        table.heading("CMD", text="CMD", anchor=CENTER)
        table.heading("SD", text="", anchor=CENTER)


# for import activiti_gui
activiti_gui = ActivitiGui()
