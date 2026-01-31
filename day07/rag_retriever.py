import os
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# -----------------------------
# Load documents manually
# -----------------------------

DOCS_PATH = "docs"

documents = []

for filename in os.listdir(DOCS_PATH):
    if filename.endswith(".txt"):
        with open(os.path.join(DOCS_PATH, filename), "r", encoding="utf-8") as f:
            text = f.read()
            documents.append(Document(page_content=text, metadata={"source": filename}))

print(f"Loaded {len(documents)} documents")

# -----------------------------
# Initialize embeddings
# -----------------------------

embeddings = OllamaEmbeddings(model="nomic-embed-text")

# -----------------------------
# Create vector store
# -----------------------------

vectorstore = FAISS.from_documents(documents=documents, embedding=embeddings)

print("Vector store created")

# -----------------------------
# Query (retrieval only)
# -----------------------------

query = "What is the difference between memory and RAG?"

retrieved_docs = vectorstore.similarity_search(query=query, k=2)

print("\n--- Retrieved Documents ---\n")

for i, doc in enumerate(retrieved_docs, start=1):
    print(f"[Result {i}] Source: {doc.metadata['source']}")
    print(doc.page_content)
    print("----------------------------------------")
