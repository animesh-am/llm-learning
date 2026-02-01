### Why LLMs Are Bad at Acting

LLMs are **text predictors**, not actors.
They generate *descriptions* of actions, not the actions themselves.

> LLMs can describe actions, not perform them.

Reasoning ≠ execution.

---

#### 1. LLMs Hallucinate Outputs

LLMs don’t check reality.
They predict what a *plausible answer* looks like based on training data.

Example

```text
User: I deleted the file. Is it gone now?
LLM: Yes, the file has been successfully deleted.
```

Reality:

* The LLM has **no access** to your filesystem
* It **guessed** a confident response

#### 2. LLMs Cannot Verify Side Effects

Actions change the world.

LLMs cannot observe those changes unless **explicitly told** via tools or feedback.

Example

```plaintext
User: Did you send the email?
LLM: Yes, the email was sent successfully.
```

Reality:

* No SMTP call
* No delivery status
* No error handling

#### 3. LLMs Lie Confidently About Actions

LLMs optimize for  **coherence** , not truth.

Confidence is a writing style, not evidence.

Example:

```plaintext
LLM: I have updated the database and restarted the server.
```

Reality:

* No DB connection
* No server
* No restart

### What is a Tool in LLM Systems

A tool in LLM system is :

* a normal deterministic function
* exceuted by the code
* never eecuted by the model

The model only decides which tool to use and supplies arguments (structured data, usually JSON)

Example:

```python
def get_weather(city: str) -> dict:
    return {"city": city, "temp_c": 32}
```

Models output:

```json
{
  "tool": "get_weather",
  "arguments": {
    "city": "Bangalore"
  }
}
```

The flow:

1. Model emits structured text
2. Your code parses it
3. Your code calls `get_weather("Bangalore")`
4. Result is sent back to the model
5. Model continues reasoning with new data

Properties of tools:

* Tools are deterministic: same input ==> same output
* Tools are stateless unless you add state
* Tools can fail - the model must handle that
* Tools extend capabilities

### Tool calling vs Prompt Tricks

Prompt only approach:

```plaintext
"Calculate 123 * 456"
```

Tool based approach:

```python
calculator(123, 456)
```

They look similar but they are not.

In prompt approach:

* The model *predicts* the most likely text sequence
* Arithmetic is treated like language
* Output is probabilistic
* Usually right for small numbers
* Quietly wrong at scale or under pressure

In tool call approach:

* The model delegates the task
* A real function runs
* Output is deterministic
* Always correct (unless your code is broken)



When Prompt Tricks Are Acceptable:

* Rough estimates
* Toy demos
* Non-critical reasoning
* Educational explanations

When Tools Are Mandatory:

* Math
* Dates & time
* Money
* IDs
* Database queries
* External state


### Why tools come after RAG?

Order:

```plaintext
Dataflow (LCEL) → Knowledge (RAG) → Actions (Tools)
```

**Step 1: Dataflow (LCEL)**

This defines how information moves.

* inputs
* branching
* retries
* memory boundaries
* tool writing

**Step 2: Knowledge (RAG)**

RAG reduces uncertainty.

* fetch relevant context.
* narrow the probability space

**Step 3: Actions (Tools)**

Tools are side effects.

* database writes
* API calls
* file ops
* payments
* emails
* irreversible behaviour

If you reverse the order:

**Tools before RAG**

* model acts on incomplete knowledge
* wrong actions with high confidence

**Tools before dataflow**

* execution paths unclear
* race conditions
* retries cause duplicate side effects


### Failure Modes of Tool Use

##### 1. Wrong Tool Selection

The model chooses a tool, not *the right* tool.

Common causes:

* ambiguous tool descriptions
* overlapping responsibilities
* vague naming (`process_data`, `handle_request` — useless)

##### 2. Bad Arguments

The model emits:

* missing fields
* wrong types
* malformed JSON
* logically invalid values

Example:

```json
{
  "user_id": "abc",
  "amount": -5000
}

Syntactically valid. Semantically insane.

```

##### 3. Overuse of Tools

When everything looks like a tool, the model:

* calls tools for trivial reasoning
* loops endlessly
* inflates latency
* burns tokens and money

Things can go like:

> tool → model → tool → model
>
> with no state change

This can me mitigated by putting on:

* clear guidance on when not to use tools
* max tool-call limits
* require justification for repeated calls


##### 4. Tool Hallucination

The model confidently calls:

```python
send_email_v2_pro()
```

But we never wrote that funtion. This can happen when:

* tools described in natural language
* similar names in training data
* weak rejection handling

To mitigate this:

* hard allow-list of tools
* reject unknown tool names
* treat hallucinated tools as a reasoning error, not a crash


**Lab 1 (tool_baseline_no_tools.py) — Observations**

What did the model pretend to do?

- It pretended to calculate math but actually guessed via pattern recall.
- It pretended to know the current system time despite having no access to a clock.
- It pretended to call an external API and returned fabricated data.

Key Insight:

The model does not execute actions.
It produces text that resembles the *result* of actions.

Confidence ≠ correctness.

Conclusion:

Without tools, the LLM is role-playing competence.
This is acceptable for language.
It is unacceptable for systems that must be correct.


**Lab 2 (tools.py) — Observations**

Tools are not smart.
They are correct.

Their value comes from:

- determinism
- testability
- trust

The LLM does not improve these tools.
These tools constrain the LLM.



Lab 3 — Observations

The LLM does not run tools.
It proposes tool usage.

All power lives outside the model:

- tool allow-lists
- argument validation
- execution timing

This transforms the LLM from an actor into a planner.
