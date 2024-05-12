# BSD 3-Clause License
# Copyright (c) 2024, Potatooff

import configparser
from os import path


#  ============ Le Potato files / folder paths  ============

project_path = path.dirname(path.dirname(path.dirname((path.abspath(__file__)))))

folder_data = path.join(project_path, "database")
file_Le_Potato_ini = path.join(folder_data, "potato.ini")
file_config_json = path.join(folder_data, "configuration.yaml")


#  ============ Le_Potato.ini values ============

config = configparser.ConfigParser()
config.read(file_Le_Potato_ini)

_INFORMATAION_SECTION = 'INFORMATIONS'
LE_POTATO_LICENSE = config[_INFORMATAION_SECTION]['License']
LE_POTATO_VERSION = config[_INFORMATAION_SECTION]['version'] 
LE_POTATO_NAME = config[_INFORMATAION_SECTION]['project_name']
LE_POTATO_OWNER = config[_INFORMATAION_SECTION]['project_owner']
LE_POTATO_GITHUB_REPOSITORY = config[_INFORMATAION_SECTION]['project_github_repository']
