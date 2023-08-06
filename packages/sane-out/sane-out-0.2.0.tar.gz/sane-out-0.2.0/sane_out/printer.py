"""
This module describes the SanePrinter class and its method

SanePrinter is the main class; it is responsible for the output of the library
"""

import sys
from typing import Optional, Iterable

from sane_out.colour import encode_ansi


class _SanePrinter:
    """
    The SanePrinter class, responsible for the whole console output.

    sane-out exports a "default" instance of SanePrinter; the class can be used to
    create different implementations. Although it is also acceptable to modify the
    module-provided version.
    """

    def __init__(self, verbose: bool = False, colour: bool = True) -> None:
        """
        Creates an instance of SanePrinter.

        :param verbose: whether the debug messages will be output
        :param colour: whether to colour the message
        """
        self.verbose = verbose
        self.colour = colour

    def _print(
        self,
        message: str = "",
        colour_code: Optional[Iterable[int]] = None,
        err: bool = False,
    ):
        """Prints a message to a specified stream / file.

        The method can become the sequence of ANSI codes to colour the message with.
        Since colour.py offers only foreground colors and the bright modofier, most uses
        will include the optional bright modifier sequence and one colour sequence.

        >>> _SanePrinter()._print("Hello World")
        Hello World

        >>> _SanePrinter()._print("Hello Cyan World", [36])
        \x1b[36mHello Cyan World\x1b[0m

        The message is printed to stdout by default; one can specify a different stream:

        >>> _SanePrinter()._print("Hello stderr", err=True)

        (doctest doesn't support stderr testing...)

        :param message: message to print
        :param colours: sequence of colours to style the message, or None to print
                        message without colours
        :param stream: stream to output the message to
        """
        if err:
            stream = sys.stderr
        else:
            stream = sys.stdout

        coloured = self.colour and colour_code is not None

        if message and coloured:
            message = f"{encode_ansi(*colour_code)}{message}{encode_ansi(0)}"

        message += "\n"

        if message:
            stream.write(message)
        stream.flush()

    def debug(self, message: str = ""):
        """
        Prints a debug message.

        The message is printed to the stdout in bright black (grey) colour. The message
        is printed only when verbose=True:

        >>> _SanePrinter().debug("Debug Message")

        >>> _SanePrinter(verbose=True).debug("Debug Message")
        \x1b[30;1mDebug Message\x1b[0m

        :param message: message to print
        """

        if self.verbose:
            self._print(message, [30, 1])

    def __call__(self, message: str = ""):
        """
        Prints a simple message.

        The message is printed to stdout without any ANSI tags.

        As you may notice, this is analogue to info(); this way, SanePrinter objects
        can be used as funcitions — a handy shortcut!

        >>> _SanePrinter()("Hello World")
        Hello World

        :param message: message to print
        """
        self.info(message)

    def info(self, message: str = ""):
        """
        Prints a simple message to the console.

        The message gets printed to stdout without any ANSI tags.

        >>> _SanePrinter().info("Hello World")
        Hello World

        :param message: message to print
        """
        self._print(message)

    def warning(self, message: str = ""):
        """
        Prints a warning message.

        The message is printed to the stderr in yellow colour.

        :param message: message to print
        """
        self._print(message, [33], err=True)

    def error(self, message: str = "", exit_code: int = -1):
        """
        Prints an error message and quits the program.

        The message is printed to the stderr in red colour.

        :param message: message to print
        :param exit_code: code to exit the program with
        """
        self.calm_error(message)
        sys.exit(exit_code)

    def calm_error(self, message: str = ""):
        """
        Prints an error message without quitting.

        The message is printed to the stderr in red colour.

        :param message: message to print
        """
        self._print(message, [31], err=True)
