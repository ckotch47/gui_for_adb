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
