#pylint: disable=wildcard-import
#pylint: disable=unused-wildcard-import
#pylint: disable=redefined-builtin
#pylint: disable=unused-argument
#pylint: disable=eval-used
"""
/src/seval.py

contains seval()
"""

import math

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

def seval(string:str, **kwargs) -> float:
    """
    given a function string, return the value
    """

    # extend kwargs with math functions
    kwargs.update(math.__dict__)

    # extend kwargs with sgn and sgn0 functions
    kwargs.update(sgn=sgn, sgn0=sgn0)

    return eval(string, kwargs)
