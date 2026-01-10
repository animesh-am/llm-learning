#### What is LangChain?

LangChain is a Python/JS framework for building LLM-powered applicationsby giving us:

- fewer repeated patterns
- composable building blocks
- standardized interfaces around prompts, models, and outputs

LangChain exists because the raw LLM APIs are too low-level for real systems.

If we directly build on OpenAI / Anthropic APIs, we repeatedly write:

- prompt formatting
- model invocation logic
- output parsing
- retries & error handling
- chaining multiple LLM calls
- swapping models later

We also should also consider what LangChain can no achieve:

- It does not make LLMs smarter
- It does not improve reasoning
- It does not replace system design
- It does not fix bad prompts

**_Langchain thus optimizes developer experience, not intelligence._**

#### The problem that LangChain solves:

1. **Boilerplate Reduction**
   Without LangChain, every LLM starts like:

   ```python
   prompt = f"""
   Summarize this text in 3 bullet points:
   {text}
   """

   response = openai.chat.completions.create(
       model="gpt-4o-mini",
       messages=[{"role": "user", "content": prompt}],
       temperature=0.3
   )

   output = response.choices[0].message.content

   ```

   Now repeat this across: files, prompts, models, teams

   LangChain helps here by packaging common LLM usage patterns into reusable abstarctions:

   ```python
   from langchain.prompts import PromptTemplate
   from langchain.chat_models import ChatOpenAI
   from langchain.chains import LLMChain

   prompt = PromptTemplate(
       template="Summarize this text in 3 bullet points:\n{text}",
       input_variables=["text"]
   )

   llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

   chain = LLMChain(llm=llm, prompt=prompt)

   chain.run(text=my_text)

   ```

   So the prompts are reused cleanly and the model config is centralized.

2. **Composability**

   Real LLM apps are rarely a single prompt. They will rewrite the user input, classify the intent, format context and generate final response.

   LangChain takes LLM logic as composable steps. Each steps takes a structured input, produces structured output and can be chained pedictably.

   Example: Simple Multi-Step Chain

   ```python
   rewrite = LLMChain(llm=llm, prompt=rewrite_prompt)
   classify = LLMChain(llm=llm, prompt=classify_prompt)
   answer = LLMChain(llm=llm, prompt=answer_prompt)

   final_output = answer.run(
       context=classify.run(
           text=rewrite.run(text=user_input)
       )
   )

   ```

3. **Standard Interfaces**

   LangChain helps swap models without rewriting our app.

   LangChain standardizes:

   • `PromptTemplate` → input formatting

   • `LLM / ChatModel` → inference

   • `OutputParser` → structured results

   So today if we are using OpenAI. And tomorrow we want to use Anthropic, we can do effortlessly.

```python
llm = ChatAnthropic(...)
# or
llm = ChatOpenAI(...)
# or
llm = ChatOllama(...)

```

#### LangChain LLM Wrappers

In LangChain, a LLM wrapper is just a Python (or JS) class that knows:

- how to call a model
- how to format inputs
- how to format outputs

```plaintext
Your code → LangChain wrapper → HTTP request → Model API → HTTP response → LangChain → Your code

```

LangChain helps in LLM abstraction. It exposes a commpn interface regardless of what the backend is:

```python
llm.invoke("prompt text")
```

Behind the scene the wrapper converts this code into prover-specific code. Providers could be: OpenAI, Hugging Face, Ollama, etc.

For example:

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    max_tokens=256
)

```

This is equivalent to curl JSON body:

```json
{
  "model": "gpt-4o-mini",
  "temperature": 0.2,
  "max_tokens": 256
}
```

Also, passing of prompts:

```python
llm.invoke("Summarize this text")
```

becomes this:

```json
{
  "messages": [{ "role": "user", "content": "Summarize this text" }]
}
```

And structured prompts like this:

```python
from langchain_core.messages import SystemMessage, HumanMessage

messages = [
    SystemMessage(content="You are a precise assistant."),
    HumanMessage(content="Explain transformers.")
]

llm.invoke(messages)

```

becomes this:

```json
{
  "messages": [
    { "role": "system", "content": "You are a precise assistant." },
    { "role": "user", "content": "Explain transformers." }
  ]
}
```

TO MAP THIS INTO curl CALLS:

| Your Mental Model | LangChain Term  |
| ----------------- | --------------- |
| curl command      | LLM wrapper     |
| JSON body         | Model config    |
| messages[]        | Prompt/messages |
| system prompt     | SystemMessage   |
| user input        | HumanMessage    |
| response text     | `.content`      |

### PromptTemplate in LangChain

PromptTemplate is a parameterized prompt text. It produces a final string prompt using the **\*template + variables** at runtime.

```python
prompt = f"""
You are a helpful assistant.
Answer the question: {question}
"""

```

In LangChain, a PromptTemplate must decalre its input up front. Example:

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["topic"],
    template="Explain {topic} in simple terms."
)

```

So the statement:

```python
final_prompt = prompt.format(topic="transformers")

```

Will become:

```plaintext
Explain transformers in simple terms.

```

**PromptTemplate vs ChatPromptTemplate**

PropmptTemplate renders one string

ChatPromptTemplate renders a list of role-bsaed messages.

### Chains in LangChain

A chain is a structured sequence of steps where:

- Each step does one clearly defined job
- The output of one step becomes the input of the next
- The order is fixed
- The responsibilities of each step are narrow and clear

Instead of giving a long prompt like:

> “Read this text, summarize it, extract entities, classify sentiment, and give advice”

You break it into **steps** :

1. Step A: Summarize
2. Step B: Extract entities from the summary
3. Step C: Classify sentiment from the summary
4. Step D: Generate advice from structured outputs

Using Chains is safe as:

- Reduces prompt injection as if someone touches on step, can not got to the next step.
- It produces smaller cognitive load per step.
- Easier validation as we can specify what a step would output
- Chains fail locally, so easy to debug

**LangChain** does not guarantee that an LLM will reason correctly, logically, or step-by-step. What LangChain does is: it passes inputs to LLM, and routes outputs to next step.

In LAB for Ollama with LangChain, we see we not explicitly mention:

- URL (`http://localhost:11434`)
- No JSON payload construction
- No manual response parsing (`response.json()["response"]`)
- Thus we lost the visibility how the model is called.

Abstractions added by LangChain:

- OllamaLLM: wraps the Ollama API and hides request / response
- PromptTemplate: Makes string fromatting as formal object
- .invoke(): It provides a unified interface across models, tools, chains

Suppose if we tweak some changes in the prompt:

```plaintext
Remove “Respond with only one word”

Increased temperature (more randomness)
```

The outputs could be:

```
The sentiment of the text appears to be positive.

```

```
POSITIVE 😊
```

It actaully deviates from what we needed.
