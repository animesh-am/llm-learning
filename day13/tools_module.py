def calculator(expression: str) -> str:
    """
    Simple calculator tool.
    """
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        raise ValueError(f"Calculator error: {e}")


def uppercase(text: str) -> str:
    """
    Converts text to uppercase.
    """
    if not text:
        raise ValueError("Text cannot be empty")
    return text.upper()
