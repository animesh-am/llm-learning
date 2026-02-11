Day 13 was about correct agent skeleton, explicit flow control, safe module boundaries and clean termination.

> But a correct system can fail silently.

Day 14 answers:
> 1. How to understand the agent is failing?
> How to know how it failed?
> How to know if it's getting worse over time?

### Types of Failure in Agent Systems
#### 1. Silent Failure
Definition: 
- The system returns an answer
- No error is thrown
- The answer is wrong or useless

This is dangerous because:
- It looks successful
- Metrics may show "success"
- Users lose trust slowly

For example:
- RAG retrieves irrelevant docs
- LLM answers confidently
- No exceptions raised

#### 2. Partial Success
Definition:
- System completes
- Some components worked
- Some failed or degraded

For example:
- Tool executed, but wrong branch chosen so the agent stopped early

#### 3. Wrong Confidence
Definition:
- The model expresses certainty
- But reasoning is flawed.
LLMs always sound confident.

#### 4. Infinite Retries
Definition:
- Retry logic cycles untill time
- System technically works but wastes time and resources

#### Degraded Quality over time
Definition:
- Agent works initially
- Retrieval quality declines
- Prompt drift occurs
- Model behaviour shifts

### Why Agents fail without throwing Errors?
LLMs always return something, even if the answer is wrong. They never  crash when unsure, or raise syntax errors.
This happens because LLMs optimize for fluency, not truth or correctness.
So the system may be:
- structurally correct, yet logically wrong
- silently degrading

### Observability vs Logging

Logging:
- records events
- prints statements
- writes files

Example:
```text
Decision: ANSWER
Tool: CALCULATOR
State: retries=1
```

Logging tells you what happened.


Observability lets you:
- reconstruct execution paths
- inspect state transitions
- reason about behavior over time
- detect patterns of failure

We need:
1. State Snapshots
    - What was the state at each node?
    - What changed?
2. Decision Traces
    - What did the LLM decide?
    - What branch was taken?
3. Path Visibility
    - Which nodes executed?
    - Where did it terminate?


### Evaluation is not only Accuracy
Most people evaluate agents like classifiers. This is incomplete as Accuracy only measures:
- Did the final answer match expectation?

But production grade evaluation asks:
- Did it stop correctly?
- Did it choose the right branch?
- Did it respect retry limits?
- Did it avoid unsafe tools?
- Did it fail safely?
- Did it stay within constraints?

> Evaluation in agent systems is about behaviour, not just outputs.


### Why LangGraph enables Observability
Traditional while-loops:
- hide transitions
- hide retries
- hide state mutation
- hide execution path

You only see prints.

**LangGraph gives**:
- explicit nodes
- explicit edges
- explicit transitions
- explicit state at each step

This makes:
- failure inspectable
- retries visible
- path traceable
- termination deterministic

So,
> Graphs don't prevent failure. They make failure observable. And an observable failure is fixable failure.




### Lab 1:
Failure modes were enumerated at design time.
This exposes weaknesses before runtime.

### Lab 2:
Instrumentation added:
- Execution path tracking
- State snapshot per node
- Transition timestamps

No business logic was modified.
Agent can now explain its behavior.

### Lab 3:
Failure injection tested:
- Ambiguous inputs
- Tool errors
- Bad retrieval
- Conflicting intent
- Retry exhaustion

Observed:
- Some failures are silent (quality degradation)
- Structural failures are detectable
- Agent terminates safely in most cases

Key Insight:
Failure is inevitable.
Silent failure is preventable with observability.

