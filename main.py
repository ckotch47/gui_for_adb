
from gui.main import gui
import module.cfg as cfg
if __name__ == "__main__":
    cfg.check_config_ini()
    gui.init_root()
