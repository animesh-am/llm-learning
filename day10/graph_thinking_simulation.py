import random

STATES = {
    "START": ["THINKING"],
    "THINKING": ["ACTING", "FAILED"],
    "ACTING": ["DONE", "FAILED"],
    "DONE": [],
    "FAILED": [],
}

TERMINAL_STATES = ["DONE", "FAILED"]


def fake_llm_suggest_next_state(current_state):
    return random.choice(STATES[current_state])


def graph_agent():
    current_state = "START"
    print("Initial State:", current_state)

    while current_state not in TERMINAL_STATES:
        suggested_state = fake_llm_suggest_next_state(current_state)
        print(f"LLM suggests transition: {current_state} → {suggested_state}")

        if suggested_state in STATES[current_state]:
            current_state = suggested_state
            print("Transition accepted.")
        else:
            print("Invalid transition rejected.")
            break

    print("Terminal State:", current_state)


if __name__ == "__main__":
    graph_agent()
