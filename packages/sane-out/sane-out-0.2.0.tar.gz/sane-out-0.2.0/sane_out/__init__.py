__version__ = "0.2.0"

import sys

from sane_out.printer import _SanePrinter

if sys.platform == "win32":
    import colorama

    colorama.init()

out = _SanePrinter()
