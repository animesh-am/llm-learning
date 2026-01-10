import requests

url = "http://localhost:11434/api/generate"
model = "llama3"

text = input("Enter text to classify sentiment: ")

prompt =  f"""
Classify the sentiment of this text.
Answer with only one word: POSITIVE, NEGATIVE, or NEUTRAL.

Text: "{text}"
"""

response = requests.post(
    url,
    json={
        "model": model,
        "prompt": prompt,
        "stream": False
    }
)

result = response.json()["response"]

print("----------------------------------------")
print("Entered Text: ", text)
print("----------------------------------------")
print(result)
print("----------------------------------------")