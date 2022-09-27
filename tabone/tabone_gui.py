from tkinter import ttk, NO, CENTER, W
from module.mouse_btn import mouse_btn
from text.text_en import text_tab_one
import tabone.tabone_service as tab_one_service
from module.hotkey import hotkey

class tab_one_gui:
    def __init__(self):
        self.service = None
        self.m_btn = mouse_btn

    def tabOne_init(self, tab):
        tab.rowconfigure(1, weight=2)
        tab.columnconfigure(0, weight=1)

        # add input for search
        input_query = ttk.Entry(tab)

        # init table
        table = ttk.Treeview(tab, selectmode='extended')
        table['columns'] = ['UID', 'PID', 'PPID', 'C', 'STIME', 'TTY', 'TIME', 'CMD', 'SD']

        # init service
        self.service = tab_one_service.service(table=table)

        # add refresh button
        refresh_btn = ttk.Button(tab, text=text_tab_one.refresh_btn, command=self.service.tabOneRefreshBTN)

        # config table head

        # config scrollbar
        y_scrollbar = ttk.Scrollbar(tab, orient='vertical', command=table.yview)
        table.configure(yscrollcommand=y_scrollbar.set)

        # add scrollbar
        y_scrollbar.configure(command=table.yview)

        # add gui element on tab
        input_query.grid(row=0, column=0, sticky="nwe", padx=5)
        refresh_btn.grid(row=0, column=1, sticky='nwe')
        table.grid(row=1, column=0, padx=(5, 20), pady=5, sticky="nsew", columnspan=2)
        y_scrollbar.grid(row=1, column=1, sticky='nse', rowspan=1)

        # register service and bind
        self.tabOneTable_columnSettings(table)
        self.service.register_for_find(input_query, tab)
        self.service.logcat_result()

        table.bind(f'<{hotkey.copy}>', self.service.copy_pid)
        self.service.bind_placeholder(input_query)

        input_query.bind(f'<{hotkey.select_all}>', self.service.select_all_input)

    @staticmethod
    def tabOneTable_columnSettings(table):
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


gui_tab_one = tab_one_gui()
