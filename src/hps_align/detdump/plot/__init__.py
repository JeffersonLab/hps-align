"""plot detector dumps to compare sensor positions and orientations"""

from typing import List
from pathlib import Path

import typer

from ._cli import app


@app.command()
def diff(
    input_file: List[Path],
    local: bool = typer.Option(False, help="Comparing alignment parameters and not global positions/orientations"),
    out: Path = typer.Option("diff.pdf", help="output file name to print image to"),
    which: str = typer.Option("hps", help="Which global coordinate system to use ('hps' or 'svt')")
):
    """Plot difference between detectors and a reference detector.

    The reference detector is the first detector provided in the input list.
    All detectors are named after the name of the file. Use soft links to
    rename files to helpful legend names if you wish.
    """

    if local:
        from ._load import _local as loader
        from ._table_fig import _local as plotter
        index = 'parameter'
        plot_kw = dict()
    else:
        from ._load import _global as loader
        from ._table_fig import _global as plotter
        index = 'sensor'
        plot_kw = dict(which=which)

    data = [
        (inf.stem, loader(inf).set_index([index]))
        for inf in input_file
    ]

    ref_name, ref_table = data[0]

    # subtract away the first detector provided
    data = [
        (name, (df-ref_table).reset_index())
        for name, df in data[1:]
    ]

    plotter(
        data,
        out,
        title=f'Difference Relative to {ref_name}',
        **plot_kw
    )


@app.command()
def abs(
    input_file: List[Path],
    local: bool = typer.Option(False, help="Comparing alignment parameters and not global positions/orientations"),
    out: Path = typer.Option("abs.pdf", help="output file name to print image to"),
    which: str = typer.Option("hps", help="Which global coordinate system to use ('hps' or 'svt')")
):
    """Plot the absolute position, overlaying all provided detectors

    All detectors are named after the name of the provided file. Use soft links `ln -s` to
    rename files to helpful legend names if you wish.
    """

    if local:
        from ._load import _local as loader
        from ._table_fig import _local as plotter
        plot_kw = dict(
            title='Constant Values'
        )
    else:
        from ._load import _global as loader
        from ._table_fig import _global as plotter
        plot_kw = dict(
            which=which,
            title='Absolute Position and Orientation'
        )

    data = [
        (inf.stem, loader(inf))
        for inf in input_file
    ]

    plotter(
        data,
        out,
        **plot_kw
    )
