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

* agents need **explicit state graphs**
* transitions must be **visible**
* execution paths must be **traceable**
