from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_message_histories import ChatMessageHistory

llm = OllamaLLM(model="llama3")

# Memory still exists
history = ChatMessageHistory()

# Prompt does NOT include history
prompt = PromptTemplate(
    input_variables=["text"],
    template="""
Classify the sentiment of the following text as POSITIVE, NEGATIVE, or NEUTRAL.
Respond with only one word.

Text: "{text}"
"""
)

chain = (
    {"text": RunnablePassthrough()}
    | prompt
    | llm
)

def run_turn(user_text: str):
    result = chain.invoke(user_text)

    # Memory is stored but never used
    history.add_user_message(user_text)
    history.add_ai_message(result)

    print("----------------------------------------")
    print("Entered Text:", user_text)
    print("Model Output:", result.strip())
    print("----------------------------------------")

while True:
    text = input("Enter text to classify sentiment (or 'exit'): ")
    if text.lower() == "exit":
        break
    run_turn(text)
