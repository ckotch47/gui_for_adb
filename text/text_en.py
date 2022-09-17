class text_tab_one:
    name = 'tab one'
    refresh_btn = 'refresh'
    placeholder_text = 'enter package name'

class text_tab_two:
    name = 'tab two'
    search_label = 'search'
    clear_btn = 'clear'
    stop_btn = 'stop'
    start_btn = 'start'
    placeholder_text = 'pid:0000 || tag:library || re:[Ss]ocket || all or * for all message'


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