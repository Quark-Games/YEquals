"""
extlib made by Michael.

includes sgn()
"""

def sgn0(num: float) -> float:
    """Returns -1 if num is less than 0 else 1."""
    if num < 0:
        return -1
    return 1

def sgn(num: float) -> float:
    """
    Return the sign of x.

    >>> sgn(0)
    0
    >>> sgn(1)
    1
    >>> sgn(-1)
    -1
    """
    if num > 0:
        return 1
    if num < 0:
        return -1
    return 0
