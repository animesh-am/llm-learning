### Stateless vs Stateful Systems

##### What is state?

State = any information stored by a system that affects future behaviour. Formally, if the system output depends on past interractions then the system is stateful.

**Examples of state**

* Conversation history
* Tool call results stored for reuse
* Retrieved documents cached across turns

##### Stateless Systems

A stateless system:

* retains no information between executions
* produces output solely from current input
* has no hidden context
* `output = f(input)`

LCEL pipelines are stateless by default. They have:

* no implicit memory
* no carry-over variables
* so every run is independent

##### Why Stateless systems scale better?

The reason being temporal coupling → Current execution does not depend on past executions. So:

* any machine can handle any request
* failed request can be retried
* multiple requests can run at the same time

##### Why Stateless Systems Debug Better?

Stateless systems provide:

* Input → Output traceability
* Deterministic reproduction
* No hidden or leftover context

##### Why do we need state?

Real LLM applications require:

* Multi-turn conversations
* Context accumulation
* Iterative reasoning
* Partial plans
* Tool results reused over time

So, `an useful LLM can never remain fully stateless.`

##### Stateful Systems

A stateful system retains information across executions and uses it to influence future behaviour.

In LLM systems, this leads to:

* Context bloat
* Prompt drift
* Compounding hallucinations
* Agent loops
* Non-reproducible bugs

This is why we need `chat history`.

So, state must be handled carefully. Pipelines should remain stateless, while state is stored externally and passed in explicitly as input. Naively relying on chat history creates unstructured, implicit state that grows over time, leading to drift, hallucinations, and hard-to-debug behavior. Therefore, LLM memory should be explicit, inspectable, and controlled - not automatically accumulated.


##### What does "Memory" means in LLM systems?

Memory ≠ Learning

* LLMs do **not learn** during inference
* No parameters are updated
* No long-term knowledge is formed


Memory ≠ Model Weights

* Model weights are **static**
* Weights change only during **training or fine-tuning**
* Runtime interactions do not alter weights

Therefore:

* Conversation history ≠ weight update
* Tool usage ≠ learning
* Repeated prompts ≠ adaptation

Memory is actually an external state injected into model as part of the input.

##### Sources of Memory in LLM Systems

Memory can come from:

* Conversation summaries
* Retrieved documents (RAG)
* User profiles
* Past tool outputs
* Cached intermediate results

All of these are:

* Stored outside the model
* Loaded at runtime
* Passed explicitly as input

Relationship to Stateless Pipelines:

* Pipelines remain stateless
* Memory is  data , not internal state
* Same input + same memory → same output

In LangChain, memory is a mechanism to store past interraction data and re-inject into future prompts.

**1. Conversation Buffer Memory**
It stores the entire conversation history.
Past user and assistant messages are appended.
On every turn, the full history is injected into the prompt
Conceptually:

```plaintext
Prompt = system prompt + full chat history + current user input
```

For example:

User asks: "Explain transformers"

Again asks: "Now explain attention again"

The model sees all previous messages and answers with full context.

The problems with this approach could be:

* Context window bloat
* Higher cost
* Prompt drift
* Higher debugging over time

**2. Windowed Memory**

It stores only the last N interactions

Older messages are dropped

And keeps recent context only

Conceptually:

```plaintext
Prompt = system prompt + last N messages + current input
```

Example

If `N = 3`:

* Only the last 3 user–assistant turns are included
* Earlier conversation is ignored

Problems with this approach could be:

* Loss in long-term context
* Still unstructured text
* No semantic understanding of importance


**3. Summary Memory**

Past conversations are summarized

Summary replaces raw chat history

Summary is injected into future prompts

Conceptually:

```plaintext
Old chat → summarizer → compact summary
Prompt = system prompt + conversation summary + recent messages + current input
```

Example

Instead of 50 messages, the model sees:

> “User is learning LLM systems, prefers concise explanations, currently studying memory and state.”

Risks:

* Summaries can omit details
* Errors in summary propagate
* Still external state, not learning


##### Why Naive Memory Fails

Naive Memory = uncontrolled accumulation of past context. It is like growing chat history.

1. **Context Dilution**

Important information gets buried as irrelevant past content grows.

What happens:

* Prompt contains too much text
* Model attention is spread thin
* Relevant signals lose priority

Example:

Early instruction: “Answer concisely”

40 turns later: buried under explanations, tool logs, retries

Model ignores it

Result:

* Lower quality responses
* Inconsistent behavior

2. **Instruction Drift**

Original system instructions slowly lose authority over time.

**What happens**

* Later user messages override earlier constraints
* Model starts following recent tone or style instead of system intent

**Example**

* System: “You are a strict tutor”
* Later chat: jokes, casual language
* Model gradually shifts personality

**Result**

* Loss of role consistency
* Hard-to-explain behavior changes

3. **Self-Contradiction**

Model is exposed to conflicting past statements.

What happens

* Old answers remain in context

* New answers disagree
* Model has no concept of “truth revision”

Example

* Turn 5: “X is correct”
* Turn 20: “X is wrong”

* Turn 30: Model sees both

Result:

* Confused outputs
* Contradictory reasoning

* Hallucinated justifications



4. Runaway Prompt Growth

Prompt size grows every turn without bound.

What happens:

* Token usage increases
* Costs rise
* Latency increases
* Context window limits approached

Example:

* Full chat history appended every turn

* Tool outputs included verbatim
* No pruning or compression

Result:

* Expensive

* Slow
* Eventually breaks when context limit is hit


##### State vs Dataflow

Dataflow

* Controls how execution proceeds
* Determines which steps run, and in what order
* Concerned with control logic

State (Memory)

* Supplies data used during execution
* Does not control flow by itself
* Concerned with stored information


LCEL Perspective

* LCEL controls dataflow

  * Fixed execution graph
  * Deterministic sequence
  * Explicit dependencies
* Memory injects data

  * Loaded as input
  * Does not alter pipeline structure



If memory starts controlling flow:

* Execution becomes history-dependent
* Behavior changes silently
* Debugging becomes impossible
