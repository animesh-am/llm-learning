import random


def fake_llm_decision():
    return random.choice(["use_tool_a", "use_tool_b", "retry", "finish", "fail"])


def tool_a():
    print("Tool A executed")
    return random.choice([True, False])


def tool_b():
    print("Tool B executed")
    return random.choice([True, False])


def spaghetti_agent():
    state = {"retries": 0, "steps": 0}

    while True:
        state["steps"] += 1
        decision = fake_llm_decision()
        print(f"\nStep {state['steps']} | Decision: {decision}")

        if decision == "use_tool_a":
            success = tool_a()
            if success:
                print("Tool A success")
            else:
                print("Tool A failed")
                state["retries"] += 1

        elif decision == "use_tool_b":
            success = tool_b()
            if success:
                print("Tool B success")
            else:
                print("Tool B failed")
                state["retries"] += 1

        elif decision == "retry":
            state["retries"] += 1
            print("Retrying...")

        elif decision == "finish":
            print("Agent finished successfully")
            break

        elif decision == "fail":
            print("Agent failed")
            break

        if state["retries"] >= 3:
            print("Too many retries — forced stop")
            break


if __name__ == "__main__":
    spaghetti_agent()
