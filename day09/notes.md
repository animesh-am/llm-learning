### What is an Agent?

An agent is `a loop with state and decision logic.`

- **State:** _memory carried across iterations_
- **Decision Logic:** _code that chooses the next action_
- **Loop:** _repeated execution untill a stop condition is met._

Agents does not: `think, reason like humans, or plan  autonomously.`

For example:

```python
state = {}

while True:
    observation = observe_environment()
    action = decide(state, observation)
    result = act(action)
    state = update_state(state, result)


```

- If we remove the _loop_ ==> it's just a function
- If we remove the _state_ ==> it's just a stateless pipeline
- If we remove _decision logic_ ==> it's automation, not an agent

#### Agent Loop Anatomy

```
observe
→ decide
→ act
→ observe result
→ repeat or stop

```

1. **Observe**
   - Read inputs (user prompt, tool output, environment state)
   - No intelligence here - pure data ingestion
2. **Decide**
   - Select next action based on:
     - current state
     - latest observation
   - This is where an LLM is often _consulted_
3. **Act**
   - call a tool
   - write output
   - modify state
4. **Observe Result**
   - Capture tool response or execution outcome
   - Feed it back top the loop.

> The loop is deterministic.
>
> Only the model’s suggestions are probabilistic.

#### How can agents be dangerous?

1. **Infinite Loops**
   - Missing or weak stopping conditions
   - Agent keeps “trying again” forever

   Result:
   - Burned tokens
   - Hung processes
   - Unresponsive systems

2. **Tool Spamming**
   - Agent retries failing tools aggressively
   - No backoff, no retry limit

   Result:
   - API bans
   - Cost explosions
   - Rate-limit hell

3. **Self-Reinforcement Errors**
   - Agent trusts its own previous output
   - Wrong assumption becomes “ground truth”
     Result:
   - Confidently wrong behavior
   - No recovery without external intervention

4. **Runaway Costs**
   - Each loop iteration costs money
   - Small bugs scale linearly with time
     Result:
   - ₹500 mistake becomes ₹50,000 overnight

#### Stoppting Conditions for Agent

An agent without a stop rule is a like a denial-f-service attack on yourself.

**Mandatory Stopping Strategies:**

1. Max Steps: Keeps a hard upper bound. And prevents infinite loops.

   ```python
   for step in range(MAX_STEPS):
       ...

   ```

2. Explicit Completion Signal: Agent must declare if the parsing is done or not for better clarity.

   ```json
   { "status": "DONE", "answer": "..." }
   ```

3. Tool Failure:
   If a tool errors repeatedly and returns invalid output. We should stop generating.
4. Confidence Threshold: We should stop when the output certainty crosses a defined bar.
   For example:
   - same conclusion generated 3 times indepently
   - similarity score above threshold.

#### Why LangGraph exists?

The core problem:

> As the agents grow: ad-hoc loops become unmaintainable
> The state becomes implicit and scattered and thus debugging becomes very difficult.

What starts as:

```python
while True:
    ...

```

Turns into nested conditionals and hidden transitions.

LangGraph exists because:

- agents need **explicit state graphs**
- transitions must be **visible**
- execution paths must be **traceable**

## LAB 1 - Naive Agent Loop

Observations & Conclusions

### 1. Looping Behavior

The agent never terminates.
There is no concept of:

- completion
- success
- diminishing returns
- or exhaustion

The model continues generating "next steps" indefinitely, even after it has clearly repeated itself.

Termination is an external concern (human kills process), not an internal capability.

### 2. Repetition

After a few iterations, the agent begins to:

- restate earlier steps
- rephrase the same advice
- oscillate between planning and execution

This happens because:

- the agent has no memory of what "done" means
- the history is unstructured text, not state
- the model optimizes for plausibility, not progress

### 3. Lack of Termination Criteria

The agent has no stopping condition such as:

- goal achieved
- confidence threshold
- action exhaustion
- contradiction detection

As a result:

- progress is never evaluated
- completion is never recognized
- the agent cannot conclude by design

### 4. Confidence Without Progress

The most dangerous behavior observed:

The agent remains confident even when:

- repeating itself
- making no measurable progress
- contradicting earlier steps

The language stays authoritative.
There is no uncertainty signal.

This demonstrates:
LLMs are optimized for confident continuation, not correctness or convergence.

### 5. Core Failure Mode

This baseline agent exhibits the classic failure pattern:

- Infinite planning
- Self-reinforcing verbosity
- No grounding
- No exit

This is the default behavior of an LLM ,mmwhen treated as an "agent" without structure.

Conclusion:
An LLM is not an agent. It is a text generator pretending to be one.

## LAB 2 - Agent with Tools (Simple Version)

### 1. Tools Improve Correctness

With tools, the agent can compute real numbers instead of guessing.

Math results are accurate when tools are used. This reduces hallucination in narrow tasks.

### 2. Tools Do NOT Fix Looping

Even with tools:the agent never stops

- it keeps recalculating
- it re-derives the same numbers

The loop structure is unchanged. The agent has no concept of "done".

### 3. New Failure Modes

New problems introduced by tools:

- Tool overuse:
  The agent calls the calculator repeatedly.
- No verification:
  Tool output is blindly trusted.
- Oscillation:
  Think → calculate → rethink → calculate again.

### 4. Core Lesson

Tools increase power, not control.

The agent still lacks:

- goal completion detection
- stopping conditions
- decision authority

Conclusion:
Tools help agents do things, but they do not help agents decide when to stop.

## LAB 3 - Agent with Explicit Limits

This lab demonstrates why control must live outside the LLM.

### 1. Successful Completion

When provided with:

- sufficient step budget
- sufficient tool budget
- an explicit DONE signal

the agent is able to:

- perform the required calculation
- recognize task completion
- terminate cleanly

Success is:

- explicit
- observable
- unambiguous

This is the first lab where the agent can end correctly without human intervention.

### 2. Forced Termination (Step Limit)

When the maximum step count is too low:

- the agent begins reasoning
- but cannot reach the DONE signal in time

The system halts execution immediately.

Key observations:

- no retries occur
- no hidden continuation happens
- failure is loud and visible

The agent does not adapt.
Control is enforced externally.

### 3. Graceful Failure (Tool Limit)

When tool usage is restricted or removed:

- the agent attempts to use a tool
- the limit is exceeded
- execution stops cleanly

There is no crash and no silent fallback.

This demonstrates graceful failure:

- capability loss is explicit
- the system remains stable
- the reason for failure is clear

### 4. Why Limits Matter

Without limits, previous labs showed:

- infinite looping
- repeated tool usage
- confident non-termination

With explicit limits:

- cost is bounded
- behavior is predictable
- failure modes are controlled

Limits do what prompts and tools cannot.

### 5. Core Insight

LLMs do not self-regulate.

They:

- do not know when to stop
- do not know when they are done
- do not know when they are failing

An agent stops only because the system forces it to stop.

Conclusion:
Autonomy is an illusion without enforcement. Control must exist outside the model.
