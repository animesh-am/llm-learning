from dataclasses import dataclass
from langgraph.graph import StateGraph, END
import subprocess

from rag_module import retrieve_context
from tools_module import calculator, uppercase


# ---- State ----
@dataclass
class AgentState:
    query: str
    context: str | None = None
    decision: str | None = None
    tool_input: str | None = None
    result: str | None = None


# ---- Nodes ----
def rag_node(state: AgentState):
    state.context = retrieve_context(state.query)
    print("\n[RAG CONTEXT]")
    print(state.context)
    return state


def llm_decide(state: AgentState):
    prompt = f"""
Decide the next step.

Context:
{state.context}

User Query:
{state.query}

Choose ONE word only:
ANSWER
CALCULATE
UPPERCASE
"""

    response = subprocess.run(
        ["ollama", "run", "llama3.1:8b", prompt],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        timeout=30,
    )

    output = response.stdout.strip().upper()

    print("\n[RAW LLM OUTPUT]")
    print(output)

    if "CALCULATE" in output:
        state.decision = "CALCULATE"
        state.tool_input = "2 + 2"
    elif "UPPERCASE" in output:
        state.decision = "UPPERCASE"
        state.tool_input = state.query
    else:
        state.decision = "ANSWER"

    print("[LLM DECISION]", state.decision)
    return state


def answer_node(state: AgentState):
    prompt = f"""
You are an assistant.

Use ONLY the context below to answer the user's question.
Do not hallucinate.

Context:
{state.context}

Question:
{state.query}

Answer clearly and concisely.
"""

    response = subprocess.run(
        ["ollama", "run", "llama3.1:8b", prompt],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        timeout=30,
    )

    state.result = response.stdout.strip()
    return state


def calculator_node(state: AgentState):
    state.result = calculator(state.tool_input)
    return state


def uppercase_node(state: AgentState):
    state.result = uppercase(state.tool_input)
    return state


def done_node(state: AgentState):
    print("\n[FINAL ANSWER]")
    print(state.result)
    return state


# ---- Graph ----
graph = StateGraph(AgentState)

graph.add_node("RAG", rag_node)
graph.add_node("DECIDE", llm_decide)
graph.add_node("ANSWER", answer_node)
graph.add_node("CALCULATE", calculator_node)
graph.add_node("UPPERCASE", uppercase_node)
graph.add_node("DONE", done_node)

graph.set_entry_point("RAG")

graph.add_edge("RAG", "DECIDE")

graph.add_conditional_edges(
    "DECIDE",
    lambda state: state.decision,
    {
        "ANSWER": "ANSWER",
        "CALCULATE": "CALCULATE",
        "UPPERCASE": "UPPERCASE",
    },
)

graph.add_edge("ANSWER", "DONE")
graph.add_edge("CALCULATE", "DONE")
graph.add_edge("UPPERCASE", "DONE")
graph.add_edge("DONE", END)

app = graph.compile()
