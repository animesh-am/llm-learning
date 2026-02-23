import subprocess
from langgraph.graph import StateGraph, END
from state_schema import AgentState
from rag_module import retrieve_context
from tools_module import calculator
from instrumentation import Instrumentor

MODEL_NAME = "llama3.1:8b"
MAX_RETRIES = 2

instrumentor = Instrumentor()


# -------- Nodes --------

def retrieve_node(state: AgentState):
    instrumentor.record("RETRIEVE", state)
    state.context = retrieve_context(state.question)
    return state


def decide_node(state: AgentState):
    instrumentor.record("DECIDE", state)

    prompt = f"""
You are a decision system.

Question:
{state.question}

Context:
{state.context}

Choose ONE word only:
ANSWER
CALCULATE
FAIL
"""

    response = subprocess.run(
        ["ollama", "run", MODEL_NAME, prompt],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        timeout=30
    )

    output = response.stdout.strip().upper()

    if "ANSWER" in output:
        state.decision = "ANSWER"
    elif "CALCULATE" in output:
        state.decision = "CALCULATE"
        state.tool_input = "2 + 2"
    elif "FAIL" in output:
        state.decision = "FAIL"
    else:
        state.retries += 1
        if state.retries > MAX_RETRIES:
            state.decision = "FAIL"
        else:
            state.decision = "RETRY"

    return state


def answer_node(state: AgentState):
    instrumentor.record("ANSWER", state)

    prompt = f"""
Answer the question using ONLY the context.

Question:
{state.question}

Context:
{state.context}
"""

    response = subprocess.run(
        ["ollama", "run", MODEL_NAME, prompt],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        timeout=30
    )

    state.final_answer = response.stdout.strip()
    state.status = "DONE"
    return state


def calculate_node(state: AgentState):
    instrumentor.record("CALCULATE", state)

    try:
        state.tool_result = calculator(state.tool_input)
        state.final_answer = f"The result is {state.tool_result}."
        state.status = "DONE"
    except Exception as e:
        state.status = "FAILED"
        state.final_answer = str(e)

    return state


def fail_node(state: AgentState):
    instrumentor.record("FAIL", state)
    state.status = "FAILED"
    return state


# -------- Graph --------

graph = StateGraph(AgentState)

graph.add_node("RETRIEVE", retrieve_node)
graph.add_node("DECIDE", decide_node)
graph.add_node("ANSWER", answer_node)
graph.add_node("CALCULATE", calculate_node)
graph.add_node("FAIL", fail_node)

graph.set_entry_point("RETRIEVE")

graph.add_edge("RETRIEVE", "DECIDE")

graph.add_conditional_edges(
    "DECIDE",
    lambda state: state.decision,
    {
        "ANSWER": "ANSWER",
        "CALCULATE": "CALCULATE",
        "FAIL": "FAIL",
        "RETRY": "DECIDE"
    }
)

graph.add_edge("ANSWER", END)
graph.add_edge("CALCULATE", END)
graph.add_edge("FAIL", END)

app = graph.compile()