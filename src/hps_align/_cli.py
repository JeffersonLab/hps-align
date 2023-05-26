"""Module to hold CLI object

In hps_align, we use [typer]_ to generate our command line parser.
This module is helpful because it parses the function signature of
our functions in order to identify what the command line parameters
should be. This allows us to forget about copying any new parameters
to functions into an argparse definition since it will be handled
by typer automatically.

One potentially issue with typer is that it requires its objects
to be used as default values for function arguments. This is not
an issue during normal operation; however, it prevents the function
from being called like a normal function. This motivates a fix
that can be included as another wrapper `hps_align._cli.typer_unpacker`
defined below.

.. [typer] https://typer.tiangolo.com/

Attributes
----------
app : typer.Typer
    our typer app which must be informed of any command's existence

Examples
--------
In order to register a function as a command with our CLI application::

    @app.command()
    def mycmd(...):
        # your code

In order to register a function and make it callable within other functions::

    @app.comand()
    @typer_unpacker
    def mycmd(...):
        # your code

Using typer's objects within your function arguments will help document the
command options and define their types. Look at typer's reference documentation
in order to get the syntax for that.
"""

import functools
import inspect
from typing import Callable

import typer
from typer.models import ParameterInfo

app = typer.Typer()


def typer_unpacker(f: Callable):
    """Decorator which accesses typer defaults and updates the kwargs
    so that the function can be used in typer CLI and normally

    This was developed by GitHub user shaneatendpoint `in response
    to question on GitHub <https://github.com/tiangolo/typer/issues/279#issuecomment-893667754>`_.
    It will not be able to be included within typer unless Python's
    typing system becomes more advanced.
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        # Get the default function argument that aren't passed in kwargs via the
        # inspect module: https://stackoverflow.com/a/12627202
        missing_default_values = {
            k: v.default
            for k, v in inspect.signature(f).parameters.items()
            if v.default is not inspect.Parameter.empty and k not in kwargs
        }

        for name, func_default in missing_default_values.items():
            # If the default value is a typer.Option or typer.Argument, we have to
            # pull either the .default attribute and pass it in the function
            # invocation, or call it first.
            if isinstance(func_default, ParameterInfo):
                if callable(func_default.default):
                    kwargs[name] = func_default.default()
                else:
                    kwargs[name] = func_default.default

        # Call the wrapped function with the defaults injected if not specified.
        return f(*args, **kwargs)

    return wrapper
