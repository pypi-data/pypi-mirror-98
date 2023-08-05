"""
This module defines ANSI colour sequences for the 8 foreground colours
"""

from enum import Enum


def encode_ansi(code: int) -> str:
    """
    Encodes the ANSI code into an ANSI excape sequence.


    >>> encode_ansi(1)
    '\\x1b[1m'

    All numbers are treated as positive; the sign doesn't matter:

    >>> encode_ansi(-31)
    '\\x1b[31m'

    :param code: ANSI code
    :return: ANSI escaped sequence
    """
    return f"\033[{str(abs(code))}m"


class FgAnsiColour(Enum):
    """
    Definitions for ANSI-encoded foreground colours as well as the bright modifier

    Colors included:
      - black
      - red
      - green
      - yellow
      - blue
      - magenta
      - cyan
      - white
    """
    BRIGHT = encode_ansi(1)

    BLACK = encode_ansi(30)
    RED = encode_ansi(31)
    GREEN = encode_ansi(32)
    YELLOW = encode_ansi(33)
    BLUE = encode_ansi(34)
    MAGENTA = encode_ansi(35)
    CYAN = encode_ansi(36)
    WHITE = encode_ansi(37)

    RESET = encode_ansi(39)
