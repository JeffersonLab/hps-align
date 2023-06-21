"""dump detector parameters for analysis"""

from . import _global
from . import _local
from ._cli import app

from . import plot

app.add_typer(
    plot.app,
    name="plot",
    help=plot.__doc__
    )
