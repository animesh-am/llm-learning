import os
from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

# -----------------------------
# Load documents
# -----------------------------

DOCS_PATH = "docs"
documents = []

for filename in os.listdir(DOCS_PATH):
    if filename.endswith(".txt"):
        with open(os.path.join(DOCS_PATH, filename), "r", encoding="utf-8") as f:
            documents.append(
                Document(
                    page_content=f.read(),
                    metadata={"source": filename}
                )
            )

# -----------------------------
# Embeddings + Vector Store
# -----------------------------

embeddings = OllamaEmbeddings(model="nomic-embed-text")

vectorstore = FAISS.from_documents(
    documents=documents,
    embedding=embeddings
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# -----------------------------
# LLM
# -----------------------------

llm = OllamaLLM(model="llama3")

# -----------------------------
# Prompt (Explicit Context Injection)
# -----------------------------

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful assistant.
Answer the question using ONLY the provided context.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}
"""
)

# -----------------------------
# Query
# -----------------------------

question = "What is the difference between memory and RAG?"

# Retrieve documents
retrieved_docs = retriever.invoke(question)

print("\n--- Retrieved Context ---\n")

context_text = ""
for i, doc in enumerate(retrieved_docs, start=1):
    print(f"[Doc {i}] Source: {doc.metadata['source']}")
    print(doc.page_content)
    print("----------------------------------------")
    context_text += doc.page_content + "\n\n"

# -----------------------------
# LCEL Pipeline
# -----------------------------

chain = prompt | llm

response = chain.invoke(
    {
        "context": context_text,
        "question": question
    }
)

print("\n--- Final Answer ---\n")
print(response)
print("----------------------------------------")
