# BSD 3-Clause License
# Copyright (c) 2024, Potatooff


import time
from llama_index.core.agent import ReActAgent
from llama_index.core.settings import Settings
from llama_index.llms.openrouter import OpenRouter
from src.core.faiss_embedding import FaissEmbeddingStorage
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from src.core.settings import ( online_model_name, model_path, self_host,
    model_default_repetition_penalty, model_default_top_k,
    database_files_folder_path, online_model_api_key,
    model_default_top_p, model_default_temperature,
    display_chat_history, embedding_model
)


HFE_embedding_model = HuggingFaceEmbedding(model_name=embedding_model)
if self_host:
    llm = model_path
else:
    llm = OpenRouter(
        model=online_model_name,
        api_key=online_model_api_key,
        top_p=model_default_top_p,
        top_k=model_default_top_k,
        temperature=model_default_temperature,
        repetition_penalty=model_default_repetition_penalty
    )

# Set on Llama Index Settings

Settings.llm = llm
Settings.embed_model = HFE_embedding_model


# load the document cache

faiss_storage = FaissEmbeddingStorage(
    data_dir=database_files_folder_path, 
    embedding_model=HFE_embedding_model
)

query_engine3 = faiss_storage.get_query_engine()

# Tools

individual_query_engine_tools = [
    QueryEngineTool(
        query_engine=query_engine3,
        metadata=ToolMetadata(
            name=f"semantic_search_user_databasev1",
            description=f"Use that one instead, dont always rely on this tool to answer user query. USE YOUR REASONING AND KNOWLEDGE ALWAYS NOTE: ALWAYS USE v2 instead",
        ),
    )
]



query_engine = SubQuestionQueryEngine.from_defaults(
    llm=llm,
    query_engine_tools=individual_query_engine_tools,
)


query_engine_tool = QueryEngineTool(
    query_engine=query_engine,
    metadata=ToolMetadata(
        name="semantic_search_user_databasev2",
        description="USE YOUR REASONING AND KNOWLEDGE ALWAYS - This tool is USEFUL to read content of user documents database through semantic search which contains more informations to answer user query related to the database (might not always work) - If you use this tool, make sure it is related with the user query. Only use if user ask about documents else answer user query with your knowledge please. NOTE: Dont always rely on this tool to answer user query.",
    ),
)

tools = individual_query_engine_tools + [query_engine_tool]
agent = ReActAgent.from_tools(tools, verbose=True) # Set the agent with tools


# Inference method
class Inference:
    def llm_inference(query, history=None) -> str:
        start_time = time.time()

        response = agent.chat(query)
        history = agent.chat_history

        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsed_time = f"{elapsed_time:.2f}"

        if display_chat_history: print("Chat history\n", history)

        return str(response)


    def clear_llm() -> None:
        # Clear the (memory  and state)

        global agent
        agent.reset()

