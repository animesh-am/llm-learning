#### What is LangChain?

LangChain is a Python/JS framework for building LLM-powered applicationsby giving us:

* fewer repeated patterns
* composable building blocks
* standardized interfaces around prompts, models, and outputs

LangChain exists because the raw LLM APIs are too low-level for real systems.

If we directly build on OpenAI / Anthropic APIs, we repeatedly write:

* prompt formatting
* model invocation logic
* output parsing
* retries & error handling
* chaining multiple LLM calls
* swapping models later

We also should also consider what LangChain can no achieve:

* It does not make LLMs smarter
* It does not improve reasoning
* It does not replace system design
* It does not fix bad prompts

***Langchain thus optimizes developer experience, not intelligence.***

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
