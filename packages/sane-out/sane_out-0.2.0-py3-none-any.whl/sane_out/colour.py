"""
This module defines function that turns ANSI codes into an escaped string
"""


def encode_ansi(*codes: int) -> str:
    """
    Encodes the ANSI code into an ANSI escape sequence.

    >>> encode_ansi(30)
    '\\x1b[30m'

    Support defining multiple codes:

    >>> encode_ansi(1, 33)
    '\\x1b[1;33m'

    All numbers are treated as positive; the sign doesn't matter:

    >>> encode_ansi(-31)
    '\\x1b[31m'

    :param codes: ANSI codes
    :return: ANSI escaped sequence
    """
    return f"\033[{';'.join([str(abs(code)) for code in codes])}m"
