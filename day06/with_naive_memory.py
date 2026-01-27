from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.chat_message_histories import ChatMessageHistory

# Initialize LLM
llm = OllamaLLM(model="llama3")

# Naive message history (no pruning, no logic)
history = ChatMessageHistory()

# Prompt includes raw history
prompt = PromptTemplate(
    input_variables=["history", "text"],
    template="""
You are a sentiment classifier.

Conversation so far:
{history}

Classify the sentiment of the following text as POSITIVE, NEGATIVE, or NEUTRAL.
Respond with only one word.

Text: "{text}"
"""
)

# LCEL pipeline
chain = (
    {
        "text": RunnablePassthrough(),
        "history": lambda _: history.messages
    }
    | prompt
    | llm
)

def run_turn(user_text: str):
    result = chain.invoke(user_text)

    # Manually store messages (THIS is the memory)
    history.add_user_message(user_text)
    history.add_ai_message(result)

    print("----------------------------------------")
    print("Entered Text:", user_text)
    print("Model Output:", result.strip())
    print("----------------------------------------")

# Interactive loop
while True:
    text = input("Enter text to classify sentiment (or 'exit'): ")
    if text.lower() == "exit":
        break
    run_turn(text)
