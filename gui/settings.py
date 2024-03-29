"""
setting window gui
"""
from tkinter import *
from tkinter import filedialog
from text import *

config = ConfigParser()


def show():
    """
    show gui for settings
    """
    _root_settings = Toplevel()

    _root_settings.geometry("500x200")

    frame_info = Frame(_root_settings)

    frame_info.pack(expand=1, padx=20, pady=(20, 0), fill='x', anchor='n')

    Label(frame_info, text=SettingText.label_information).pack()

    frame_adb = Frame(_root_settings)
    frame_adb.pack(expand=1, padx=20, pady=20, fill='x', anchor='n')
    Label(frame_adb, text=SettingText.label_adb_select).pack(side='left')
    Button(frame_adb, text=SettingText.change, command=select_folder).pack(side='right')

    config.read(cfg.get_path_config())
    temp_locale = config.get('DEFAULT', 'locale')

    locale_var = StringVar()
    if temp_locale in app_locale:
        locale_var.set(temp_locale)
    else:
        locale_var.set(app_locale[0])

    # Create Dropdown menu
    frame_locale = Frame(_root_settings)
    frame_locale.pack(expand=1, padx=20, pady=0, fill='x', anchor='n')
    Label(frame_locale, text=SettingText.label_locale_select).pack(side='left')
    OptionMenu(frame_locale, locale_var, *app_locale, command=select_locale).pack(side='right')

    _root_settings.mainloop()


def select_locale(event):
    """
    save language
    """
    if event in app_locale:
        config.read(cfg.get_path_config())
        config['DEFAULT']['locale'] = event
        config.write(open(cfg.get_path_config(), 'w'))


def select_folder():
    """
    save folder selected
    """
    folder_selected = filedialog.askdirectory() + '/'

    config.read(cfg.get_path_config())
    config['DEFAULT']['adb_path'] = folder_selected
    config.write(open(cfg.get_path_config(), 'w'))
