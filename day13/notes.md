### Failure Patterns

Most people fail by:

* mixing retrieval logic into prompts
* letting the LLM decide control flow
* hiding state inside strings
* bolting features together late

> Day 13 only answers: `What does a real, minimal, shippable agent architecture look like?`

We must keep these separate:

* **Retrieval logic:** Fetches knowledge from external sources
* **Tool execution:** Performs side effects (API calls, DB writes, calculations)
* **Decision logic:** Chooses *what* to do next (often LLM-assisted)
* **Control flow:** Enforces allowed transitions and termination
* **Orchestration:** Wires everything together

If we mix these:

* state becomes implicit
* behaviour becomes non-reproducible
* small changes may break everything


### Why RAG is a Module, not a Node?

What is RAG (Retrieval-Augmented Generation):

* enriches inputs with external knowledge
* runs at **query time**
* does **not** remember
* does **not** decide

> RAG feeds the agent, it does not become the agent.



Why RAG Should Be a Module:

* Keeps retrieval logic isolated
* Makes it testable independently
* Prevents prompt-driven control flow
* Avoids hidden state mutation


### Why tools are Leaf Nodes?

What Tools actually does:

* execute actions
* talk to external systems
* return results


Tools must  **never** :

* decide what happens next
* branch execution
* retry themselves
* terminate the agent


By making tools leaf nodes:

* execution remains predictable
* retries are controlled by the graph
* failures are handled explicitly
* debugging is proper


### The "Thin Agent" Principle

A good agent is ***thin.***

What a Thin Agent Does:

* decides minimally
* delegates aggressively
* stops early
* fails cleanly


A production-grade skeleton means:

* correct boundaries
* explicit state
* inspectable execution
* safe failure modes
* clean separation of concerns



### Lab 1: rag_module.py

* RAG is implemented as a pure module
* No LangGraph usage
* No tools
* No state mutation
* Input → retrieved context only

> RAG enriches input. It does not decide behaviour.

This module can be:

* tested independently
* reused elsewhere
* swapped without touching agent logic


### Lab 2: tools_module.py

Tools:

* take arguments

* return results
* fail loudly

We don't need any:

* LLM calls
* Graph logic

This matters because:

> Tools execute. They do not decide.

This keeps:

* side effects contained
* control flow proper
* failures visible


### Lab 3: agent_graph.py

* LangGraph is the spine
* RAG feeds the decision node
* LLM  suggests, graph enforces
* Tools are leaf nodes
* Explicit END state guarantees termination


### Lab 4: run_agent.py

We do not have:

* any logic
* any decisions
* any state mutation
* Only wiring and execution
