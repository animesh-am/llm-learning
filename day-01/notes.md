### What is LLM?

LLM stands for large language model. It is a **very large probabilistic machine whose only job is to predict the next token** given previous tokens.

**Tokens:** A token is a chunk of text. Sometimes it is a word, sometimes punctuation, sometimes whitespace.

For example:

```bash
"cat" --> one token
"unbelievable" --> might split into "un", "bel", "ievable"
"ChatGPT" --> "Chat" and "GPT"
```

Go to this link and find out the nimber of tokens for any sentence.

[LLM Token Counter](https://platform.openai.com/tokenizer)

The model never understands the meaning. It only sees sequences of tokens and learns how those sequences tend to continue.

**Training on Text:**

During training, an LLM is shown massive amounts of text: books, articles, code, conversations, documentation, all mixed together. The training task is simple:

`Given N tokens, predict the next; i.e; N+1 th token.`

If the training data contains:

- Facts → the models learn factual pattern.
- Lies → it learns those patterns too
- Logical arguments → it learns to shape logic
- Bad reasoning → it learns that as well

**Probability Distribution:**

At each step, the model outputs a **probability distribution** over all possible next tokens.

It generates a ranked list like:

- "is" → 42%
- "was" → 18%
- "seems" → 9%
- "banana" → 0.003%

One token is sampled, appended to the input and the process continues.

Actually, the model does not plan ahead that it is going to reply in a certain way. It does not know where the sentence is going. The worst part is it does not know if it contradicted itself two paragraphs ago.

---

##### Training vs Inference in LLMs

**_Training_ **is the process of learning the model's parameters (weights).

- **Input:** is massive text datasets (trillions of tokens)
- **Objective:** Minimize prediction error for next token prediction
- **Output:** a fixed set of numbers (weights), often billions or trillions of parameters

After the training is done the model is frozen, the weights do not change. This is the model we download or can access via API.

For the training huge GPU/TPU clusters are needed in data centers and may need months to compute.

This is what happens during training:

1. Take a chunk of text → tokenize it
2. Predict the next token
3. Compare prediction vs actual token
4. Compute error (loss)
5. Backpropagate error
6. Update weights
7. Repeat it trillions of times

This is what is **_Gradient Descent_**.

**Inference** is simply running the trainrd model.

- **Input:** Tokens that we provide (prompt + context)
- **Output:** Probability distribution of next token
- **No learning or updating.**

What we can control during inference?

- Prompt
- Context window
- System instructions
- Sampling parameters

  - temperature
  - top-k
  - top-p

- Tool calling
- Retrieval (RAG)
- Memory (external, not model weights)

---

##### What is Ollama?

Ollama is a software that:

- Loads already-trained language models
- Runs them locally on your machine
- Executes inference only

`For analogy: Ollama to LLMs is what Docker is to containers.`

---

##### Prompt vs System Prompt

**System Prompt** defines the _behaviour_:

- Who the model is
- What it is allowed to do
- What it must never do
- Output constraints
- Safety boundaries
- Reasoning style
- Tool usage rules

For example: `"You are ecommerce chatbot. Never disrespect any customer. Always respond in light hearted way."`

**User Prompt**

- Requests an action
- Asks a question
- Supplies data
- And most importantly, it has to operate inside the system contraints.

For example: `"What is the price of 10 units of cotton saree?"`

**Prompt Injection:**

It occurs when user input is treated as instructions instead of data and alters the behaviour unintentionally.

---

##### Temperature in LLMs

Temperature is a scalar applied to the model’s logits that reshapes the probability distribution before sampling.

It does **not** :

- Add creativity
- Add intelligence
- Add new information

It only changes **how probabilities are sampled**.

- Deterministic tasks → low T (≈ 0–0.3)
- Structured outputs → low T
- Brainstorming → moderate T (≈ 0.7)
- Exploration → higher T (with constraints)

##### Top-k and Top-p Sampling in LLMs

After temperature reshapes probabilities, you still have:

- A long tail of garbage tokens
- Rare tokens with tiny but non-zero probability
- Failure modes caused by “technically possible” tokens

Top-k and top-p are **hard constraints on the sampling space** .

They decide **which tokens are even allowed to be sampled** .

**Top-k** keeps only the k highest-probability tokens and discards the rest. Everything outside the top-k set is assigned probability zero.

Given sorted probabilities: `p1 ≥ p2 ≥ p3 ≥ ... ≥ pN`

Keep: `{p1, p2, ..., pk}`

Discard: `{pk+1, ..., pN}`

This truncates the tail.

**Top-p** keeps the smallest set of tokens whose cumulative probability ≥ p. The number of tokens kept is dynamic.

Sort probabilities: `p1 ≥ p2 ≥ p3 ≥ ... `

Find smallest n such that: `Σ(i=1..n) pi ≥ p`

Keep tokens `{p1 … pn}`, discard the rest, then renormalize.

It keeps most of the probability mass.

| Aspect              | Top-k       | Top-p         |
| ------------------- | ----------- | ------------- |
| Token count         | Fixed       | Dynamic       |
| Context sensitivity | None        | High          |
| Tail control        | Hard cutoff | Probabilistic |
| Stability           | Lower       | Higher        |
| Modern default      | Rare        | Common        |
