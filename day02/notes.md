**Why LLMs are bad at JSON by default?**

JSON (Javascript Object Notation) is  a rigid, brittle, punctuation-obsessed format, and large-language models are probalistic text generators that never cared for commas like that.

Long story short, LLMs are trained to predict the next token that looks statistically plausible given everything that came before. They are excellent at producing language-like continuations. JSON is not a language; it's a formal like a formal grammar.

First problem: When an LLM opens a `{`, it does not truly know it has to close later. It has no stack or a parser. It just knows that often a `}` follows eventually.

Second problem: LLMs are rewarded during training for being flexible, expressive, and context-sensitive. JSON demands the opposite: exact quotes, exact commas, no comments, no trailing commas, no extra text.

Third problem: A compiler rejects invalid JSON instantly. An LLM has no rejection step. Once a bad token is emitted, it keeps going confidently.

That is the reason why we need to define ***structured output*** in LLMS.

A bad prompt:

```plaintext
Return a user profile in JSON.
```

Result:

```json
{
  "name": "Alice",
  "age": "25 years",
  "hobbies": ["reading", "coding"],
  "note": "Let me know if you want changes!"
}
```

We don't need `"note"` and we only needed age as  a number.

Good structured prompt:

```json
Return a JSON object with EXACTLY these keys:
- name: string
- age: number
- is_active: boolean

No additional keys are allowed.

```

Expected output:

```json
{
  "name": "Alice",
  "age": 25,
  "is_active": true
}

```

Weak instruction: `Please return valid JSON.`

Strong instruction:

```diff
Rules:
- Output ONLY JSON
- No explanations
- No comments
- No markdown
- No trailing text
- No extra keys

```

Proper prompt for all of the above would be like:

```yaml
Task:
Generate user data.

Schema:
- name: string
- age: number
- is_active: boolean

Rules:
- Output ONLY JSON
- No extra keys
- No text outside delimiters

Output format:
<json>
{VALID_JSON_HERE}
</json>

```

#### **Determinism vs Reliability in LLMs**

**Determinism →** same input + same setting ≈ same output

**Reliability →** Output is correct, valid, and usable

`Determinism does not imply correctness.`

* LLMs always samples tokens from a probability distribution
* Temperature only sharpens the distribution; it never removes sampling
* The highest probability token can still be wrong.
* Thus at low temperature, the model will repeat the same mistake consistently
* Errors become determinist

For example:

Schema expects: `"age": number`

Model bias: `"age": "25"`

Low temperature may generate 25 always.

This matters a lot in building Agents as they rely on:

* chained generations
* tool calls
* state passing
* self-feedback loops
