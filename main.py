# 🥔 Le Potato 
# BSD 3-Clause License
# Copyright (c) 2024, Potatooff

from colorama import Fore, Style
from src.frontend.app import app

from src.core.settings import (
    web_server_host, web_server_port, web_server_debug, backend
)

if __name__ == '__main__':
    try:
        print(Fore.YELLOW + "🥔 Starting server..." + Style.RESET_ALL)
        app.run(
            host = None if web_server_host is None else web_server_host,
            port = 1234 if web_server_port is None else web_server_port, 
            debug= True if web_server_debug is None else web_server_debug
        )

    finally:
        if backend:
            # Clean files before closing
            from src.core.rag import ClientRAG
            print(Fore.RED + "🥔 Clearing file caches!" + Style.RESET_ALL)
            ClientRAG.file_faiss_storage.deleteFilesFromDatabase()
            
        print(Fore.RED + "🥔 Shutting down server, Thank you!" + Style.RESET_ALL)
        