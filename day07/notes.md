### Retrieval-Augmented Generation (RAG)

**Retrieval-Augmented Generation (RAG)** is a pattern where:

- external data is **retrieved at query time**
- and **injected into the model’s prompt**
- to help generate a better response

Nothing is learnt. Nothing is stored. Nothing is remembered.

##### Retrieval ≠ Generation

These are two separate steps. Mixing them up causes most confusion.

###### Retrieval

- Finds relevant data from an external source(vector DB, search index, SQL, files, APIs)
- Happens outside the LLM
- Output = raw text or structured data
- For example: `User question → embedding → vector search → top 5 documents`

###### Generation

- The LLM produces text
- Happens after retrieval
- Uses retrieved data only because it is placed in the prompt
- Example: `Prompt = system instructions + retrieved docs + user question`

So, if the retrieval fails, generation still happens - just with worse input.

After the response is generated:

- the model forgets everything
- the next request starts clean

RAG works by **injecting retrieved content at query time**.

That injection usually looks like this:

```
System Prompt:
"You are a helpful assistant..."

Context:
	<Document 1>
	<Document 2>
	<Document 3>

User Question:
"What is our internal leave policy?"
```

It will:

* retrieve HR policy doc
* inject doc into prompt
* LLM answers using provided policy

Some common industy lies:

```
- “RAG gives the model memory” → false  
- “RAG trains the model on your data” → false  
- “RAG replaces fine-tuning” → false  
- “RAG makes the model smarter” → false  

RAG makes the **inputs better**, not the model.
```

#### What are Embeddings?

An embedding is a numerical representation of meaning. Technically, embeddings turn text into vectors so meaning can be compared with math. `Text → Vector`

"Refund policy for enterprise customers"

    ↓

[0.021, -0.884, 0.113, ..., 0.447]

Key points for embeddings:

* Output is a **fixed-length vector** (e.g., 384, 768, 1536 numbers)
* Each number has **no human meaning by itself**
* Meaning exists only in the **relative position** between vectors

```
Same text → almost same vector  
Similar text → nearby vector  
Unrelated text → far-away vector
```

Retrieval is just:

```
question vector
	vs
stored document vectors
	↓
find the closest ones
```

It is based on **Semantic Similarity.** For example:

```
Query: "vacation policy"
Doc: "employee leave guidelines"
→ may not match

This is where semantic search comes to rescue
Both map to **nearby vectors** because they express similar ideas.

That’s semantic similarity:
- Similar meaning
- Different words

This is why embeddings outperform traditional search for RAG.
```

**Cosine Similarity**

> Are these vectors pointing in the same direction?

- Measures the **angle** between vectors
- Ignores vector length
- Good default for text

**Dot Product**

> How strongly do these vectors line up?

- Measures alignment **and** magnitude
- Faster in some systems
- Often used when vectors are already normalized

**Euclidean Distance**

> How far apart are the points?

- Straight-line distance in space
- Sensitive to scale
- Rarely preferred for modern embeddings

You usually **do not choose** the metric freely.

- Embedding model → expected metric
- Vector DB → optimized metric

Mismatch = degraded retrieval.
This is a silent failure and very common.

For example:

```
Docs:
A: "How to request paid leave"
B: "GPU memory optimization tricks"
C: "Holiday and vacation rules"

Query:
"What's the leave policy?"

Embedding search result:
A (closest)
C
B (far away)
```

The most important thing is the system never understood leave. It just compared vectors.

What Embeddings Are NOT

- Not keywords
- Not summaries
- Not probabilities
- Not knowledge storage

They are **coordinates in meaning-space**.

RAG depends on embeddings because:

- retrieval needs similarity
- similarity needs vectors
- vectors come from embeddings

#### What are Vector Stores?

Vector stores store vectors in database. A **vector store** is a database optimized to:

- store embedding vectors
- index them efficiently
- return the most similar ones for a query vector

Why plain databases fail?

Raw embeddings look like: `[0.021, -0.884, 0.113, ..., 0.447]`

If you store millions of these:

- brute-force comparison becomes slow
- latency explodes
- cost explodes

So vector stores build **indexes**. Although it is not accurate but its fast with close results.

**Similarity Search**

Given:

- query vector `q`
- stored vectors `v1, v2, v3, ...`

The vector store:

- computes similarity using a distance metric
- ranks vectors by closeness
- returns the best matches

We ask for top-k = k most similar vectors

top-3 results:

1. Doc A (0.92 similarity)
2. Doc C (0.89 similarity)
3. Doc F (0.85 similarity)

```
Typical values:
- `k = 3–5` for short answers
- `k = 5–10` for complex questions

Bigger `k` ≠ always better.  
Context window limits still exist.
```

Documents

    → embeddings

    → vector store (index + storage)

User query

    → embedding

    → similarity search (top-k)

    → retrieved text

    → prompt injection

    → LLM response

#### RAG vs Memory

RAG and memory solve different problems.

> RAG adds information only for certain request.
>
> Memory changes behaviour across request.

Example of memory:

```
User: I prefer short answers.
(User preference stored)

Later when asked: 

User: Explain transformers.
→ Model answers briefly because of past memory
```

Example of RAG:

```
Query: "What is our leave policy?"
→ Retrieve HR document
→ Inject into prompt
→ Answer generated
→ Context discarded
```

> Memory keeps accumulating and old data never expires unless explicitly managed.
>
> But, RAG works on a bounded dataset. If we get some wrong information, we can update the documnet or re-embed.

> Memory is often stored as free text blobs
>
> ```
> "User likes Python. Mentioned GPUs once. Works in finance."
> ```
>
> For RAG, data is chunked intentionally. And data is retrieved when it matches the query.
>
> ```plaintext
> Chunks:
> - Leave policy
> - Remote work policy
> - Expense reimbursement
>
> Query: "How many leaves do I get?"
> ```

> Memory causes drift over time. The answers gets personalized and the debugging becomes impossible.
>
> RAG - retrieval is tied to the query and only relevant chunks are injected.
>
> ```
> Every response is:
> (system prompt)
> + (retrieved context)
> + (current question)
>
> Same input ==> Same output
>
> RAG pipeline
> Documents → embeddings → retrieval → prompt → answer
> (No feedback loop)
> ```

#### How RAG can fail?

If the retrieval is bad, generation will still happen and the model answers with junk.

**Irrelevant Retrieval:** The vector search returns documents that are technically similar but contextually wrong. Example:

```plaintext
Query: "leave policy"
Retrieved:
- "Medical leave guidelines" (ok)
- "Leave the package at the security" (very bad)
```

The model confidelntly answers using wrong source.

**Chunking errors:** Documents are split poorly and thus the meaning is broken across chunks.

```
Bad Chunk:
"...Employees are entitled to 24 days of annual leave if..."

Next Chunk:
"...they have completed one year of service."
```

The retrieval may fetch only the half idea.

**Over-Retrieval:** If we assume "more context = better answer" and retrieve too many chunks then we are wrong.

Example: `top_k = 15`

The information is diluted with contradictory data, and the important facts are buried.

**Prompt Overload:**

We have the:

* system prompt
* developer instructions
* safety rules
* retrieved documents
* user question

Everything sent together and we get unpredictable answers.

## Lab 1: Stateless Baseline (No Context)

### What was missing?

- No access to internal documents
- No retrieval step
- No grounding data

### What happened?

- The model still answered
- The answer sounded confident
- The content was generic or guessed

### Key Insight

LLMs do not know when they don’t know.

Without retrieval:

- generation still happens
- hallucination risk is maximal
- confidence is misleading

This baseline proves why RAG is required.



## Lab 2: Embeddings + Vector Store

### What was added?

- Document embeddings
- Vector index (FAISS)
- Similarity-based retrieval

### What is NOT happening?

- No LLM generation
- No prompt injection
- No memory

### Key Insight

If retrieval is wrong here,
adding an LLM later will only make the wrong answer sound better.



## Lab 3: Context Injection via RAG

### What changed?

- Retrieved documents injected into the prompt
- LLM constrained to provided context

### What stayed the same?

- Stateless execution
- No memory
- No persistence

### Key Insight

RAG works by improving inputs, not by changing the model.
If retrieval is wrong, the answer will still be wrong—just more confidently phrased.



## Lab 4: RAG vs Memory (State Comparison)

### Experiment Setup

We asked the system three questions in sequence:

1. **Factual question** (answer exists in retrieved documents)
2. **Contradictory question** (conflicts with earlier answer)
3. **Unrelated question** (no overlap with previous topics)

The RAG pipeline was unchanged between questions.
No memory component was added.
Each query ran independently.

---

## Observations

### 1. Does knowledge persist?

**No.**

- The system did not “remember” earlier answers
- Each response depended only on:
  - the current query
  - the documents retrieved for that query

When the factual question was asked again later, the system recomputed retrieval from scratch.

This confirms:

> RAG does not persist knowledge across requests.

---

### 2. Does it drift?

**No.**

- Earlier answers did not influence later ones
- No reinforcement of mistakes
- No gradual behavior change

Contradictory questions were answered strictly based on newly retrieved context, not prior responses.

There was no accumulation of bias, preference, or state.

---

### 3. Does it reset cleanly?

**Yes. Completely.**

Each query behaved as if it were the first request:
