from agent_graph import app, AgentState


def test_case(question):
    print(f"\n=== TEST: {question} ===")
    state = AgentState(question=question)
    result = app.invoke(state)
    print("Final State:", result)


if __name__ == "__main__":
    test_case("What is an agent?")
    test_case("What is 2 + 2?")
    test_case("Do something impossible")
