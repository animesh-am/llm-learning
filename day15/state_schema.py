from dataclasses import dataclass


@dataclass
class AgentState:
    question: str
    context: str = ""
    decision: str = ""
    tool_input: str = ""
    tool_result: str = ""
    final_answer: str = ""
    retries: int = 0
    status: str = "RUNNING"