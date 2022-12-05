from configparser import ConfigParser
from text.app_locale import app_locale
import module.cfg as cfg
cfg.check_config_ini()
config = ConfigParser()
config.read(cfg.get_path_config())
this_locale = config.get('DEFAULT', 'locale')

if this_locale == 'ru':
    from text.text_ru import *
else:
    from text.text_en import *


