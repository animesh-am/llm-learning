from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

# Initialize LLM
llm = OllamaLLM(model="llama3")

# Prompt template
prompt = PromptTemplate(
    input_variables=["text"],
    template="""
Classify the sentiment of the following text as POSITIVE, NEGATIVE, or NEUTRAL.
Respond with only one word.

Text: "{text}"
"""
)

# LCEL pipeline (this is the key difference from Day 4)
chain = prompt | llm

# User input
text = input("Enter text to classify sentiment: ")

# Invoke the pipeline
result = chain.invoke({"text": text})

print("----------------------------------------")
print("Entered Text:", text)
print("----------------------------------------")
print(result)
print("----------------------------------------")
