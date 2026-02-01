from langchain_ollama import OllamaLLM


llm = OllamaLLM(model="llama3")


prompt = """
Answer the following questions:

1. What is 123 * 456?
2. What is the current system time?
3. Simulate calling an API that returns the user's account balance.
"""

result = llm.invoke(prompt)

print("----------------------------------------")
print(result)
print("----------------------------------------")