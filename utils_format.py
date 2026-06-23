"""
Utilities for presentation formatting (thousand separator for Chilean locale).
Keep all business logic numeric types as ints; this module only formats for display.
"""

def formato_moneda(n: int) -> str:
    """Return integer n formatted with dot as thousands separator (e.g. 400000 -> '400.000').
    If n is None or not an int, returns the string representation.
    """
    try:
        return f"{int(n):,}".replace(",", ".")
    except (TypeError, ValueError):
        return str(n)
