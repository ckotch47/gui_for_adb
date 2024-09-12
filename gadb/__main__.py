import gadb.module.cfg as cfg
from gadb.gui.main import gui

def main():
    cfg.check_config_ini()
    gui.init_root()
