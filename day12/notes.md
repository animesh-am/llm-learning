By the end of Day 11, we proved:

* Graphs enforce structure
* Termination is guaranteed
* LLM uncertainty is contained inside deterministic control

However, real system do not operate in ideal conditions. They face:

* partial failures
* uncertain decisions
* steps that should not be automated

The core question of today is:

> How do real agent systems behave when things don't go perfectly?

The answer is:

* branching paths
* retries with limits
* human checkpoints

### Branching as First-Class Control Flow

**Correct branching model:**

* Decisions are expressed as:
  * state values
  * explicit edges
* Nodes:
  * execute logics
  * update state
  * do not decide global control flow

What goes wrong with if / else inside nodes:

* Control flow becomes hidden execution logic
* Transitions are:
  * implicit
  * no-visual
  * difficut to trace
* Graph observability collapses

We do a proper Graph-level branching by ensuring the following:

* One node ➡️ multiple possible outgoing edges
* Edge selection:
  * based on state
  * validated by the graph
* All paths are:
  * visible
  * enumerable
  * debuggable

### Retries are Control Logic, not Model behaviour

Retries are actually `control flow decisions.`

Retries must be:

* **bounded:** No infinite attepts
* **observable:** Retry count is visible in state
* **stateful:** Every retry mutates state (e.g., attempt count, error reason)

If we keep Implicit Retries:

* Hidden infinite loops
* Silent cost explosions
* Non-reproducible failures
* Debugging becomes impossible

### Why Failure is a valid Terminal State

Properties of a FAILED state:

* Explicit
* Named
* Reachable by design
* Terminates execution cleanly

This matters because:

* Not all goals are achievable
* Not all tools succeed
* Not all decisions converge

`So the system must stop safely, not just pretend.`

### Human-in-the-Loop (HITL) as a Graph Pattern

Humans are nodes in the graph. They serve as:

* **Pause points**: execution halts awaiting input
* **Approval gates**: Human decision controls transition
* **Escalation paths**: Agent hands control to a human on failure or uncertainty

Human states must be:

* explicit
* named
* terminal or resumable

And, the state must capture:

* why human intervention was needed.

If branching, retries, or HITL are added after the fact:

* state becomes implicit
* control flow becomes opaque
* graphs degrade back into loops
* observability collapses

## Lab 1 — Conditional Branching Graph

### Problem This Lab Solves

In real agent systems, decisions lead to  **different execution paths** .

If branching is implemented using `if/else` inside nodes:

* control flow becomes hidden
* execution paths are not visible at runtime
* debugging becomes guesswork

This lab addresses  **where branching belongs** .

---

### What Was Implemented

* A graph with:
  * one decision node
  * two distinct branches
  * two terminal outcomes
* Branching implemented using:
  * `add_conditional_edges`
  * state-based decisions
* No `if/else` used inside node logic

---

### What We Achieved

* Branching is **explicit at the graph level**
* All possible execution paths are:
  * visible
  * enumerable
  * debuggable
* Different inputs produce different terminal states cleanly

## Lab 2 — Retry with Limits

### Problem This Lab Solves

Retries are often implemented as:

* implicit loops
* silent re-executions
* uncontrolled repetition

This causes:

* infinite loops
* hidden cost explosions
* untraceable failures

This lab addresses  **how retries must be modeled** .

---

### What Was Implemented

* A retry counter stored in explicit state
* A retry path modeled as a graph cycle
* A hard maximum retry limit
* A FAILED terminal state on retry exhaustion

---

### What We Achieved

* Retries became:
  * bounded
  * observable
  * reproducible
* Retry behavior is visible in execution traces
* Infinite execution is structurally impossible

## Lab 3 — Human-in-the-Loop (HITL) Pattern

### Problem This Lab Solves

Some decisions:

* cannot be automated
* should not be automated
* require accountability

Treating humans as exceptions or overrides:

* breaks control flow
* destroys traceability
* introduces hidden state

This lab addresses  **how humans must be modeled** .

---

### What Was Implemented

* A graph where:
  * the agent reaches a decision
  * execution pauses
  * a human node determines the next state
* Human input simulated via CLI
* Approval and rejection mapped to explicit terminal states

---

### What We Achieved

# Humans became **first-class nodes**

* Execution remained:
  * explicit
  * traceable
  * safe
* No hacks, overrides, or side exits
