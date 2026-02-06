from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage


def calculator(expression: str):
    try:
        return eval(expression, {"__builtins__": {}})
    except Exception as e:
        return f"Error: {e}"

TOOLS = {
    "calculator": calculator
}

# -----------------------------
# LLM
# -----------------------------

llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0.7
)

# -----------------------------
# SIMPLE AGENT LOOP
# -----------------------------

def agent_with_tools(user_goal):
    history = []

    print("\n=== TOOL AGENT STARTED ===")
    print("Goal:", user_goal)
    print("Stop manually.\n")

    while True:  # still intentionally infinite
        prompt = f"""
            You are an agent.

            Goal:
            {user_goal}

            Available tools:
            - calculator (math only)

            To use a tool, respond EXACTLY like this:
            USE_TOOL: calculator
            INPUT: <math expression>

            Previous steps:
            {history}

            What is the next step?
        """

        reply = llm.invoke(
            [HumanMessage(content=prompt)]
        ).content.strip()

        print("Agent:", reply)

        # -----------------------------
        # VERY SIMPLE TOOL HANDLING
        # -----------------------------

        if reply.startswith("USE_TOOL:"):
            lines = reply.splitlines()
            tool_name = lines[0].replace("USE_TOOL:", "").strip()
            tool_input = lines[1].replace("INPUT:", "").strip()

            if tool_name in TOOLS:
                result = TOOLS[tool_name](tool_input)
                observation = f"Tool result: {result}"
            else:
                observation = "Tool not allowed."

            print(observation)
            history.append(reply)
            history.append(observation)

        else:
            history.append(reply)

        print("-" * 100)


if __name__ == "__main__":
    agent_with_tools(
        "Calculate the break-even point for a SaaS startup with $10k monthly costs"
    )
