##### How do we make agent behaviour explicit, inspectable, and debuggable?

By using Graphs.

### 1. Why While-Loops Fail for Complex Agents?

As the agent logic evolves, loops accumulate:

* conditionals
* retries
* special cases
* early exits
* partial successes

This creates four structural failures:

**a)** **Hidden Transitions**

State changes happen inside arbitrary code blocks:

```python
if tool_failed:
    state["retry"] += 1

```

But there is nor explicit declaration of:

* from which state
* to which state
* under what transition rule


**b)** **Implicit State Changes**

State mutates as a side effect:

* tool calls
* error handlers
* retries
* exception paths

At runtime, we can not easily answer:

> Why I am in this state?
>
> Because the transition was implicit, not declared.



**c) Nested Conditionals**

Loops accumulate layers:

```python
while True:
    if A:
        if B:
            if C:
                ...
```

Each nesting:

* hides execution paths
* multiple possible behaviours
* destroys predictability


**d) Impossible to Trace Execution Paths**

When control flows lives in code:

* there is no runtime map
* no visual trace
* no execution history by design

> This is a control structure problem. This makes debugging very hard.


### 2. Finite State Machines (FSM)

A Finite State machine consists of:

* ***States***: Distinct, named configurations of the system
* ***Transitions***: Explicit rules for moving between states
* ***Events / Conditions***: Triggers that cause transitions
* ***Terminal States***: States where execution ends

Why do we need FSM here?

FSM enforce:

* explicit state
* explicit transitions
* explicit termination

FSMs are foundation in:

* compilers
* parsers
* networking protocols
* operating systems
* embedded systems


### 3. Agent as a State Machine

Agents are often described as:

* "thinking"
* "reasoning"
* "deciding"

This langusge is misleading.

**Correct Mapping:** 

| Agent Metaphor   | Actual Mechanism           |
| ---------------- | -------------------------- |
| *“Thinking”*  | State transition           |
| *“Acting”*    | Side effect (tool, output) |
| *“Observing”* | State update               |
| *“Planning”*  | Conditional transitions    |

> An agent is a *state machine* whose transitions may consult a probabilistic model.
>
> So, the model suggests and the graph decides.



### 4. Graphs vs Loops

| Loop                 | Graph                |
| -------------------- | -------------------- |
| Implicit transitions | Explicit transitions |
| Hard to debug        | Traceable            |
| Hidden state         | Named state          |
| Ad-hoc exits         | Terminal nodes       |

**Why loops hide behaviour?**

* Transitions are encoded in code paths
* State mutations are scattered
* Execution paths are emergent, not declared

**Why Graphs reveal behaviour?**

Graphs force you to:

* name states
* declare transitions
* define terminal points
* visualize execution paths


### Why LangGraph exists?

**The Limits of LCEL**

LCEL (LangChain Expression Language):

* excels at **linear pipelines**
* handles sequential flows well

But agents require:

* branching
* looping with visibility
* conditional transitions
* explicit state


LangGraph exists because agents need:

* **branching control flow**
* **observable loops**
* **explicit state**
* **inspectable execution paths**

In short:

> **LangGraph = stateful, inspectable execution graph**




# Lab 1 Notes (ad_hoc_agent_spaghetti.py)

Where is state stored?

- Inside a mutable dictionary scattered across the loop.
- No single source of truth.

Where do transitions occur?

- Inside if / elif blocks.
- Transitions are implicit, not declared.

Can you trace execution after 10 steps?

- Not reliably.
- Control flow depends on random decisions + nested conditionals.

Conclusion:

- This works but is structurally opaque.
- Debugging requires reading the entire loop.




# Lab 2 Notes (state_machine_manual.py)

State Storage:

- Single explicit variable `state`
- Always one of: START, THINKING, ACTING, DONE, FAILED

Transitions:

- Defined explicitly in code
- No hidden or side-effect-based transitions

Execution Traceability:

- Every state transition is printed
- Full execution path is visible

Termination:

- DONE and FAILED are terminal states
- Execution stops deterministically

Key Takeaway:

- Control flow is explicit and debuggable
- This is the correct structural model for agents
- LLMs should operate inside this, not replace it


# Lab 3 Notes

What changed?

- States are explicit.
- Transitions are validated.
- LLM does NOT control execution.
- Terminal states stop the system.

Why this matters:

- No implicit loops
- No hidden transitions
- Execution is inspectable
