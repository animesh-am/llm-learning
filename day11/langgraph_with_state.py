from dataclasses import dataclass

from langgraph.graph import END, StateGraph


# ----- State -----
@dataclass
class AgentState:
    counter: int = 0
    status: str = "RUNNING"


# ----- Nodes -----
def increment(state: AgentState):
    state.counter += 1
    print("Counter:", state.counter)
    return state


def check(state: AgentState):
    if state.counter >= 3:
        state.status = "DONE"
    return state


def done(state: AgentState):
    print("DONE reached")
    return state


# ----- Graph -----
graph = StateGraph(AgentState)

graph.add_node("INCREMENT", increment)
graph.add_node("CHECK", check)
graph.add_node("DONE", done)

graph.set_entry_point("INCREMENT")

graph.add_edge("INCREMENT", "CHECK")

graph.add_conditional_edges(
    "CHECK",
    lambda state: state.status,
    {"RUNNING": "INCREMENT", "DONE": "DONE"},
)

graph.add_edge("DONE", END)


app = graph.compile()

if __name__ == "__main__":
    result = app.invoke(AgentState())
    print("Final state:", result)
