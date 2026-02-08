"""
Problem

Some decisions must not be automated.
Humans must be modeled — not hacked in.
"""

from dataclasses import dataclass

from langgraph.graph import END, StateGraph


# ---- State ----
@dataclass
class AgentState:
    decision: str | None = None


# ---- Nodes ----
def agent_decision(state: AgentState):
    print("Agent proposes an action")
    return state


def human_review(state: AgentState):
    choice = input("Human decision (approve/reject): ").strip().lower()
    state.decision = "APPROVE" if choice == "approve" else "REJECT"
    return state


def approved(state: AgentState):
    print("APPROVED: Execution continues")
    return state


def rejected(state: AgentState):
    print("REJECTED: Execution failed")
    return state


# ---- Graph ----
graph = StateGraph(AgentState)

graph.add_node("AGENT", agent_decision)
graph.add_node("HUMAN", human_review)
graph.add_node("APPROVED", approved)
graph.add_node("REJECTED", rejected)

graph.set_entry_point("AGENT")

graph.add_edge("AGENT", "HUMAN")

graph.add_conditional_edges(
    "HUMAN",
    lambda state: state.decision,
    {
        "APPROVE": "APPROVED",
        "REJECT": "REJECTED",
    },
)

graph.add_edge("APPROVED", END)
graph.add_edge("REJECTED", END)

app = graph.compile()

if __name__ == "__main__":
    app.invoke(AgentState())
