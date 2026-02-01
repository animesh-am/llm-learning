from datetime import datetime


def add(a: int, b: int) -> int:
  """
    Add two integers.

    Deterministic:
    Same inputs always produce the same output.

    No side effects.
    No validation logic beyond Python typing.
  """
  return a+b


def multiply(a: int, b: int) -> int:
  """
    Multiply two integers.

    Deterministic:
    Same inputs always produce the same output.

    No side effects.
    No hidden state.
  """
  return a*b


def get_current_time() -> str:
  """
    Return the current system time as an ISO-8601 string.

    Deterministic with respect to execution time.
    No arguments.
    Single responsibility.
  """
  return datetime.now().isoformat()