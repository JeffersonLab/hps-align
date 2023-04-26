
import typer

from ._cli import app, typer_unpacker

from .plot._plotter import plotter
from . import plot

from enum import Enum

class PlotOpt(str,Enum) :
    pass

for name in plotter.__registry__ :
    PlotOpt.__dict__[name] = name

@app.command()
@typer_unpacker
def choose(
        plots: List[PlotOpt]
        ) :
    pass
