"""plot detector dumps to compare sensor positions and orientations"""

from typing import List
from pathlib import Path
from enum import Enum

import typer

from ._angles import angle_calculator
from .._cli import app


class Coord(Enum):
    """which coordinate system to use"""
    GLOBAL = "global"
    """coordinates of sensors in some parent volume holding all of them"""
    LOCAL = "local"
    """coordinates relative to each sensor individually i.e. the alignment constants themselves"""


class Plot(Enum):
    """which type of comparison plot to use"""
    ABS = "abs"
    """plot all values in absolute terms"""
    DIFF = "diff"
    """subtract all values by the reference values"""


Angle = Enum('Angle', {name: name for name in angle_calculator.__registry__})
Angle.__doc__ = """what angle definition should be used in global coordinate plots

See _angles module for how these definitions are defined.
"""

for a in Angle:
    a.__doc__ = angle_calculator.__registry__[a.value].__doc__


class Position(Enum):
    """what position definition should be used in global coordinate plots"""
    HPS = "hps"
    """positions relative to entire HPS detector"""
    SVT = "svt"
    """positions relative to SVT box"""


@app.command()
def plot(
    input_file: List[Path],
    out: Path = typer.Option(None, help="output file name to print image to, default is <plot>.pdf"),
    coord: Coord = typer.Option(Coord.GLOBAL.value, help="which coordinate system to use"),
    angle: Angle = typer.Option(Angle.axis.value, help='which angle definition to use in global coordinates'),
    pos: Position = typer.Option(Position.HPS.value, help='which position definition to use in global coordinates'),
    plot: Plot = typer.Option(Plot.ABS.value, help='What type of plot to make')
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

    if coord == Coord.LOCAL:
        from ._load import _local as loader
        from ._load import _local_is2016 as is2016
        from ._load import _local_remap2016 as remap2016
        from ._table_fig import _local as plotter
        index = 'parameter'
        plot_kw = dict()
        load_kw = dict()
        if plot == Plot.ABS:
            plot_kw['title'] = 'Constant Values'
    else:
        from ._load import _global as loader
        from ._load import _global_is2016 as is2016
        from ._load import _global_remap2016 as remap2016
        from ._table_fig import _global as plotter
        index = 'sensor'
        angle_def = angle_calculator.__registry__[angle.value]
        plot_kw = dict(
            position=pos.value,
            angle_title=angle_def.__title__
        )
        load_kw = dict(
            angle_calculator=angle_def
        )
        if plot == Plot.ABS:
            plot_kw['title'] = 'Absolute Position and Orientation'

    data = [
        (inf.stem, loader(inf, **load_kw))
        for inf in input_file
    ]

    years = [is2016(df) for _name, df in data]
    if any(years) and not all(years):
        # at least one is 2016 but not all of them,
        # apply 2016 remap to the 2016 ones
        for yes2016, (_name, df) in zip(years, data):
            if yes2016:
                df[index] = df[index].apply(lambda i: remap2016[i])

    if plot == Plot.DIFF:
        if len(data) < 2:
            raise ValueError('Must provide 2 or more detectors to make a diff plot!')
        # set the index so subtraction lines up along ID
        for _name, df in data:
            df.set_index([index], inplace=True)
        # get reference detector
        ref_name, ref_table = data[0]
        ref_table['sortval'] = 0
        ref_table['lay'] = 0
        # subtract away the first detector provided
        data = [
            (name, (df-ref_table).reset_index().sort_values('sortval').dropna(subset=['ux']).reset_index(drop=True))
            for name, df in data[1:]
        ]
        # remove layers not in both years if comparing both detector versions
        if any(years) and not all(years):
            data = [((name, df[df.lay > 1.5]) if (df['lay'] == 1.0).any() else (name, df[df.lay > 2.5])) for name, df in data]
        # change plot title
        plot_kw['title'] = f'Difference Relative to {ref_name}'

    plotter(
        data,
        out,
        **plot_kw
    )
