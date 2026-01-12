from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda,
    RunnableMap,
)

llm = OllamaLLM(model="llama3")

prompt = PromptTemplate(
    input_variables=["text"],
    template="""
Classify the sentiment of the following text as POSITIVE, NEGATIVE, or NEUTRAL.
Respond with only one word.

Text: "{text}"
"""
)

# LCEL multi-step pipeline with debug prints
chain = (
    RunnableMap({"text": RunnablePassthrough()})

    | RunnableLambda(lambda x: (print("STEP 1 - Raw Input:", x), x)[1])

    | prompt
    | RunnableLambda(lambda x: (print("STEP 2 - Prompt Output:", x), x)[1])

    | llm
    | RunnableLambda(lambda x: (print("STEP 3 - LLM Output:", x), x)[1])

    | RunnableLambda(lambda sentiment: {
        "sentiment": sentiment.strip()
    })

    | RunnableLambda(lambda x: (print("STEP 4 - Structured Dict:", x), x)[1])

    | RunnableLambda(
        lambda data: f"Final Sentiment Classification: {data['sentiment']}"
    )
)

text = input("Enter text to classify sentiment: ")
result = chain.invoke(text)

print("----------------------------------------")
print("Entered Text:", text)
print("----------------------------------------")
print(result)
print("----------------------------------------")
