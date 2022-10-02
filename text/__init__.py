from configparser import ConfigParser



config = ConfigParser()
config.read('config.ini')
this_locale = config.get('DEFAULT','locale')
print(this_locale)
if this_locale == 'ru':
    from text.text_ru import *
else:
    from text.text_en import *