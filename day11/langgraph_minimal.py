from langgraph.graph import END, StateGraph


# ----- State -----
class State(dict):
    pass


# ----- Nodes -----
def start_node(state: State):
    print("START node")
    return state


def middle_node(state: State):
    print("MIDDLE node")
    return state


def terminal_node(state: State):
    print("TERMINAL node reached")
    return state


# ----- Graph -----
graph = StateGraph(State)

graph.add_node("START", start_node)
graph.add_node("MIDDLE", middle_node)
graph.add_node("TERMINAL", terminal_node)

graph.set_entry_point("START")

graph.add_edge("START", "MIDDLE")
graph.add_edge("MIDDLE", "TERMINAL")
graph.add_edge("TERMINAL", END)


app = graph.compile()


if __name__ == "__main__":
    final_state = app.invoke({})
    print("Final state:", final_state)
