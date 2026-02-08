"""Problem

Retries are control logic, not LLM behavior.
They must be explicit and limited.
"""

from dataclasses import dataclass

from langgraph.graph import END, StateGraph

MAX_RETRIES = 3


# ---- State ----
@dataclass
class AgentState:
    retries: int = 0
    success: bool = False


# ---- Nodes ----
def attempt(state: AgentState):
    state.retries += 1
    print(f"Attempt {state.retries}")
    return state


def check(state: AgentState):
    if state.retries >= MAX_RETRIES:
        return "FAILED"
    return "RETRY"


def failed(state: AgentState):
    print("FAILED: Retry limit reached")
    return state


# ---- Graph ----
graph = StateGraph(AgentState)

graph.add_node("ATTEMPT", attempt)
graph.add_node("FAILED", failed)

graph.set_entry_point("ATTEMPT")

graph.add_conditional_edges(
    "ATTEMPT",
    check,
    {
        "RETRY": "ATTEMPT",
        "FAILED": "FAILED",
    },
)

graph.add_edge("FAILED", END)

app = graph.compile()

if __name__ == "__main__":
    app.invoke(AgentState())
