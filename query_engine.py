# query_engine.py

# ✅ Core LlamaIndex imports for loading and querying
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.cohere import Cohere as CohereLLM  # (Not directly used here, but ready for extension)

# ✅ Import your custom Cohere wrapper
from cohere_client import CohereClient
from config import COHERE_API_KEY

# ✅ Initialize Cohere client once
cohere_client = CohereClient()

def query_index(question, chat_history=None):
    """
    Query the vector index for an answer to the user’s question.
    Always retrieves chunks from the entire index and uses Cohere to generate the final answer.
    Supports multi-turn context by including prior Q&A in the final prompt.

    Args:
        question (str): The user’s current question.
        chat_history (list, optional): Previous conversation history for multi-turn continuity.

    Returns:
        tuple: (answer text, list of source metadata dicts)
    """

    # ✅ Load the index from local storage
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    cohere_embed = CohereEmbedding(api_key=COHERE_API_KEY)
    index = load_index_from_storage(storage_context, embed_model=cohere_embed)

    # ✅ Retrieve the most relevant chunks using only the raw question
    nodes = index.as_retriever().retrieve(question)

    # ✅ Combine all retrieved chunks into a single context string
    retrieved_text = "\n\n".join([n.get_content() for n in nodes])

    # ✅ Prepare messages for Cohere chat completion
    messages = []
    if chat_history:
        # Include previous turns if available
        messages.extend(chat_history)

    # Add the current user question with retrieved context attached
    messages.append({
        "role": "user",
        "content": f"{question}\n\nContext:\n{retrieved_text}"
    })

    # ✅ Generate the final answer using Cohere's LLM
    answer = cohere_client.generate_answer(messages=messages)

    # ✅ Collect metadata for each retrieved chunk (for source transparency)
    sources = []
    for node in nodes:
        meta = node.metadata or {}
        sources.append({
            "file_name": meta.get("file_name", "Unknown"),
            "folder_name": meta.get("folder_name", "Unknown"),
            "folder_path": meta.get("folder_path", "Unknown"),
            "page_number": meta.get("page_number", "Unknown"),
            "summary": meta.get("summary", "N/A"),
            "entities": meta.get("entities", "N/A")
        })

    return answer, sources
