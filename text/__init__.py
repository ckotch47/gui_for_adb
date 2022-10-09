from configparser import ConfigParser
from text.app_locale import app_locale

config = ConfigParser()
config.read('config.ini')
this_locale = config.get('DEFAULT', 'locale')

if this_locale == 'ru':
    from text.text_ru import *
else:
    from text.text_en import *


