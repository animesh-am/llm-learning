from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from tools import add, multiply, get_current_time

import re
import json


# -----------------------------
# Tool Registry (Hard Allow-List)
# -----------------------------

TOOLS = {
    "add": add,
    "multiply": multiply,
    "get_current_time": get_current_time,
}


# -----------------------------
# Prompt
# -----------------------------

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You may answer directly OR request a tool.

If requesting a tool, respond ONLY with valid JSON:
{{
  "tool": "<tool_name>",
  "arguments": {{
    "key": "value"
  }}
}}

Available tools:
- add(a: int, b: int)
- multiply(a: int, b: int)
- get_current_time()

If no tool is needed, respond with:
{{
  "tool": null,
  "answer": "<final answer>"
}}
""",
        ),
        ("user", "{input}"),
    ]
)


# -----------------------------
# Model
# -----------------------------

llm = Ollama(model="llama3", temperature=0)  # reduce creative damage


# -----------------------------
# LCEL Pipeline
# -----------------------------

chain = prompt | llm | StrOutputParser()


# -----------------------------
# Controlled Execution Layer
# -----------------------------


def extract_json(text: str) -> dict:
    """
    Extract the first JSON object from model output.
    Fail loudly if none exists.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON found in model output:\n{text}")

    return json.loads(match.group())


def execute_tool_or_answer(raw_output: str) -> str:
    """
    Trust boundary.
    Model emits text.
    We extract intent.
    """

    model_output = extract_json(raw_output)

    tool_name = model_output.get("tool")

    if tool_name is None:
        return model_output.get("answer", "No answer provided.")

    if tool_name not in TOOLS:
        raise ValueError(f"Rejected unknown tool: {tool_name}")

    arguments = model_output.get("arguments", {})
    result = TOOLS[tool_name](**arguments)

    return f"[TOOL:{tool_name}] → {result}"


executor = RunnableLambda(execute_tool_or_answer)


# -----------------------------
# Full Pipeline
# -----------------------------

pipeline = chain | executor


# -----------------------------
# Run
# -----------------------------

if __name__ == "__main__":
    while True:
        user_input = input("\nUser> ")
        if user_input.lower() in {"exit", "quit"}:
            break

        output = pipeline.invoke({"input": user_input})
        print("System>", output)
