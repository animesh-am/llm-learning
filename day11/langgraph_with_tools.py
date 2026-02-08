import subprocess
from dataclasses import dataclass

from langgraph.graph import END, StateGraph


# ----- State -----
@dataclass
class AgentState:
    query: str
    decision: str | None = None
    result: str | None = None


# ----- LLM Node (Ollama) -----
def llm_decide(state: AgentState):
    prompt = f"""
    Decide the next step.
    Options: SEARCH or DONE.
    Query: {state.query}
  """

    response = subprocess.check_output(["ollama", "run", "llama3.1", prompt], text=True)

    state.decision = "SEARCH" if "search" in response.lower() else "DONE"
    print("LLM decision:", state.decision)
    return state


# ----- Tool Node -----
def search_tool(state: AgentState):
    print("Executing tool (fake search)")
    state.result = f"Result for: {state.query}"
    return state


# ----- Done Node -----
def done(state: AgentState):
    print("Final result:", state.result)
    return state


# ---- Graph ----
graph = StateGraph(AgentState)

graph.add_node("LLM_DECIDE", llm_decide)
graph.add_node("SEARCH", search_tool)
graph.add_node("DONE", done)

graph.set_entry_point("LLM_DECIDE")

graph.add_conditional_edges(
    "LLM_DECIDE",
    lambda state: state.decision,
    {
        "SEARCH": "SEARCH",
        "DONE": "DONE",
    },
)

graph.add_edge("SEARCH", "DONE")
graph.add_edge("DONE", END)

app = graph.compile()

if __name__ == "__main__":
    app.invoke(AgentState(query="What is LangGraph?"))
