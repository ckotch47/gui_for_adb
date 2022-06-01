from tkinter import Text, Toplevel


def show(textin = 'massage'):
    __MainWindow = Toplevel()
    __MainWindow.geometry('900x150')
    __MainWindow.wm_title('message')
    text = Text(__MainWindow, padx=10, pady=10)
    text.insert(1.0, textin)
    text.pack(expand=1, fill='both', pady=10, padx=10)
