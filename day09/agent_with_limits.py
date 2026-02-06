from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# -----------------------------
# SIMPLE TOOL (ALLOW-LIST)
# -----------------------------


def calculator(expression: str):
    try:
        return eval(expression, {"__builtins__": {}})
    except Exception as e:
        return f"Error: {e}"


# -----------------------------
# LIMITS (CONTROL LIVES HERE)
# -----------------------------

MAX_STEPS = 5
MAX_TOOL_CALLS = 1

# -----------------------------
# MODEL
# -----------------------------

llm = ChatOllama(model="llama3.1:8b", temperature=0.3)

# -----------------------------
# AGENT WITH EXPLICIT LIMITS
# -----------------------------


def agent_with_limits(goal):
    history = []
    steps = 0
    tool_calls = 0

    print("\n=== AGENT WITH LIMITS ===")
    print("Goal:", goal.strip())
    print(f"Max steps: {MAX_STEPS}")
    print(f"Max tool calls: {MAX_TOOL_CALLS}\n")

    while True:

        # ---- HARD STOPS ----
        if steps >= MAX_STEPS:
            print("❌ TERMINATED: step limit exceeded")
            break

        if tool_calls >= MAX_TOOL_CALLS:
            print("❌ TERMINATED: tool call limit exceeded")
            break

        steps += 1

        prompt = f"""
                    You are an agent.

                    Goal:
                    {goal}

                    Rules:
                    - If the goal is complete, reply ONLY with: DONE
                    - To use a tool, reply EXACTLY like this:
                      USE_TOOL: calculator
                      INPUT: <math expression>

                    Steps used: {steps}/{MAX_STEPS}
                    Tool calls used: {tool_calls}/{MAX_TOOL_CALLS}

                    History:
                    {history}

                    What is the next step?
                  """

        reply = llm.invoke([HumanMessage(content=prompt)]).content.strip()

        print(f"Step {steps} | Agent:", reply)

        # ---- DONE SIGNAL ----
        if reply == "DONE":
            print("✅ SUCCESS: agent completed the task")
            break

        # ---- TOOL USAGE ----
        if reply.startswith("USE_TOOL:"):
            tool_calls += 1
            expression = reply.splitlines()[1].replace("INPUT:", "").strip()
            result = calculator(expression)

            observation = f"Tool result: {result}"
            print(observation)

            history.append(reply)
            history.append(observation)
        else:
            history.append(reply)

        print("-" * 100)


if __name__ == "__main__":
    agent_with_limits(
        """
            Monthly cost: $10,000
            Revenue per customer per month: $50

            Goal:
            Calculate how many customers are needed to break even.
        """
    )
