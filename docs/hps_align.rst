HPS Align
=========

.. automodule:: hps_align.__main__

Sub-Modules
-----------

.. toctree::
   :maxdepth: 2

   hps_align.plot
   hps_align.detdump

CLI Development
---------------

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
that can be included as another wrapper :meth:`hps_align._cli.typer_unpacker`
defined below.

.. [typer] https://typer.tiangolo.com/

In typer a command line *application* can have commands, arguments,
options or other sub-applications. We use all of these tools to
construct our tree of possible actions. The detdump module is an
example of a sub-application with its own commands which have their
own arguments and options while the plot module is an example of
a command for our root application.

.. automodule:: hps_align._cli
   :members:
