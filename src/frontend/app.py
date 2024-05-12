# BSD 3-Clause License
# Copyright (c) 2024, Potatooff

import os
from src.core.potato import *
from colorama import Fore, Style
from werkzeug.utils import secure_filename

from flask import (
    Flask, render_template, jsonify, request
)

from src.core.settings import (
    database_files_folder_path, backend, 
    model_username, username, hosting_method
)


# Flask app for the front end
app = Flask(__name__)


# Backend routes

if backend:
    from src.core.inference import ClientRAG
    
    # Check the hosting method
    if hosting_method == 'openai':
        from src.core.inference import OpenAIInference as Inference
    elif hosting_method == 'custom':
        from src.core.inference import CustomInference as Inference
    else:
        raise ValueError("Invalid hosting method. Please, check the configuration.yaml file.")

    @app.route('/llm_chat_completion', methods=['POST'])
    def llm_chat_completion():
        """Chat with llm."""
        data = request.get_json()
        user_query = data['user_query']
        llm_response = Inference.llmInference(user_query)

        return jsonify(llm_response)


    @app.route('/clear_history', methods=['POST'])
    def clear_chat_history():
        """Clears the chat history."""
        Inference.clearChatHistory()
        
        return 'Chat history cleared', 200
    
    @app.route('/delete_message', methods=['POST'])
    def delete_message_by_id():
        """Deletes a message by its ID."""
        
        data = request.get_json()
        message_id = data['messageID']
        Inference.deleteMessageByID(int(message_id))

        return 'Message deleted', 200
    

    @app.route('/copy_message', methods=['POST'])
    def copy_message_by_id():
        """Copies a message by its ID."""
        
        data = request.get_json()
        message_id = data['messageID']
        content = Inference.copyMessageByID(message_id)

        return jsonify(content)
    

    # FILE ATTACHMENT FOR RAG - Not working yet
    @app.route('/upload-file', methods=['POST'])
    def upload_file():
        """Backend route to upload a file to the server."""
        
        if 'file' not in request.files:
            return jsonify({'message': 'No file part in the request'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'message': 'No file selected for uploading'}), 400
        
        if file:
            from src.core.inference  import ClientRAG
            filename = secure_filename(file.filename)
            file.save(os.path.join(database_files_folder_path, filename))
            ClientRAG.file_query_engine = ClientRAG.file_faiss_storage.updateIndex(os.path.join(database_files_folder_path, filename))

            return jsonify({'message': f'File {filename} uploaded successfully'}), 200
    

# Website routes


@app.route('/')
def home():
    """
    Renders the home page template with the LePotato information.

    Returns:
        The rendered home.html template with the following variables:
        - LePotatoName: The name of the LePotato.
        - LePotatoLicense: The license of the LePotato.
        - LePotatoVersion: The version of the LePotato.
    """
    
    return render_template(
        'home.html',
        LePotatoName=LE_POTATO_NAME,
        LePotatoLicense=LE_POTATO_LICENSE,
        LePotatoVersion=LE_POTATO_VERSION,
    )

@app.route('/immersive-chat')
def immersive_chat():
    """
    WARNING - Experimental
    Renders the immersion  chat page.

    If the backend is enabled, clears the chat history before rendering the page.

    Returns:
        The rendered classic chat page with the appropriate variables.
    """
    
    if backend:
        Inference.clearChatHistory()

    return render_template(
        'immersive_chat.html',
        LePotatoName=LE_POTATO_NAME,
    )

@app.route('/classic-chat')
def classic_chat():
    """
    Renders the classic chat page.

    If the backend is enabled, clears the chat history before rendering the page.

    Returns:
        The rendered classic chat page with the appropriate variables.
    """
    
    if backend:
        Inference.clearChatHistory()
        ClientRAG.file_faiss_storage.deleteFilesFromDatabase()

    return render_template(
        'classic_chat.html',
        LePotatoName=LE_POTATO_NAME,
        user_username=username,
        llm_username=model_username,
        backend=backend,
    )

@app.route('/about')
def about():
    """
    Renders the about.html template with the LePotatoName variable.

    Returns:
        The rendered about.html template.
    """
    
    return render_template(
        'about.html',
        LePotatoName=LE_POTATO_NAME,
    )

@app.errorhandler(404)
def page_not_found(e):
    """
    Error handler for 404 page not found.

    Args:
        e: The exception object representing the error.

    Returns:
        A rendered template for the 404.html page with the LePotatoName variable set to LE_POTATO_NAME.
    """
    
    print(Fore.RED + f"404 Error: Page not found\n{e}" + Style.RESET_ALL)

    return render_template(
        '404.html',
        LePotatoName=LE_POTATO_NAME,
    ), 404
