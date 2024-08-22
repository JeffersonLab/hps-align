"""create detector with small misalignments"""

import typer
from pathlib import Path
from ._cli import app
from .._cli import typer_unpacker

from . import _misalign

@app.command()
@typer_unpacker
def movement(
    year: int = typer.Argument(..., help='year of detector'),
    detector: str = typer.Argument(..., help='input detector .xml file'),
    method: str = typer.Argument('gauss', help='distribution to draw from (gauss, uniform)'),
    rw: float = typer.Option(None, help='characteristic displacement in Rw'),
    tu: float = typer.Option(None, help='characteristic displacement in Tu'),
    output: str = typer.Option(None, help='output detector .xml file')
):
    """Moving the sensors"""
    if rw is None and tu is None:
        raise ValueError('must provide at least one of rw or tu')
    
    misaligner = _misalign.Misalignment(detector, new_name=output)

    if rw is not None:
        rw = float(rw)
        misaligner.move_rw(method, rw)

    if tu is not None:
        tu = float(tu)
        misaligner.move_tu(method, tu)
    
