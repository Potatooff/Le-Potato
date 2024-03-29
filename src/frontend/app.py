# BSD 3-Clause License
# Copyright (c) 2024, Potatooff

import os
from colorama import Fore, Style
from src.core.inference import Inference
from src.core.settings import database_files_folder_path
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Website routes

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/about')
def about():
    return render_template('about.html')


# Backend routes

@app.route('/llm_chat_completion', methods=['POST'])
def llm_chat_completion():
    data = request.get_json()
    user_query = data['user_query']
    llm_response = Inference.llm_inference(user_query)
    return jsonify(llm_response)


@app.route('/clear_history', methods=['POST'])
def clear_chat_history():
    Inference.clear_llm()
    return 'Chat history cleared', 200


# FILE ATTACHMENT FOR RAG
@app.route('/upload', methods=['POST'])
def handle_files_upload() -> None:
    files = request.files.getlist('files[]')

    if not os.path.exists(database_files_folder_path):
        os.makedirs(database_files_folder_path)

    for file in files:

        if file:
            
            file_path = os.path.join(database_files_folder_path, file.filename)

            if os.path.exists(file_path): # Check if the file already exists
                print(Fore.RED + "File name existing - Replacing it for the attached file: " + Style.RESET_ALL + f"{file.filename}")  

            file.save(file_path)

    return 'Files uploaded successfully', 200
