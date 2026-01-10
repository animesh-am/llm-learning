from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

# Initialize the LLM (same model as Lab 1)
llm = OllamaLLM(model="llama3")

# Same prompt as Lab 1
prompt = PromptTemplate(
    input_variables=["text"],
    template="""
Classify the sentiment of the following text as POSITIVE, NEGATIVE, or NEUTRAL.
Respond with only one word.

Text: "{text}"
"""
)

text = input("Enter text to classify sentiment: ")

formatted_prompt = prompt.format(text=text)
result = llm.invoke(formatted_prompt)

print("----------------------------------------")
print("Entered Text: ", text)
print("----------------------------------------")
print(result)
print("----------------------------------------")