# BSD 3-Clause License
# Copyright (c) 2024, Potatooff
# Assuming the API is OpenAI Compatible.

from openai import OpenAI
from src.core.rag import *
from src.core.settings import *


# Inference utils
class OpenAIInference:
    # Initialize LLM + Chat history

    client: OpenAI = OpenAI(
        api_key=online_model_api_key,
        base_url=online_model_base_url,
    )

    # We give each message a ID for tracking
    chat_history_record: list = [
        (0, {"role": "user", "content": model_system_prompt}),
        (1, {"role": "assistant", "content": "By now, I will now follow  the first message instruction for the rest of the conversation."})
    ]

    @staticmethod
    def _getChatHistory() -> list:
        """Chat history."""
        
        _chat_history: list = list()

        # Get all the messages
        for record in OpenAIInference.chat_history_record:
            _chat_history.append(record[1])

        return _chat_history


    @staticmethod
    def llmInference(user_query: str) -> tuple:
        """Send a chat completion to the LLM."""

        # Check if the user called rag arg
        if user_query.lower()[:4].strip() == "-rag":

            # Processing query 
            parts = user_query.split("\n", 1)
            rag_query = parts[0][4:].strip() # Remove the -rag and get all content before a newline
            user_query = parts[1].strip() if len(parts) > 1 else ''

            if backend_verbose: 
                print(rag_query)
                print(user_query)

            # Get RAG Source
            final_query = [user_query]
            _rag_sources =  ClientRAG.RunRag(rag_query)

            for i, source in enumerate(_rag_sources):
                final_query.append(f"Context Source from file search {i+1} result: {source}")

            user_query: str = "\n\n".join(final_query) # Query + Relevant rag source


        # Here we are getting the latest ID to not lose the tracking and save user response
        OpenAIInference.chat_history_record.append(
            (OpenAIInference.chat_history_record[-1][0] + 1, {"role": "user", "content": user_query})
        )

        response = OpenAIInference.client.chat.completions.create(
            seed=3407,
            user=username,
            top_p=model_default_top_p,
            max_tokens=model_default_max_tokens,
            temperature=model_default_temperature,
            stop=model_default_stop_sequence,
            model=online_model_name,
            messages= OpenAIInference._getChatHistory()
        )

        # Here we are getting the latest ID to not lose the tracking and save llm response
        OpenAIInference.chat_history_record.append(
            (OpenAIInference.chat_history_record[-1][0] + 1, {"role": "assistant", "content": response.choices[0].message.content})
        )

        return (OpenAIInference.chat_history_record[-1][0], OpenAIInference.chat_history_record[-1][1]["content"])


    @staticmethod
    def deleteMessageByID(message_id: int) -> None:
        """Delete message by ID."""

        # We look for the message we want to delete
        for i, record in enumerate(OpenAIInference.chat_history_record):
            if record[0] == message_id:

                # It works by pair, we remove the user and assistant reply
                if record[1]["role"] == "user":
                    OpenAIInference.chat_history_record.pop(i)
                    OpenAIInference.chat_history_record.pop(i + 1)
                    break
                else:
                    OpenAIInference.chat_history_record.pop(i)
                    OpenAIInference.chat_history_record.pop(i - 1)
                    break



    def copyMessageByID(message_id: str) -> str:
        """Copy message by ID."""

        # We return content of the ID
        for record in OpenAIInference.chat_history_record:
            if record[0] == int(message_id):
               return str(record[1]["content"])


    @staticmethod
    def clearChatHistory() -> None:
        """ Clear the chat history. """
        
        OpenAIInference.chat_history_record = [
            (0, {"role": "user", "content": model_system_prompt}),
            (1, {"role": "assistant", "content": "By now, I will now follow  the first message instruction for the rest of the conversation."})
        ]

        return None


# Your custom inference logic down here hehe... have fun!
class CustomInference: 
    """Here you can add your custom inference logic, following the OpenAIInference class ^"""
    
    @staticmethod
    def llmInference(user_query: str) -> tuple:
        ...
        
    @staticmethod
    def deleteMessageByID(message_id: int) -> None:
        ...
        
    @staticmethod
    def copyMessageByID(message_id):
        ...
        
    @staticmethod
    def clearChatHistory() -> None:
        ...