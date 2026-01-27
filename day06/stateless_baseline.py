# Reused Day 05 LCEL pipeline intentionally (no memory, no history)

from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

# Initialize LLM (stateless call)
llm = OllamaLLM(model="llama3")

# Prompt for sentiment classification
prompt = PromptTemplate(
    input_variables=["text"],
    template="""
Classify the sentiment of the following text as POSITIVE, NEGATIVE, or NEUTRAL.
Respond with only one word.

Text: "{text}"
"""
)

# LCEL multi-step pipeline
chain = (
    {"text": RunnablePassthrough()}
    | prompt
    | llm
    | (lambda sentiment: {
        "sentiment": sentiment.strip()
    })
    | (lambda data: f"Final Sentiment Classification: {data['sentiment']}")
)

# User input
text = input("Enter text to classify sentiment: ")

# Invoke pipeline
result = chain.invoke(text)

print("----------------------------------------")
print("Entered Text:", text)
print("----------------------------------------")
print(result)
print("----------------------------------------")