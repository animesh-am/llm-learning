def calculator(expression: str) -> str:
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        raise ValueError(f"Invalid calculation: {e}")
