
from enum import Enum
from typing import List

import typer

from .._cli import app, typer_unpacker
from ._plotter import plotter

from . import vertex
from . import tracks
from . import residual

PlotOpt = Enum('PlotOpt', {name:name for name in plotter.__registry__})


@app.command()
@typer_unpacker
def plot(
        plots: List[PlotOpt]
):
    pass
