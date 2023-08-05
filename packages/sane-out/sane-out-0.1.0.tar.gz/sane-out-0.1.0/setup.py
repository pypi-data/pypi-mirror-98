# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sane_out']

package_data = \
{'': ['*']}

extras_require = \
{':sys_platform == "win32"': ['colorama>=0.4.4,<0.5.0']}

setup_kwargs = {
    'name': 'sane-out',
    'version': '0.1.0',
    'description': 'A lightweight library for clean console output',
    'long_description': '# sane-out for Python\n\n> A lightweight library for clean console output\n\n## Install\n\nWith pip:\n\n```sh\npip install sane-out\n```\n\nWith Poetry:\n\n```sh\npoetry add sane-out\n```\n\nWith pipenv:\n\n```sh\npipenv install sane-out\n```\n\n## Use\n\n### Default behaviour\n\n```py\nfrom sane_out import out\n\nout("This is an info message")\nout.info("This is an info message too")\n\nout.debug("This is a debug message. It won\'t be printed without \'verbose=True\'")\nout.verbose = True\nout.debug("Now this debug message will be printed")\n\nout.warning("Warning! This is a message that will be printed to stderr")\n\nout.error("Your code will print an error message crash with code -1!")\nout.error("You can crash your program with a custom code", 42)\n\nout.calm_error("You can also print an error message without crashing")\n```\n\n### Custom instance\n\n```py\nfrom sane_out import _SanePrinter\n\n# Setup your output with constructor params\n\ntalkative = _SanePrinter(verbose=True, colour=True)\nboring = _SanePrinter(verbose=False, colour=False)\n\ntalkative.debug("Shhh... This is a debug message")\nboring.debug("I will not print this")\nboring.warning("And this won\'t have amy colour")\n```\n\n\n## License\n\nMIT © Nikita Karamov\n',
    'author': 'Nikita Karamov',
    'author_email': 'nick@karamoff.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sane-out/python',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
