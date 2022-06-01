from tkinter import Text, END, Toplevel, ttk, StringVar
import requests


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class ShowReq:
    def __init__(self):
        self.dataText = None
        self.textbox1 = None
        self.label = None
        self.textbox = None
        self.btn_send = None
        self.comboBox = None
        self.responseText = None
        self.select_method = None
        self.req = None
        self.auth = None

    def show(self, req='http://127.0.0.0/api', method='GET', token=None):
        __MainWindow = Toplevel()
        __MainWindow.geometry('900x350')
        __MainWindow.wm_title('request')
        __MainWindow.rowconfigure(3, weight=3)
        __MainWindow.columnconfigure(1, weight=3)

        self.select_method = StringVar()
        self.auth = StringVar()
        self.req = StringVar()



        self.comboBox = ttk.Combobox(__MainWindow, textvariable=self.select_method, width=8)
        self.comboBox['value'] = ['GET', 'POST', 'PUT', 'DELETE']
        self.comboBox['state'] = 'readonly'
        self.comboBox.grid(padx=10, pady=1, row=0, column=0, sticky='we')

        self.textbox = ttk.Entry(__MainWindow, textvariable=self.req)
        self.textbox.insert(0, req)
        self.textbox.grid(padx=10, pady=1, row=0, column=1, columnspan=1, sticky='we')

        self.btn_send = ttk.Button(__MainWindow, text='send', command=self.send)
        self.btn_send.grid(padx=10, pady=1, row=0, column=2)

        self.label = ttk.Label(__MainWindow, text='bearer')
        self.label.grid(padx=10, pady=1, row=1, column=0, columnspan=1, rowspan=1, sticky='wen')

        self.textbox1 = ttk.Entry(__MainWindow, textvariable=self.auth)
        self.textbox1.grid(padx=10, pady=3, row=1, column=1, columnspan=1, rowspan=1, sticky='wen')

        self.dataText = Text(__MainWindow, height=10)
        self.dataText.insert(1.0, 'data - json')
        self.dataText.grid(padx=10, pady=5, row=2, column=0, columnspan=3, rowspan=1, sticky='nsew')

        self.responseText = Text(__MainWindow, height=10)
        self.responseText.insert(1.0, 'response')
        self.responseText.grid(padx=10, pady=5, row=3, column=0, columnspan=3, rowspan=4, sticky='nsew')

        if token is not None:
            self.auth = token
            self.textbox1.delete(0, END)
            self.textbox1.insert(0, token)

        if method == 'GET':
            self.comboBox.current(0)
        elif method == 'POST':
            self.comboBox.current(1)
        elif method == 'PUT':
            self.comboBox.current(2)
        elif method == 'DELETE':
            self.comboBox.current(3)

    def send(self):
        methods = self.select_method.get()
        url = self.req.get()
        auth = self.auth.get()
        if methods == 'GET':
            try:
                temp = requests.get(url, auth=BearerAuth(auth)).json()
                str(temp[0]).replace('{', '{\n')
                str(temp[0]).replace('}', '}\n')
                str(temp[0]).replace(',', ',\n')
                self.responseText.delete(1.0, END)
                self.responseText.insert(1.0, temp)
            except:
                temp = requests.get(url, auth=BearerAuth(auth))
                self.responseText.delete(1.0, END)
                self.responseText.insert(1.0, temp.text)
        # elif methods == 'POST':
        #     temp = requests.post(self.req, headers={"Authorization" : self.auth.get()}).json()
        # elif methods == 'PUT':
        #     temp = requests.put(self.req, headers={"Authorization" : self.auth.get()}).json()
        # elif methods == 'DELETE':
        #     temp = requests.delete(self.req, headers={"Authorization" : self.auth.get()}).json()


showReq = ShowReq()
