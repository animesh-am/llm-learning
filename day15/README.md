## 1. Overview

This project implements a **safe, structured research assistant agent** built using:

* Retrieval-Augmented Generation (RAG)
* Deterministic tools
* LangGraph for explicit control flow
* Structured state management
* Bounded retries
* Full execution trace instrumentation

This is  **not a demo chatbot** .

It is a deliberately designed agent system with visible control flow and safe failure handling.

The system demonstrates how to build an agent that:

* Retrieves relevant knowledge
* Decides between answering directly or using a tool
* Executes tools safely
* Terminates deterministically
* Logs its decision path
* Fails visibly and predictably

## 2. Architecture

The system follows a strict, layered architecture:

```code
User Question
      ↓
LangGraph Entry
      ↓
RETRIEVE (RAG module)
      ↓
DECIDE (LLM decision node)
      ↓
 ┌───────────────┬───────────────┬───────────────┐
 │               │               │
ANSWER        CALCULATE        FAIL
 │               │
 DONE         DONE
      ↓
END
```

All transitions are explicit.

All decisions are validated by the graph.

All failures terminate cleanly.

There are no hidden loops.

There is no autonomous planning.

There is no prompt-driven control flow.

## 3. Module Separation

Each file has a  **single responsibility** :


### `state_schema.py`

Defines the explicit state structure used throughout the system.

State is the spine of the agent.

---

### `rag_module.py`

Handles:

* Document loading
* Embeddings
* Vector similarity search
* Context retrieval

It does  **not** :

* Mutate agent state
* Decide control flow
* Call tools

It enriches input only.

---

### `tools_module.py`

Contains deterministic tools such as:

* Calculator

Tools:

* Take structured input
* Return structured output
* Raise exceptions on invalid input
* Never retry
* Never decide what happens next

---

### `agent_graph.py`

Defines the LangGraph execution graph:

* Node definitions
* Conditional transitions
* Retry limits
* Terminal states

This file enforces system behavior.

---

### `instrumentation.py`

Tracks:

* Node execution order
* State snapshot per transition
* Execution timestamps

It does not modify business logic.

---

### `run.py`

CLI entry point only.

No decisions.

No logic.

No state mutation.

---

### `evaluation.py`

Simulates test scenarios to evaluate behavior and failure handling.


## 4. Why the Graph Enforces Safety

Traditional agent loops hide control flow inside code.

LangGraph enforces:

* Explicit nodes
* Explicit transitions
* Explicit terminal states
* Bounded retry cycles

The model can suggest a decision, but it cannot:

* Create new transitions
* Execute arbitrary tools
* Loop indefinitely
* Skip termination

Control lives in the graph, not in the prompt.

This prevents runaway behavior and hidden execution paths.

---

## 5. Why RAG Is Isolated

RAG is responsible only for  **retrieval** .

It:

* Injects knowledge
* Does not decide actions
* Does not modify global state
* Does not control execution

If retrieval quality degrades, it is isolated and testable.

This separation prevents:

* Retrieval logic from leaking into decision logic
* Hidden state mutation
* Prompt-based control coupling

RAG feeds the agent.

It does not become the agent.

---

## 6. Why Tools Are Leaf Nodes

Tools execute deterministic side effects.

They:

* Perform calculations
* Return results
* Raise exceptions if invalid

They do not:

* Decide what happens next
* Retry internally
* Change control flow

By keeping tools as leaf nodes:

* Side effects are contained
* Retry logic remains centralized
* Execution paths stay predictable

This prevents tool-level chaos.

---

## 7. Why Retries Are Bounded

Retries are handled explicitly in the graph.

Rules:

* Retry counter stored in state
* Max retry limit enforced
* Retry exhaustion transitions to FAIL
* No infinite loops

This prevents:

* Silent infinite execution
* Hidden degradation
* Cost explosions
* Non-terminating systems

A system that cannot terminate safely is not production-ready.

---

## 8. Why Observability Matters

The system records:

* Execution path
* State at each node
* Transition timestamps

This allows us to answer:

* What did the agent do?
* Why did it choose that path?
* Where did it fail?
* Did it respect constraints?

Observability is not logging.

It is the ability to reconstruct behavior without guessing.

Without observability:

* Silent failure dominates
* Debugging becomes speculation
* Evaluation becomes impossible

LangGraph makes observability possible because structure exists.

---

## 9. Failure Handling Philosophy

This system treats failure as a valid terminal state.

Example failure state:

```
{
  "status": "FAILED",
  "reason": "Retry limit exceeded"
}
```

Failure is:

* Explicit
* Inspectable
* Structured
* Controlled


## 10. What This Project Demonstrates

This capstone demonstrates understanding of:

* State-driven architecture
* Separation of concerns
* Controlled LLM integration
* Deterministic tool execution
* Explicit retry policies
* Safe termination
* Observability patterns
* Structured evaluation

It is a minimal but architecturally correct agent system.
