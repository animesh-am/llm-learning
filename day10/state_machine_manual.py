class AgentState:
    START = "START"
    THINKING = "THINKING"
    ACTING = "ACTING"
    DONE = "DONE"
    FAILED = "FAILED"


def run_state_machine(success=True):
    state = AgentState.START
    print("Initial State:", state)

    while state not in [AgentState.DONE, AgentState.FAILED]:
        if state == AgentState.START:
            state = AgentState.THINKING

        elif state == AgentState.THINKING:
            state = AgentState.ACTING

        elif state == AgentState.ACTING:
            if success:
                state = AgentState.DONE
            else:
                state = AgentState.FAILED

        print("Transitioned to:", state)

    print("Terminal State Reached:", state)


if __name__ == "__main__":
    print("\n--- Success Path ---")
    run_state_machine(success=True)

    print("\n--- Failure Path ---")
    run_state_machine(success=False)
