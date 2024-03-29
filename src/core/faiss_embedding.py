# BSD 3-Clause License
# Copyright (c) 2024, Potatooff
# Faiss library is using the cpu only version!

import faiss, os
from colorama import Fore, Style
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext, load_index_from_storage
from src.core.settings import database_cachedfiles_folder_path, embedding_model_dimension


class FaissEmbeddingStorage: 
    # Change the model dimension on the database/configuration.yaml file

    def __init__(self, data_dir, embedding_model, dimension=embedding_model_dimension):
        self.d = dimension
        self.data_dir = data_dir
        self.embedded_model = embedding_model
        self.index = self.initialize_index()

    def initialize_index(self):
        if os.path.exists(database_cachedfiles_folder_path) and os.listdir(database_cachedfiles_folder_path):

            print(
                Fore.BLUE + 
                "Reusing previous embeddings - NOTE: delete database/cached_files folder for fresh embeddings. Please wait..." +
                Style.RESET_ALL
            )

            vector_store = FaissVectorStore.from_persist_dir(database_cachedfiles_folder_path)
            storage_context = StorageContext.from_defaults(
                vector_store=vector_store, 
                persist_dir=database_cachedfiles_folder_path
            )

            index = load_index_from_storage(
                storage_context=storage_context, 
                embed_model=self.embedded_model
            )

            return index
        
        else:
            print(
                Fore.BLUE + 
                "Creating embeddings for the first time. This may take a while. Please wait..." +
                Style.RESET_ALL
            )

            faiss_index = faiss.IndexFlatL2(self.d)
            vector_store = FaissVectorStore(faiss_index=faiss_index)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            documents = SimpleDirectoryReader(self.data_dir).load_data(show_progress=True)

            index = VectorStoreIndex.from_documents(
                documents, 
                storage_context=storage_context, 
                embed_model=self.embedded_model
            )

            index.storage_context.persist(persist_dir=database_cachedfiles_folder_path)

            return index

    def get_query_engine(self):
        return self.index.as_query_engine()


    def get_chat_engine(self, llm):
        if llm is None:
            raise ValueError("LLM is required for chat engine")

        return self.index.as_chat_engine(
            chat_mode="react",
            llm=llm,
            verbose=True,
        )