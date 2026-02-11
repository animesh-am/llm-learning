# Day 14 — Failure Modes

## 1. Wrong Tool Chosen
Manifestation:
- LLM selects CALCULATE instead of ANSWER.

Detectable Today:
- Yes (decision trace visible).

Fails Safely:
- Yes (still terminates).

---

## 2. Tool Argument Malformed
Manifestation:
- Calculator receives invalid expression.
- Tool raises ValueError.

Detectable Today:
- Yes (exception thrown).

Fails Safely:
- Yes (execution stops loudly).

---

## 3. RAG Returns Irrelevant Context
Manifestation:
- Context unrelated to query.
- LLM answers incorrectly but confidently.

Detectable Today:
- No (silent failure).

Fails Safely:
- Technically yes (terminates), but incorrect output.

---

## 4. LLM Chooses Invalid Action
Manifestation:
- LLM outputs unknown keyword.

Detectable Today:
- Yes (conditional edges reject).

Fails Safely:
- Yes (no invalid node execution).

---

## 5. Retry Exhaustion
Manifestation:
- Retry counter reaches max limit.
- Agent transitions to FAILED.

Detectable Today:
- Yes (state shows retry count).

Fails Safely:
- Yes (explicit terminal state).

---

## 6. Human Rejects Action
Manifestation:
- HITL node returns REJECT.
- Graph transitions to FAILED.

Detectable Today:
- Yes (path trace shows rejection).

Fails Safely:
- Yes.

---

## 7. Agent Stops Too Early
Manifestation:
- LLM chooses ANSWER without using necessary tool.
- Output incomplete.

Detectable Today:
- Partially (decision trace visible).

Fails Safely:
- Terminates safely, but semantically wrong.

---

## 8. Agent Never Reaches Terminal State
Manifestation:
- Missing END edge.
- Infinite graph loop.

Detectable Today:
- Yes (execution never completes).

Fails Safely:
- No (infinite execution).
