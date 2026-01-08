First of all run the Ollama model

```
ollama run llama3.1:latest
```

Paste the following prompt:

```yaml
You must output ONLY valid JSON.

Schema (no deviations allowed):
- animal: string
- diet: string
- dangerous: boolean
- confidence: number

Rules:
- Output ONLY the JSON object
- No explanations
- No markdown
- No comments
- No extra keys
- No text before or after JSON

If any rule is violated, the output is invalid.

Return the JSON now.

Generate 5 dummy data based on the above.
```

Output at:

[structured output](D:\Animesh\Projects\llm-learning\day02\structured_output.json "open")
