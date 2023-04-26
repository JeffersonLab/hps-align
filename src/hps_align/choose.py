
from typing import List

import typer

from ._cli import app, typer_unpacker

from .plot._plotter import plotter
from . import plot

from enum import Enum

PlotOpt = Enum('PlotOpt', {name: name for name in plotter.__registry__})


@app.command()
@typer_unpacker
def choose(
        plots: List[PlotOpt]
):
    pass
