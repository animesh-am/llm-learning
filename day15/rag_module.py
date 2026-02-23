import os
import numpy as np
from sentence_transformers import SentenceTransformer

DATA_DIR = "data"

_model = SentenceTransformer("all-MiniLM-L6-v2")


def load_documents():
    documents = []
    for filename in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            documents.append(f.read())
    return documents


_documents = load_documents()
_embeddings = _model.encode(_documents)


def retrieve_context(query: str, top_k: int = 2) -> str:
    query_embedding = _model.encode([query])[0]
    similarities = np.dot(_embeddings, query_embedding)

    top_indices = similarities.argsort()[-top_k:][::-1]
    retrieved = [_documents[i] for i in top_indices]

    return "\n".join(retrieved)