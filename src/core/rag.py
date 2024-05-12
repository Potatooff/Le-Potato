# BSD 3-Clause License
# Copyright (c) 2024, Potatooff

from src.core.settings import *
from llama_index.core import QueryBundle
from llama_index.core.settings import Settings
from src.core.embeddings import FaissEmbeddingStorage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from llama_index.core.postprocessor import (
    MetadataReplacementPostProcessor,  SentenceTransformerRerank,
    SentenceEmbeddingOptimizer
)


# Load embedding model
HFE_embedding_model = HuggingFaceEmbedding(model_name=embedding_model)
Settings.embed_model = HFE_embedding_model



# Node Processors - This recipe gives some sweet results
POST_PROCESSOR = [
    MetadataReplacementPostProcessor(target_metadata_key="window"),
    SentenceEmbeddingOptimizer(embed_model=Settings.embed_model, percentile_cutoff=0.5),
    SentenceTransformerRerank(top_n=rerank_top_n, model=reranker_model) # Reranker (most important for good result)
]

class ClientRAG:

    # Set up the query engine for each files
    file_faiss_storage =  FaissEmbeddingStorage(embedding_model=HFE_embedding_model)
    file_query_engine = file_faiss_storage.get_retriever_engine()

    def RunRag(query: str) -> list:
        """Related Document Source"""

        _related_source: list = list()
        _nodes = ClientRAG.file_query_engine.retrieve(query)

        # Postprocess the nodes
        for _, postprocessor in enumerate(POST_PROCESSOR):
            if _ == 2: # Check if the node is the Reranker
                _nodes = postprocessor.postprocess_nodes(_nodes, QueryBundle(query_str=query))
            else:
                _nodes = postprocessor.postprocess_nodes(_nodes)

        # Extract text from the 2 most relevant node
        for node in _nodes:
            # Add to the related source
            _related_source.append(node.text)

            if backend_verbose:
                print(node)

        return _related_source
