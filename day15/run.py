from agent_graph import app, AgentState, instrumentor


def main():
    question = input("Enter your question: ")
    state = AgentState(question=question)

    final_state = app.invoke(state)

    instrumentor.report()

    print("\n=== FINAL OUTPUT ===")
    print(final_state)


if __name__ == "__main__":
    main()