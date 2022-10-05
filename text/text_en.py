class text_tab_one:
    name = 'ps'
    refresh_btn = 'refresh'
    placeholder_text = 'enter package name'
    title = 'activity'


class text_tab_two:
    name = 'log'
    search_label = 'search'
    clear_btn = 'clear'
    stop_btn = 'stop'
    start_btn = 'start'
    activity_btn = 'ps'
    placeholder_text = 'pid:0000 || tag:library || re:[Ss]ocket || type:(w,d,i,v,e,f,s)'


class main_text:
    title = 'gui adb'
    warning_not_found_device = {
        'title': 'Warning',
        'text': 'No devices/emulators found'
    }
    error_close_subprocess = {
        'title': 'Error',
        'text': 'App cannot close the stream'
    }
    warning_stop_log_before_close_app = {
        'title': 'Error',
        'text': 'App cannot be closed while running log'
    }
    error_not_found_adb = {
        'title': 'Error',
        'text': 'App not found path to adb \nPlease pick folder with adb tools'
    }

class text_select_device:
    title = 'devices'
    label = 'Select device'
    ok_btn = 'ok'
    cancel_btn = 'cancel'


class text_menu_top:
    file = 'File'
    select_device = 'Select device'
    exit = 'Exit'
    about = 'About'
    settings = 'Settings'
    help = 'Help'
    performance = 'Performance'


class text_about_window:
    title = 'About'
    text = 'gui for adb logcat \n' \
           'Build on 2022 \n' \
           'Powered by ckotch47'
    github = 'https://github.com/ckotch47'


class text_settings:
    title = 'Settings'
    label_adb_select = 'Select folder with adb'
    change = 'Change'
    label_locale_select = 'Select language'
    label_information = 'Settings will be applied after application restart'
