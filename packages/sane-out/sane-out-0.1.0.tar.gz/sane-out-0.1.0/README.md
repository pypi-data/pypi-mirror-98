# sane-out for Python

> A lightweight library for clean console output

## Install

With pip:

```sh
pip install sane-out
```

With Poetry:

```sh
poetry add sane-out
```

With pipenv:

```sh
pipenv install sane-out
```

## Use

### Default behaviour

```py
from sane_out import out

out("This is an info message")
out.info("This is an info message too")

out.debug("This is a debug message. It won't be printed without 'verbose=True'")
out.verbose = True
out.debug("Now this debug message will be printed")

out.warning("Warning! This is a message that will be printed to stderr")

out.error("Your code will print an error message crash with code -1!")
out.error("You can crash your program with a custom code", 42)

out.calm_error("You can also print an error message without crashing")
```

### Custom instance

```py
from sane_out import _SanePrinter

# Setup your output with constructor params

talkative = _SanePrinter(verbose=True, colour=True)
boring = _SanePrinter(verbose=False, colour=False)

talkative.debug("Shhh... This is a debug message")
boring.debug("I will not print this")
boring.warning("And this won't have amy colour")
```


## License

MIT © Nikita Karamov
