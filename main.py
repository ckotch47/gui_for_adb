import os
import subprocess
import sys
import threading
import tkinter
from tkinter import *
from tkinter import ttk
from adb_shell.auth.keygen import keygen
import showMassage
from showReq import showReq


def returnFrormatString(string):
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


def clear_all(tree):
    tree.delete(*tree.get_children())


def return_value_from_string(str_is):
    p = str(str_is).replace("b'", "").replace("'", "").split('\\')[0].split(' ')
    return [x for x in p if x]


class MyGUI:
    count = 0

    def __init__(self):
        self.SavedToken = None
        self.popup_tabOne = None
        self._tabOneRefresh = None
        self.popup_tabTwo = None
        self.popup = None
        self.popen = None
        self.inputPID = None
        self.inputRegx = None
        self.inputTag = None
        self.PIDVar = None
        self.th_pid = None
        self.popenPid = None
        self.tableTagOrRegx = None
        self.th_tag = None
        self.th_regx = None
        self.popenRegx = None
        self.popenTag = None
        self.RegxVar = None
        self.TagVar = None
        self.yscrollbar = None
        self.table = None
        self.input = None
        self.__tabTwo = None
        self.__tabOne = None
        self._root = None
        self._tabControl = None
        self.printlogTagBool = True
        self.printlogRegxBool = True
        self.printlogPid = True
        self._tabControlList = 0
        self._tabControlParam = 1

        if sys.platform == 'linux' or sys.platform == 'linux2':
            self.ADB_Path = os.getcwd() + '/linux_adb'
        elif sys.platform == 'darwin':
            self.ADB_Path = os.getcwd() + '/OSX_adb'
        elif sys.platform == 'win32':
            self.ADB_Path = os.getcwd() + '/win32_adb'

    def init_root(self):
        # self._root = Tk()
        self._root = Tk()

        self._root.title("GUI на Python")
        self._root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.popupInit_tabOne()
        self.popupInit_tabTwo()

    def on_closing(self):
        self.stoplog()
        os.system(self.ADB_Path + "/adb kill-server")
        sys.exit(0)

    def tabOneRefreshBTN(self):
        clear_all(self.table)
        self.logcatresult()

    def init_tab(self):
        self._tabControl = ttk.Notebook(self._root)

        self.__tabOne = ttk.Frame(self._tabControl)
        self.__tabTwo = ttk.Frame(self._tabControl)

        self._tabControl.add(self.__tabOne, text='list')
        self._tabControl.add(self.__tabTwo, text='param')

        self._tabControl.pack(expand=1, fill="both")

    def runMain(self):
        self.init_root()
        self.init_tab()

        self.tabOne_init()
        self.tabTwo_init()
        self._root.mainloop()

    def find_by_query(self, query):
        i = 0
        for child in self.table.get_children():
            i += 1
            if query in self.table.item(child).get("values")[7]:
                self.table.selection_set(child)
                self.table.yview_moveto((i - 1) / self.count)
        return True

    def OnDoubleClickOnTableOne(self, event):
        item = self.table.selection()[0]
        self._tabControl.select(self._tabControlParam)
        # self.PIDVar = item
        self.inputPID.delete(0, END)
        self.inputPID.insert(0, item)
        self.byPIDCallback()

    # -----------------------------TAB ONE ----------------------------------#
    def tabOne_init(self):
        self.__tabOne.rowconfigure(1, weight=2)
        self.__tabOne.columnconfigure(0, weight=1)

        # create list
        reg_find_by_query = self.__tabOne.register(self.find_by_query)
        self.input = ttk.Entry(self.__tabOne)
        self.input.config(validate='key', validatecommand=(reg_find_by_query, '%P'))
        self.input.grid(column=0, row=0, sticky=(N + W + E), padx=5, ipady=3)

        self._tabOneRefresh = ttk.Button(self.__tabOne, text='refresh', command=self.tabOneRefreshBTN)
        self._tabOneRefresh.grid(column=1, row=0, sticky=(N + W + E))

        self.table = ttk.Treeview(self.__tabOne, selectmode='extended')
        self.table['columns'] = ['UID', 'PID', 'PPID', 'C', 'STIME', 'TTY', 'TIME', 'CMD', 'SD']
        # bind double-click for item in table
        self.table.bind('<Double-1>', self.OnDoubleClickOnTableOne)
        self.tabOneTable_columnSettings()

        self.yscrollbar = ttk.Scrollbar(self.__tabOne, orient='vertical', command=self.table.yview)
        self.table.configure(yscrollcommand=self.yscrollbar.set)
        self.table.bind('<Button-3>', self.doPopup_tabOne)
        self.table.grid(padx=(5, 20), pady=5, sticky="nsew", columnspan=2)

        self.yscrollbar.grid(row=1, column=1, sticky='nse', rowspan=1)
        self.yscrollbar.configure(command=self.table.yview)

        self.logcatresult()

    def tabOneTable_columnSettings(self):
        # --column start
        self.table.column("#0", width=0, stretch=NO)
        self.table.column('UID', anchor=CENTER, width=80, stretch=NO)
        self.table.column('PID', anchor=CENTER, width=60, stretch=NO)
        self.table.column('PPID', width=0, stretch=NO)
        self.table.column('C', width=0, stretch=NO)
        self.table.column('STIME', width=0, stretch=NO)
        self.table.column('TTY', width=0, stretch=NO)
        self.table.column('TIME', anchor=CENTER, width=80, stretch=NO)
        self.table.column('CMD', anchor=W, width=360)
        self.table.column('SD', width=0, stretch=NO)
        # --column end
        self.table.heading("#0", text="", anchor=CENTER)
        self.table.heading("UID", text="UID", anchor=CENTER)
        self.table.heading("PID", text="PID", anchor=CENTER)
        self.table.heading("PPID", text="", anchor=CENTER)
        self.table.heading("C", text="", anchor=CENTER)
        self.table.heading("STIME", text="", anchor=CENTER)
        self.table.heading("TTY", text="", anchor=CENTER)
        self.table.heading("TIME", text="TIME", anchor=CENTER)
        self.table.heading("CMD", text="CMD", anchor=CENTER)
        self.table.heading("SD", text="", anchor=CENTER)

    # get proccess from linux_adb
    def logcatcommand(self):
        self.popen = subprocess.Popen([self.ADB_Path + "/adb", "shell", "ps", "-Af"], shell=False,
                                      stdout=subprocess.PIPE)
        return iter(self.popen.stdout.readline, b"")

    # format and adding proccess
    def logcatresult(self):
        iid_dict = []
        ix = 0
        for line in self.logcatcommand():
            if ix == 0:
                ix = 1
                continue
            i = return_value_from_string(line)
            if i[0].find('u0_') != -1 and i[1] not in iid_dict:
                iid_dict.append(i[1])
                self.count += 1
                self.table.insert(parent='', index='end', iid=i[1],
                                  values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], ''))
            else:
                continue

    # clear and format data from shell to list

    # -----------------------------TAB ONE ----------------------------------#

    # ----------------------------- POP UP ----------------------------------#
    def doPopup_tabOne(self, event):
        try:
            self.popup_tabOne.selection = self.table.set(self.table.identify_row(event.y))
            self.popup_tabOne.post(event.x_root, event.y_root)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self.popup_tabOne.grab_release()

    def popupInit_tabOne(self):
        self.popup_tabOne = tkinter.Menu(self.table, tearoff=0)
        self.popup_tabOne.add_command(command=self.your_copy_tabOne, label="Copy")
        self.popup_tabOne.add_command(command=self.popup_tabOne.grab_release, label="None")

    def your_copy_tabOne(self):
        self._root.clipboard_clear()
        temp_string = ''
        for i in self.table.selection():
            temp = self.table.item(i)['values']
            temp_string += str(temp[0]) + ' ' + str(temp[1]) + ' ' + str(temp[4]) + ' ' + '\t' + ' ' + str(
                temp[7]) + '\n'
        self._root.clipboard_append(temp_string)

    def doPopup_tabTwo(self, event):
        try:
            self.popup_tabTwo.selection = self.tableTagOrRegx.set(self.tableTagOrRegx.identify_row(event.y))
            self.popup_tabTwo.post(event.x_root, event.y_root)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self.popup_tabTwo.grab_release()

    def ShowMassageTabTwoMSG(self):
        try:
            textin = self.tableTagOrRegx.selection()
            textin = self.tableTagOrRegx.item(textin)['values'][-1].replace(':', '').lstrip().rstrip()
        except:
            textin = ''
        finally:
            showMassage.show(textin)

    def ShowMassageTabTwoReq(self):
        try:
            temp = self.tableTagOrRegx.selection()
            temp = self.tableTagOrRegx.item(temp)['values'][-1].lstrip().rstrip()
            temp = temp.split(' ')
        except:
            temp = ['', '']
        finally:
            showReq.show(method=temp[0], req=temp[1], token=self.SavedToken)

    def SaveToken(self):
        temp = self.tableTagOrRegx.selection()
        temp = self.tableTagOrRegx.item(temp)['values'][-1].lstrip().rstrip().split(' ')[2]
        self.SavedToken = temp

    def popupInit_tabTwo(self):
        self.popup_tabTwo = tkinter.Menu(self.tableTagOrRegx, tearoff=0)
        self.popup_tabTwo.add_command(command=self.your_copy_tabTwo, label="Copy")
        self.popup_tabTwo.add_command(command=self.ShowMassageTabTwoMSG, label="Show")
        self.popup_tabTwo.add_command(command=self.ShowMassageTabTwoReq, label="Req")
        self.popup_tabTwo.add_command(command=self.SaveToken, label="Set Bearer")
        self.popup_tabTwo.add_command(command=self.popup_tabTwo.grab_release, label="None")

    def your_copy_tabTwo(self):
        self._root.clipboard_clear()
        temp_string = ''
        for i in self.tableTagOrRegx.selection():
            temp = self.tableTagOrRegx.item(i)['values']
            print(temp)
            temp_string += str(temp[0]) + ' ' + str(temp[1]) + ' ' + str(temp[2]) + ' ' + \
                           str(temp[3]) + ' ' + str(temp[5]) + '\t' + '\n'
        self._root.clipboard_append(temp_string)

    # -----------------------------POP UP ----------------------------------#

    # -----------------------------TAB TWO ----------------------------------#
    # ------- callback for input START
    def byTagCallback(self, event):
        self.logTag(self.TagVar.get())

    def byRegxCallback(self, event):
        self.logRegx(self.RegxVar.get())

    def byPIDCallback(self, event=None):
        self.logPid(self.PIDVar.get())

    # ------- clear logcat history and table
    def clearHistory_logcat(self):
        os.system(self.ADB_Path + '/adb logcat -c')
        clear_all(self.tableTagOrRegx)

    # ------- clear logcat history and table END

    # ------- callback for input END
    # init tab and table start
    def tabTwo_init(self):
        self.__tabTwo.rowconfigure(3, weight=3)
        self.__tabTwo.columnconfigure(2, weight=3)
        self.TagVar = StringVar()
        self.RegxVar = StringVar()
        self.PIDVar = StringVar()

        labelTag = ttk.Label(self.__tabTwo, text='print by tag')
        labelTag.grid(row=0, column=0, sticky=N + E, columnspan=1, padx=5, pady=5)

        self.inputTag = ttk.Entry(self.__tabTwo, textvariable=self.TagVar)
        self.inputTag.bind('<Return>', self.byTagCallback)
        self.inputTag.grid(row=0, column=1, sticky=N + E, columnspan=1, padx=5, pady=5)

        labelRegx = ttk.Label(self.__tabTwo, text='print by regx')
        labelRegx.grid(row=0, column=3, sticky=N + W, columnspan=1, padx=5, pady=5)

        self.inputRegx = ttk.Entry(self.__tabTwo, textvariable=self.RegxVar)
        self.inputRegx.grid(row=0, column=4, sticky=N + W, columnspan=1, padx=5, pady=5)
        self.inputRegx.bind('<Return>', self.byRegxCallback)

        labelPID = ttk.Label(self.__tabTwo, text='print by PID')
        labelPID.grid(row=1, column=0, sticky=N + E, columnspan=1, padx=5, pady=5)

        self.inputPID = ttk.Entry(self.__tabTwo, textvariable=self.PIDVar)
        self.inputPID.grid(row=1, column=1, sticky=N + E, columnspan=1, padx=5, pady=5)
        self.inputPID.bind('<Return>', self.byPIDCallback)

        printBtn = ttk.Button(self.__tabTwo, text='clear', command=self.clearHistory_logcat)
        printBtn.grid(row=0, column=5, sticky=N + E, columnspan=1, pady=5, padx=5)

        closeBtn = ttk.Button(self.__tabTwo, text='stop', command=self.stoplog)
        closeBtn.grid(row=1, column=5, sticky=N + E, columnspan=1, pady=5, padx=5)

        # label_h = ttk.Label(self.__tabTwo, text='[Ss]ocket ?')
        # label_h.grid(row=1, column=4, sticky=N + W)
        self.init_tableTwo()

    def init_tableTwo(self):
        self.tableTagOrRegx = ttk.Treeview(self.__tabTwo, selectmode='extended')
        self.tableTagOrRegx['columns'] = ['TIME', 'PID', 'PPID', 'TYPE', 'LIBRARY', 'MESSAGE']
        self.tableTagOrRegx.column("#0", width=0, stretch=NO)
        self.tableTagOrRegx.column('TIME', anchor=CENTER, width=100, stretch=NO)
        self.tableTagOrRegx.column('PID', anchor=CENTER, width=50, stretch=NO)
        self.tableTagOrRegx.column('PPID', anchor=CENTER, width=50, stretch=NO)
        self.tableTagOrRegx.column('TYPE', anchor=CENTER, width=40, stretch=NO)
        self.tableTagOrRegx.column('LIBRARY', anchor=CENTER, width=150, stretch=NO)
        self.tableTagOrRegx.column('MESSAGE', anchor='w', width=80, )

        self.table.heading("#0", text="", anchor=CENTER)

        self.tableTagOrRegx.heading("#0", text="", anchor=CENTER)
        self.tableTagOrRegx.heading('TIME', text="TIME", anchor=CENTER)
        self.tableTagOrRegx.heading('PID', text="PID", anchor=CENTER)
        self.tableTagOrRegx.heading('PPID', text="PPID", anchor=CENTER)
        self.tableTagOrRegx.heading('TYPE', text="TYPE", anchor=CENTER)
        self.tableTagOrRegx.heading('LIBRARY', text="LIBRARY", anchor=CENTER)
        self.tableTagOrRegx.heading('MESSAGE', text="MESSAGE", anchor=CENTER)

        self.tableTagOrRegx.bind('<Button-3>', self.doPopup_tabTwo)
        self.tableTagOrRegx.bind('<Double-1>', self.OnDoubleClickOnTableTwo)

        self.yscrollbarTwo = ttk.Scrollbar(self.__tabTwo, orient='vertical', command=self.tableTagOrRegx.yview)
        self.tableTagOrRegx.configure(yscrollcommand=self.yscrollbarTwo.set)

        self.yscrollbarTwo.grid(row=3, column=7, sticky='nse', rowspan=1)
        self.yscrollbarTwo.configure(command=self.tableTagOrRegx.yview)

        self.tableTagOrRegx.grid(padx=5, pady=5, sticky="nsew", row=3, columnspan=6)

    def OnDoubleClickOnTableTwo(self, event):
        item = self.tableTagOrRegx.selection()[0]
        print(self.tableTagOrRegx.item(item))

    # init tab and table end

    # ----- logging by tag
    def logTag(self, param):
        clear_all(self.tableTagOrRegx)
        self.stoplog()
        self.popenTag = subprocess.Popen([self.ADB_Path + "/adb", "logcat", "-s", param], shell=False,
                                         stdout=subprocess.PIPE)
        self.printlogTagBool = True
        self.th_tag = threading.Thread(target=self.printlogTag)
        self.th_tag.start()

    def printlogTag(self):
        temp = iter(self.popenTag.stdout.readline, b"")
        for i in temp:
            if self.printlogTagBool:
                temp_str = returnFrormatString(i)
                if temp_str:
                    self.tableTagOrRegx.insert(parent='', index='end',
                                               values=(temp_str[1], temp_str[2], temp_str[3],
                                                       temp_str[4], temp_str[5], temp_str[6]))
                    self.tableTagOrRegx.yview_moveto(1)

    # ----- logging by tag

    # ----- logging by regx
    def logRegx(self, param):
        clear_all(self.tableTagOrRegx)
        self.stoplog()
        self.popenRegx = subprocess.Popen([self.ADB_Path + "/adb", "logcat", "-e", param], shell=False,
                                          stdout=subprocess.PIPE)
        self.printlogRegxBool = True
        self.th_regx = threading.Thread(target=self.printlogRegx)
        self.th_regx.start()

    def printlogRegx(self):
        temp = iter(self.popenRegx.stdout.readline, b"")
        for i in temp:
            if self.printlogRegx:
                temp_str = returnFrormatString(i)
                if temp_str:
                    self.tableTagOrRegx.insert(parent='', index='end',
                                               values=(temp_str[1], temp_str[2], temp_str[3],
                                                       temp_str[4], temp_str[5], temp_str[6]))
                    self.tableTagOrRegx.yview_moveto(1)

    # ----- logging by regx

    # ----- logging by PID
    def logPid(self, param):
        clear_all(self.tableTagOrRegx)
        self.stoplog()
        self.popenPid = subprocess.Popen([self.ADB_Path + "/adb", "logcat", "--pid=" + param], shell=False,
                                         stdout=subprocess.PIPE)
        self.printlogPid = True
        self.th_pid = threading.Thread(target=self.printLogPid)
        self.th_pid.start()

    def printLogPid(self):
        temp = iter(self.popenPid.stdout.readline, b"")
        for i in temp:
            if self.printlogPid:
                temp_str = returnFrormatString(i)
                if temp_str:
                    self.tableTagOrRegx.insert(parent='', index='end',
                                               values=(temp_str[1], temp_str[2], temp_str[3],
                                                       temp_str[4], temp_str[5], temp_str[6]))
                    self.tableTagOrRegx.yview_moveto(1)

    # ----- logging by PID

    # stop logging
    def stoplog(self):
        if self.popenTag:
            self.printlogTagBool = False
            try:
                os.kill(self.popenTag.pid, 1)
            except ():
                print('fail kill')
            self.th_tag.join(timeout=1)

        if self.popenRegx:
            self.printlogRegxBool = False
            try:
                os.kill(self.popenRegx.pid, 1)
            except ():
                print('fail kill')
            self.th_regx.join(timeout=1)

        if self.popenPid:
            self.printlogPid = False
            try:
                os.kill(self.popenPid.pid, 1)
            except ():
                print('fail kill')
            self.th_pid.join(timeout=1)
        os.kill(self.popen.pid, 0)
    # -----------------------------TAB TWO ----------------------------------#


myGUI = MyGUI()
if __name__ == "__main__":
    keygen(os.getcwd() + '/adbkey')
    myGUI.runMain()
