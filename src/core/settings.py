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
    print(Fore.RED + "Configuration file not found. Please, check the configuration.yaml file." + Style.RESET_ALL)
    exit()

except yaml.YAMLError as e:
    print(Fore.RED + f"Configuration file is not a valid YAML file. Please, check the configuration.yaml file content.\n---\n{e}\n---" + Style.RESET_ALL)
    exit()


# Access the default settings | Change them on the settings.json file

web_server_host = configuration_read_mode['GENERAL']['host']
web_server_port = configuration_read_mode['GENERAL']['port']
web_server_debug = configuration_read_mode['GENERAL']['debug']
backend = configuration_read_mode['GENERAL']['backend']
backend_verbose = configuration_read_mode['GENERAL']['backend_verbose']

hosting_method = configuration_read_mode['GENERAL']['hosting_method']
online_model_name = configuration_read_mode['GENERAL']['online_model_name']
online_model_api_key = configuration_read_mode['GENERAL']['online_model_api_key']
online_model_base_url = configuration_read_mode['GENERAL']['online_model_base_url']

rerank_top_n = configuration_read_mode['GENERAL']['rerank_top_n']
reranker_model = configuration_read_mode['GENERAL']['reranker_model']
rag_chunk_size = configuration_read_mode['GENERAL']['rag_chunk_size']
embedding_model = configuration_read_mode['GENERAL']['embedding_model']
similarity_top_k = configuration_read_mode['GENERAL']['similarity_top_k']
rag_chunk_overlap = configuration_read_mode['GENERAL']['rag_chunk_overlap']
embedding_model_dimension = configuration_read_mode['GENERAL']['embedding_model_dimensions']

summarize_web_content = configuration_read_mode['GENERAL']['summarize_web_content']
summarize_model = configuration_read_mode['GENERAL']['summarize_model']

display_chat_history = configuration_read_mode['GENERAL']['display_chat_history']

username = configuration_read_mode['GENERAL']['username']
model_username = configuration_read_mode['GENERAL']['model_username']

model_system_prompt = configuration_read_mode['MODEL_INFERENCE_PARAMS']['model_system_prompt']
model_default_top_p = configuration_read_mode['MODEL_INFERENCE_PARAMS']['model_default_top_p']
model_default_temperature = configuration_read_mode['MODEL_INFERENCE_PARAMS']['model_default_temperature']

model_default_max_tokens = configuration_read_mode['MODEL_INFERENCE_PARAMS']['model_default_max_tokens']
model_default_stop_sequence = configuration_read_mode['MODEL_INFERENCE_PARAMS']['model_default_stop_sequence']

model_default_presence_penalty = configuration_read_mode['MODEL_INFERENCE_PARAMS']['model_default_presence_penalty']
model_default_frequency_penalty = configuration_read_mode['MODEL_INFERENCE_PARAMS']['model_default_frequency_penalty']
