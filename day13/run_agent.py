from agent_graph import app, AgentState

def main():
    query = input("Enter your query: ")
    state = AgentState(query=query)
    app.invoke(state)

if __name__ == "__main__":
    main()
