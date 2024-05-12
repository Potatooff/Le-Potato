# BSD 3-Clause License
# Copyright (c) 2024, Potatooff
# Faiss library is using the cpu only version!

import faiss, os
from llama_index.core.settings import Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.vector_stores.faiss import FaissVectorStore

from llama_index.core import (
    VectorStoreIndex, SimpleDirectoryReader, load_index_from_storage, StorageContext
)

from src.core.settings import (
    similarity_top_k,  database_files_folder_path, embedding_model_dimension, 
    database_cachedfiles_folder_path, web_server_debug, rag_chunk_size, rag_chunk_overlap
)


class FaissEmbeddingStorage: 
    """Create, load or Update embeddings"""

    def __init__(self, embedding_model, dimension=embedding_model_dimension):
        self.d = dimension
        self.embedded_model = embedding_model
        self.index = None 


    def load_index_from_cache(self, cache_folder_path):
        """Load the index from the cache"""

        vector_store = FaissVectorStore.from_persist_dir(cache_folder_path)
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store, 
            persist_dir=cache_folder_path
        )

        index = load_index_from_storage(
            show_progress=web_server_debug,
            storage_context=storage_context, 
            embed_model=self.embedded_model
        )

        return index


    def initialize_index(self) -> VectorStoreIndex | None:
        """ Create the index from the files in the database_files_folder_path"""

        # Check if the folder is empty
        folder_files =  os.listdir(database_files_folder_path)
        if len(folder_files) == 0: return None
        elif len(folder_files) == 1 and folder_files[0] == '.gitkeep': return None
        

        # Create embedding and save to cache        

        # Set the chunk size and overlap
        Settings.text_splitter = SentenceSplitter(chunk_size=rag_chunk_size, chunk_overlap=rag_chunk_overlap)

        # Check for embedding caches
        if os.path.exists(database_cachedfiles_folder_path):
            return self.load_index_from_cache(database_cachedfiles_folder_path)
        
        # Create embeddings
        faiss_index = faiss.IndexFlatL2(self.d)
        vector_store = FaissVectorStore(faiss_index=faiss_index)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)        
        documents = SimpleDirectoryReader(input_dir=database_files_folder_path).load_data(show_progress=web_server_debug)
        nodes = Settings.text_splitter.get_nodes_from_documents(documents=documents, show_progress=web_server_debug)
        index = VectorStoreIndex(
            nodes=nodes,
            show_progress=web_server_debug,
            storage_context=storage_context, 
            embed_model=self.embedded_model,
        )

        # Save the index
        index.storage_context.persist(persist_dir=database_cachedfiles_folder_path)

        return index

    
    def updateIndex(self, file_path: str) -> VectorIndexRetriever | None:
        """Update the index with new files"""

        try:
            # Check if the index has been created
            if self.index is None:
                self.index = self.initialize_index()

                if self.index is None:
                    print("Failed to initialize the index.")
                    return None
                
                return VectorIndexRetriever(index=self.index, similarity_top_k=similarity_top_k)

            # Update the index with new files
            Settings.text_splitter = SentenceSplitter(chunk_size=rag_chunk_size, chunk_overlap=rag_chunk_overlap)

            try:
                documents = SimpleDirectoryReader(input_files=[file_path]).load_data(show_progress=web_server_debug)
            except Exception as e:
                print(f"Failed to read or process documents from {file_path}: {e}")
                return None

            _nodes = Settings.text_splitter.get_nodes_from_documents(documents=documents, show_progress=web_server_debug)

            # Insert and save the index
            self.index.insert_nodes(_nodes)
            self.index.storage_context.persist(persist_dir=database_cachedfiles_folder_path)

            return VectorIndexRetriever(index=self.index, similarity_top_k=similarity_top_k)

        except Exception as e:
            print(f"An error occurred in updateIndex: {e}")
            return None


    def deleteFilesFromDatabase(
        self, folder_path: list = [database_files_folder_path, database_cachedfiles_folder_path]
    ):
        """Delete the cache and current folder at the end of the session"""
        try:
            if folder_path:  # Check if the list is not empty
                print(len(folder_path))
                for folder in folder_path:
                    if os.listdir(folder):  # Check if the folder is not empty
                        for filename in os.listdir(folder):
                            if filename != '.gitkeep':  # Skip '.gitkeep' files
                                file_path = os.path.join(folder, filename)
                                try:
                                    if os.path.isfile(file_path) or os.path.islink(file_path):
                                        os.remove(file_path)  # Remove the file
                                    elif os.path.isdir(file_path):
                                        os.rmdir(file_path)  # Remove empty directories
                                except Exception as e:
                                    print(f"Failed to delete {file_path}. Reason: {e}")
                if os.path.exists(database_cachedfiles_folder_path):
                    os.rmdir(database_cachedfiles_folder_path)
                    
        except FileNotFoundError as e:
            return None


    def get_retriever_engine(self) -> VectorIndexRetriever | None:
        """Returns the rag engine with the postprocessors and reranker enabled"""
        
        if self.index is None: 
            return None
        else: 
            return VectorIndexRetriever(index=self.index, similarity_top_k=similarity_top_k)
