"""
util module
"""
import random
import string


def rstri(length) -> str:
    """
    get random digits string of length
    """
    return ''.join(random.choice(string.digits) for x in range(length))
