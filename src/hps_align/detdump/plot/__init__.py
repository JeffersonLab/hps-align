"""plot detector dumps to compare sensor positions and orientations"""

from typing import List
from pathlib import Path
from enum import Enum

import typer

from .._cli import app


class WhichCoord(Enum):
    """which coordinate system to use"""
    HPS = "hps"
    """coordinates relative to entire HPS detector"""
    SVT = "svt"
    """coordinates relative to SVT frame"""
    LOCAL = "local"
    """coordinates relative to each sensor individually i.e. the alignment constants themselves"""


class WhichPlot(Enum):
    """which type of comparison plot to use"""
    ABS = "abs"
    """plot all values in absolute terms"""
    DIFF = "diff"
    """subtract all values by the reference values"""


@app.command()
def plot(
    input_file: List[Path],
    out: Path = typer.Option(None, help="output file name to print image to, default is <plot>.pdf"),
    which: WhichCoord = typer.Option(WhichCoord.HPS.value, help="Which coordinate system to use"),
    plot: WhichPlot = typer.Option(WhichPlot.ABS.value, help='What type of plot to make')
):
    """Plot detector coordinate and orientation data

    If the 'diff' <plot> is chosen, then all values are subtracted by their
    reference values which are defined by the first detector provided in the
    input list.

    All detectors are named after the name of the file. Use soft links to
    rename files to helpful legend names if you wish.
    """

    if out is None:
        out = plot.value + '.pdf'

    if which == WhichCoord.LOCAL:
        from ._load import _local as loader
        from ._table_fig import _local as plotter
        index = 'parameter'
        plot_kw = dict()
        if plot == WhichPlot.ABS:
            plot_kw['title'] = 'Constant Values'
    else:
        from ._load import _global as loader
        from ._table_fig import _global as plotter
        index = 'sensor'
        plot_kw = dict(which=which.value)
        if plot == WhichPlot.ABS:
            plot_kw['title'] = 'Absolute Position and Orientation'

    data = [
        (inf.stem, loader(inf))
        for inf in input_file
    ]

    if plot == WhichPlot.DIFF:
        if len(data) < 2:
            raise ValueError('Must provide 2 or more detectors to make a diff plot!')
        # set the index so subtraction lines up along ID
        for _name, df in data:
            df.set_index([index], inplace=True)
        # get reference detector
        ref_name, ref_table = data[0]
        # subtract away the first detector provided
        data = [
            (name, (df-ref_table).reset_index())
            for name, df in data[1:]
        ]
        # change plot title
        plot_kw['title'] = f'Difference Relative to {ref_name}'

    plotter(
        data,
        out,
        **plot_kw
    )
