# BSD 3-Clause License
# Copyright (c) 2024, Potatooff

from src.frontend.app import app
from colorama import Fore, Style
from src.core.settings import (
    web_server_host, web_server_port, 
    web_server_debug, cli_mode
)


if __name__ == '__main__':
    try:
        if cli_mode:
            print(Fore.YELLOW + "Running in CLI mode..." + Style.RESET_ALL)

        else:
            print(Fore.YELLOW + "Starting server..." + Style.RESET_ALL)
            app.run(
                host = None if web_server_host is None else web_server_host,
                port = 1234 if web_server_port is None else web_server_port, 
                debug= True if web_server_debug is None else web_server_debug
            )

    finally:
        print(Fore.RED + "Shutting down server, Thank you! :)" + Style.RESET_ALL)
        