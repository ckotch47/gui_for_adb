from tkinter import ttk, NO, CENTER, Text, PhotoImage
from module.mouse_btn import mouse_btn
from text.text_en import text_tab_two
import log_window.log_service as tab_two_service
from module.hotkey import hotkey
from activity.activity_gui import gui_tab_one


class tab_two_gui:
    def __init__(self):
        self.service = None
        self.m_btn = mouse_btn

    def tabTwo_init(self, tab):
        # config tab row, col
        tab.rowconfigure(1, weight=2)
        tab.columnconfigure(0, weight=1)

        # init table
        table = ttk.Treeview(tab, selectmode='extended')
        table['columns'] = ['TIME', 'PID', 'PPID', 'TYPE', 'LIBRARY', 'MESSAGE']

        # init msg box
        msg_text = Text(tab, padx=10, pady=10, height=8)
        # init service
        self.service = tab_two_service.service(table=table, text_box=msg_text)

        # add input
        input_find = ttk.Entry(tab)

        # add btn start
        start_btn = ttk.Button(tab, text=text_tab_two.start_btn, command=self.service.callback_start_btn)

        # add button to clear log
        clear_btn = ttk.Button(tab, text=text_tab_two.clear_btn, command=self.service.clear_logcat)

        # add button to stop log
        stop_btn = ttk.Button(tab, text=text_tab_two.stop_btn, command=self.service.stop_log)

        # add btn start
        activity_btn = ttk.Button(tab, text=text_tab_two.activity_btn, command=gui_tab_one.show)

        # config table head
        self.tabTwoTable_columnSettings(table)

        # add scrollbar
        y_scrollbarTwo = ttk.Scrollbar(tab, orient='vertical', command=table.yview)
        table.configure(yscrollcommand=y_scrollbarTwo.set)
        y_scrollbarTwo.configure(command=table.yview)

        # add message box

        # row 0
        input_find.grid(row=0, column=0, sticky="nwe", padx=(5, 0), ipady=0)
        start_btn.grid(row=0, column=1, sticky='ne', padx=(5, 0))
        clear_btn.grid(row=0, column=2, sticky='ne', padx=5)
        stop_btn.grid(row=0, column=3, sticky='ne', )
        activity_btn.grid(row=0, column=4, sticky='ne', padx=5)

        # row 1
        table.grid(row=1, column=0, padx=(5, 20), pady=5, sticky="nsew", rowspan=3, columnspan=5)

        # row 2
        msg_text.grid(row=4, column=0, sticky="nsew", padx=(3, 17), pady=5, rowspan=1, columnspan=5)

        # scrollbar
        y_scrollbarTwo.grid(row=1, column=4, sticky='nse', rowspan=4)

        # register service and bind

        self.service.bind_placeholder(input_find)

        table.bind(f'<{self.m_btn.double_left}>', self.service.on_double_click_row)
        table.bind(f'<{hotkey.copy}>', self.service.copy_value)
        table.bind(f'<{hotkey.stop}>', self.service.stop_log)
        tab.bind(f'<{hotkey.stop}>', self.service.stop_log)

        input_find.bind(f'<{hotkey.start}>', self.service.callback_start_btn)
        input_find.bind(f'<{hotkey.enter}>', self.service.callback_start_btn)
        input_find.bind(f'<{hotkey.select_all}>', self.service.select_all_input)

        msg_text.bind(f'<{hotkey.select_all}>', self.service.select_all_text)

        # self.service.main_log('','')

    @staticmethod
    def tabTwoTable_columnSettings(table):
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


gui_tab_two = tab_two_gui()
