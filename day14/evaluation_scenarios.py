import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



from day13.agent_graph import app, AgentState


def run_scenario(name, query):
    print(f"\n===== SCENARIO: {name} =====")
    state = AgentState(query=query)
    final_state = app.invoke(state)
    print("\nFinal State:", final_state)
    print("=" * 50)


if __name__ == "__main__":

    # 1. Ambiguous Query
    run_scenario(
        "Ambiguous Query",
        "Tell me something interesting."
    )

    # 2. Invalid Calculation
    run_scenario(
        "Invalid Calculation",
        "Calculate something impossible."
    )

    # 3. Irrelevant RAG Context
    run_scenario(
        "Irrelevant RAG",
        "What is the capital of Mars?"
    )

    # 4. Conflicting Instructions
    run_scenario(
        "Conflicting Instructions",
        "Answer and calculate and uppercase."
    )

    # 5. Forced Retry Exhaustion
    run_scenario(
        "Forced Retry",
        "Force retry behavior."
    )
