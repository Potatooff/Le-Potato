# BSD 3-Clause License
# Copyright (c) 2024, Potatooff


import yaml
from os import path
from colorama import Fore, Style


# Loading project paths

src_folder_path = path.dirname(path.dirname(path.dirname((path.abspath(__file__)))))
database_folder_path = path.join(src_folder_path, "database")
database_configuration_file_path = path.join(database_folder_path, "configuration.yaml")

database_files_folder_path = path.join(database_folder_path, "files")
database_cachedfiles_folder_path = path.join(database_folder_path, "cached_files")


# Load settings

print(Fore.CYAN + "Loading configuration... NOTE: Some parameters might not be used through the inference process. Check the way you inferencing the LLM." + Style.RESET_ALL)

try:
    with open(database_configuration_file_path, 'r') as yaml_file:
        configuration_read_mode = yaml.safe_load(yaml_file)

except FileNotFoundError:
    print(Fore.RED + "Configuration file not found. Please, check the configuration.json file." + Style.RESET_ALL)
    exit()

except yaml.YAMLError:
    print(Fore.RED + "Configuration file is not a valid JSON file. Please, check the configuration.json file content." + Style.RESET_ALL)
    exit()


# Access the default settings | Change them on the settings.json file

web_server_host = configuration_read_mode['GENERAL']['host']
web_server_port = configuration_read_mode['GENERAL']['port']
web_server_debug = configuration_read_mode['GENERAL']['debug']
cli_mode = configuration_read_mode['GENERAL']['cli_mode']

self_host = configuration_read_mode['GENERAL']['self_host']
model_path = configuration_read_mode['GENERAL']['model_path']
online_model_name = configuration_read_mode['GENERAL']['online_model_name']
online_model_api_key = configuration_read_mode['GENERAL']['online_model_api_key']

embedding_model = configuration_read_mode['GENERAL']['embedding_model']
embedding_model_dimension = configuration_read_mode['GENERAL']['embedding_model_dimensions']

display_chat_history = configuration_read_mode['GENERAL']['display_chat_history']

model_default_top_p = configuration_read_mode['MODEL_INFERENCE_PARAMS']['model_default_top_p']
model_default_top_k = configuration_read_mode['MODEL_INFERENCE_PARAMS']['model_default_top_k']
model_default_min_p = configuration_read_mode['MODEL_INFERENCE_PARAMS']['model_default_min_p']
model_default_temperature = configuration_read_mode['MODEL_INFERENCE_PARAMS']['model_default_temperature']

model_default_max_tokens = configuration_read_mode['MODEL_INFERENCE_PARAMS']['model_default_max_tokens']
model_default_stop_sequence = configuration_read_mode['MODEL_INFERENCE_PARAMS']['model_default_stop_sequence']
model_default_context_length = configuration_read_mode['MODEL_INFERENCE_PARAMS']['model_default_context_length']
model_default_new_max_tokens = configuration_read_mode['MODEL_INFERENCE_PARAMS']['model_default_new_max_tokens']

model_default_presence_penalty = configuration_read_mode['MODEL_INFERENCE_PARAMS']['model_default_presence_penalty']
model_default_frequency_penalty = configuration_read_mode['MODEL_INFERENCE_PARAMS']['model_default_frequency_penalty']
model_default_repetition_penalty = configuration_read_mode['MODEL_INFERENCE_PARAMS']['model_default_repetition_penalty']
