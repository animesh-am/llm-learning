
from sentence_transformers import SentenceTransformer
import numpy as np

# ---- Dummy Documents ----
DOCUMENTS = [
    "LangGraph is a state machine framework for LLM workflows.",
    "RAG stands for Retrieval Augmented Generation.",
    "Tools should be executed as leaf nodes in agent graphs.",
]

# ---- Embedding Model ----
_model = SentenceTransformer("all-MiniLM-L6-v2")

# ---- Build Vector Store ----
_doc_embeddings = _model.encode(DOCUMENTS)


def retrieve_context(query: str, top_k: int = 2) -> str:
    """
    Input: user query
    Output: retrieved context (string)
    """
    query_embedding = _model.encode([query])[0]

    similarities = np.dot(_doc_embeddings, query_embedding)
    top_indices = similarities.argsort()[-top_k:][::-1]

    retrieved = [DOCUMENTS[i] for i in top_indices]
    return "\n".join(retrieved)


# if __name__ == "__main__":
#     query = "What is RAG?"
#     context = retrieve_context(query)
#     print("-"*100)
#     print("Retrieved Context:")
#     print(context)