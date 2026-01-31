from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

# Initialize LLM
llm = OllamaLLM(model="llama3")

# Prompt template (NO CONTEXT)
prompt = PromptTemplate(
    input_variables=["question"],
    template="""
    You are a helpful assistant.

    Answer the following question as accurately as possible.

    Question:
    "{question}"
    """.strip()
)

# LCEL pipeline
chain = prompt | llm

# Question that REQUIRES external knowledge
question = "What is our internal leave policy for full-time employees?"

# Invoke pipeline
result = chain.invoke({"question": question})

print("----------------------------------------")
print("Question:", question)
print("----------------------------------------")
print(result)
print("----------------------------------------")
# Expected: The model will likely not be able to answer accurately due to lack of context.