""" Problem

Agents must choose different paths based on confidence or evaluation.
This decision must not live inside a node.

"""

from dataclasses import dataclass

from langgraph.graph import END, StateGraph


# ---- State ----
@dataclass
class AgentState:
    confidence: float


# ---- Nodes ----
def decide_confidence(state: AgentState):
    print(f"Confidence value: {state.confidence}")
    return state


def done(state: AgentState):
    print("DONE: Confidence is high")
    return state


def retry(state: AgentState):
    print("RETRY PATH: Confidence is low")
    return state


# ---- Graph ----
graph = StateGraph(AgentState)

graph.add_node("DECIDE", decide_confidence)
graph.add_node("DONE", done)
graph.add_node("RETRY", retry)

graph.set_entry_point("DECIDE")

graph.add_conditional_edges(
    "DECIDE",
    lambda state: "HIGH" if state.confidence >= 0.7 else "LOW",
    {
        "HIGH": "DONE",
        "LOW": "RETRY",
    },
)

graph.add_edge("DONE", END)
graph.add_edge("RETRY", END)

app = graph.compile()

if __name__ == "__main__":
    print("\n--- High Confidence Run ---")
    app.invoke(AgentState(confidence=0.9))

    print("\n--- Low Confidence Run ---")
    app.invoke(AgentState(confidence=0.4))
