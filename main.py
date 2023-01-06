import module.cfg as cfg
from gui.main import gui

if __name__ == "__main__":
    cfg.check_config_ini()
    gui.init_root()
