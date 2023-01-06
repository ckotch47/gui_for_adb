"""
ru text locale
"""


class ActivitiText:
    name = 'ps'
    refresh_btn = 'Обновить'
    placeholder_text = 'Имя пакета'
    title = 'Процессы'


class LogText:
    name = 'Лог'
    search_label = 'Поиск'
    clear_btn = 'Очистить'
    stop_btn = 'Стоп'
    start_btn = 'Старт'
    activity_btn = 'ps'
    placeholder_text = 'pid:0000 || tag:library || re:[Ss]ocket || type:(w,d,i,v,e,f,s)'


class MainText:
    title = 'gui adb'
    warning_not_found_device = {
        'title': 'Предупреждение',
        'text': 'Устройство не найдено'
    }
    error_close_subprocess = {
        'title': 'Ошибка',
        'text': 'Что-то пошло не так, приложение не может закрыть поток'
    }
    warning_stop_log_before_close_app = {
        'title': 'Ошибка',
        'text': 'Остановите запись логов для закрытия приложения'
    }
    error_not_found_adb = {
        'title': 'Ошибка',
        'text': 'Приложение не может найти путь к adb \nУкажите путь к папке с adb tools\n'
                'Или скачайте с https://developer.android.com/studio/releases/platform-tools'
    }


class SelectDeviceText:
    title = 'Устройства'
    label = 'Выберите устройств'
    ok_btn = 'Ок'
    cancel_btn = 'Отмена'


class MenuTopText:
    file = 'Файл'
    select_device = 'Выбрать устройств'
    exit = 'Выход'
    about = 'О программе'
    settings = 'Настройки'
    help = 'Помощь'
    performance = 'Настройки'


class AboutGuiText:
    title = 'О программе'
    text = 'gui for adb logcat \n' \
           'Build on 2022 \n' \
           'Powered by ckotch47'
    github = 'https://github.com/ckotch47'


class SettingText:
    title = 'Настройки'
    label_adb_select = 'Укажите путь ADB'
    change = 'Выбрать'
    label_locale_select = 'Укажите язык'
    label_information = 'Настройки применятся после перезагрузки приложения'
