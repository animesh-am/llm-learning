from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage


# Initialize LLM
llm = ChatOllama(model="llama3.1:8b", temperature=0.7)


def naive_agent(user_goal: str):
    history = []

    print("\n=== NAIVE AGENT STARTED ===")
    print("Goal:", user_goal)
    print("Kill the process manually to stop.\n")

    while True:  # intentionally infinite loop
        prompt = f"""
      You are an automomous agent.
      
      User goal: {user_goal}
      
      Previous steps taken: {history}
      
      Decide the next step to achieve the goal. Be confident and decisive.
    """

        response = llm.invoke([HumanMessage(content=prompt)]).content.strip()

        history.append(response)

        print("Agent: ", response)
        print("-" * 1)


if __name__ == "__main__":
    user_goal = "Write a business plan for an AI startup."
    naive_agent(user_goal)
