### What is LCEL?

LangChain Expression Langauage (LCEL) is a functional pipeline system for orchestrating computation over structure data. It is used to connect blocks like prompts, models, data retrievers and parsers by using  a "pipe" sysmbol (|) so that information flows smoothly from one part to another. Instead of writing complex code, we just stack these blocks in the order we need and LCEL makes sure each step passes its output to the next. It is developed to build AI apps quickly, keep code clean, modular and take advantage of features like parallel processing and easy debugging.

**Runnables**

> It is a callable object that takes an input and produces an output, synchronously or asynchronously, with a standardized interface.


**Common types of Runnable**

| Runnable            | What it does                               |
| ------------------- | ------------------------------------------ |
| PromptTemplate      | Converts structured input → prompt string |
| LLM / ChatModel     | Converts text/messages → model output     |
| OutputParser        | Converts model output → structured data   |
| RunnableLambda      | Arbitrary Python logic                     |
| RunnableMap         | Runs multiple runnables in parallel        |
| RunnablePassthrough | Forwards input unchanged                   |

Example:

```python
from langchain_core.runnables import RunnableLambda

uppercase = RunnableLambda(lambda x: x.upper())

uppercase.invoke("hello")
# → "HELLO"
```

LCEL pipelines pass dictionaries (not loose variables). This is because multiple values may coexist. 

Example: Dictionary in, dictionary out

```python
from langchain_core.runnables import RunnableLambda

add_length = RunnableLambda(
    lambda x: {
        "text": x["text"],
        "length": len(x["text"])
    }
)

add_length.invoke({"text": "hello"})
# → {"text": "hello", "length": 5}

```

**Pipe ( | ) operator**

`A | B` simply means `output_of_A → input_of_B `

For example:

```
prompt | model | parser
```

Equivalent to:

```python
parser(model(prompt(input)))
```

End to end pipeline:

```python
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

prompt = PromptTemplate.from_template(
    "Explain {topic} in simple terms."
)

model = ChatOpenAI()
parser = StrOutputParser()

chain = prompt | model | parser

chain.invoke({"topic": "quantum computing"})
```


**A Runnable** is an object that implements a standard execution interface:

* `invoke()` — single input → single output
* `batch()` — many inputs → many outputs
* `stream()` — input → output chunks over time

> Thus a runnable is an unit of work that knows how to run once, run many times, or stream results.

Actually LCEL does not work because of `|`. It works because every object in the pipeline obeys the same rules.

For example in `invoke`:

```python
prompt.invoke({"topic": "AI"})
model.invoke("Explain AI")
parser.invoke(ai_message)
```

So they have different inputs but same execution method (invoke).

For `batch()`, instead of a loop:

```python
for x in inputs:
    runnable.invoke(x)
```

we write:

```python
runnable.batch(inputs)
```

This helps in parallel execution where possible. For example:

```python
inputs = [
    {"topic": "LLMs"},
    {"topic": "Transformers"},
    {"topic": "Vector databases"}
]

chain.batch(inputs)

```



Now, for `stream()` we run one runnable and yield output incrementally as it becomes available. This is critical fpr chat ui where we have long responses and tool calling agents. For example:

```python
for chunk in model.stream("Explain LCEL"):
    print(chunk.content, end="")
```

Output arrives token by token.

So when we write:

```python
chain = A | B | C
```

LCEL builds a RunnableSequence, whose execution looks like:

```python
invoke():
    output_A = A.invoke(input)
    output_B = B.invoke(output_A)
    output_C = C.invoke(output_B)
```

It is the same for `batch()` and `stream()`.

Now an interesting fact: ***RunnableLambda is just a function.***

```python
from langchain_core.runnables import RunnableLambda

double = RunnableLambda(lambda x: x * 2)

double.invoke(3)
# → 6

```

So, `LCEL is not for LLMs. LLMs just happen to be runnables.`

`Also, we can say that every LCEL component is a Runnable, and every Runnable supports invoke(), batch() and stream().`


##### What PromptTemplate is in relation to LCEL?

A PromptTemplate is a Runnable that:

* Takes a dictionary as input
* Applies deterministic string formatting
* Returns a string

A PromptTemplate supports:

* `invoke()`
* `batch()`
* `stream()`

Example: PromptTemplate as a Runnable

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Explain {topic} in simple terms."
)

prompt.invoke({"topic": "LCEL"})
```

Output :

```plaintext
"Explain LCEL in simple terms."
```

Here, input dictionary: `{"topic": "LCEL"}` and output string: `"Explain LCEL in simple terms."` If keys don't match then execution fails.

Example: Prompt → Model → Parser

```python
chain = prompt | model | parser
```

Dataflows:

```plaintext
dict
 ↓
PromptTemplate (render)
 ↓
string
 ↓
LLM (reason)
 ↓
message
 ↓
Parser (structure)
 ↓
dict / string
```

Batching prompts:

```python
inputs = [
    {"topic": "LLMs"},
    {"topic": "Embeddings"},
    {"topic": "Agents"}
]

prompt.batch(inputs)
```

Output:

```python
[
    "Explain LLMs in simple terms.",
    "Explain Embeddings in simple terms.",
    "Explain Agents in simple terms."
]
```

PromptTemplate technically support `stream()`, but they produce output immediately, also there is nothing to stream.


Why do we use LCEL over chains?

Example of LLMChain:

```python
chain = LLMChain(
    prompt=prompt,
    llm=model
)

chain.run({"topic": "LCEL"})
```

Problem 1: If we try to reuse part of a chain then we have to create nested chains. For example:

```python
chain1 = LLMChain(...)
chain2 = LLMChain(...)

def hacked_pipeline(x):
    a = chain1.run(x)
    return chain2.run(a)
```

Problem 2: With LLMChain we can not easily answer:

* What was the rendered prompt?
* What intermediate data existed?
* What step failed?
* What inputs reached the model?

To handle LCEL introduces an uniform execution interface across all components. Thus, LCEL replaces: `opaque chain → mystery output`

with this: `data → runnable → runnable → runnable → output `

where each step is visible and each step is executable alone.

Example of **Reusability:**

```python
base_prompt = PromptTemplate(...)
reasoning = base_prompt | model

summarize = reasoning | summary_parser
classify = reasoning | classification_parser
```


##### Determinism in LCEL Pipelines

A process is deterministic if `the same input always produces the same output.`

A process is probabilistic if: `the same input can produce different outputs.`

Thus, all orchestration is deterministic, only the model is probabilistic.

What is Deterministic in LCEL?

1. Data routing is deterministic.
   For example:
   If we run this:

   ```python
   chain = prompt | model | parser
   ```

   The execution order is fixed. Prompt always runs first, model always second and parser always third.
2. Input / output transformations are deterministic

   For example: PromptTemplate, RunnableLambda, RunnableMap, RunnablePassthrough, Output parsers all of these behave like pure functions.
3. Branching logic is deterministic

   ```python
   RunnableBranch(
       (lambda x: x["score"] > 0.8, high_confidence_chain),
       low_confidence_chain
   )
   ```

   Given the same input, same branch is chosen.


What is not Deterministic by nature?

LLM outputs are never deterministic.
Even with `temperature = 0, top_p = 1 and same prompt` we can not guarantee identical inputs across time, models, or infrastructure.
Example:

```python
"Explain LCEL briefly."
```

Possible outputs:

* “LCEL is a functional pipeline…”
* “LCEL enables dataflow orchestration…”
* “LCEL allows composable LLM execution…”

A LCEL pipeline:

```python
pipeline = (
    RunnablePassthrough()		  # deterministic
    | RunnableLambda(validate_input)      # deterministic
    | prompt                              # deterministic
    | model                               # 
```


The thing to consider is:

> LCEL pipelines are graphs, no function calls. So we need `RunnablePassthrough` as it gets and sends the input as ouput to the next element in the chain.



What actually is happening in *[lcel_multistep.py](D:\Animesh\Projects\llm-learning\day05\lcel_multistep.py)*

1. **RunnablePassthrough**

   ```python
   {"text": RunnablePassthrough()}
   ```

   Takes raw input and injects it into the prompt under the key `"text"`.
2. **Single LLM call**

   ```python
   | prompt | llm
   ```

   Exactly one model invocation.
3. **Deterministic structuring**

   ```python
   lambda sentiment: {"sentiment": sentiment.strip()}
   ```

   You’re converting unstructured text into a  **machine-friendly object** .
4. **Final formatting step**

   ```python
   lambda data: f"..."

   ```
