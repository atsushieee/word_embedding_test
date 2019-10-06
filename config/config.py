import os
import yaml

MODULE_PATH = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = open(MODULE_PATH + '/../config/config.yml', 'r')
CONFIG = yaml.load(CONFIG_PATH)
