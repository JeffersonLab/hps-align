"""plot detector dumps to compare sensor positions and orientations"""

from typing import List
from pathlib import Path

import typer

from ._cli import app
from . import _load

def _table_fig(data_items, title, output_file, which='hps'):
    """construct a table of figures using matplotlib subplots"""

    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(
        nrows = 3,
        ncols = 2,
        sharex = 'col'
    )
    fig.set_size_inches(17,8)

    for i_c, c in enumerate(['x','y','z']):
        for i_tr, tr in enumerate([which,'theta']):
            # go through coordinates down columns and
            # and position/rotation across rows
            ax = axes[i_c][i_tr]
            for name, data in data_items:
                ax.scatter(
                    data.sensor,
                    data[f'{tr}{c}']*1000,
                    label = name if i_c==0 and i_tr == 0 else '_no_legend'
                )
            if i_tr == 0:
                ax.set_ylabel(f'{c.upper()} [$\mu$m]')
            else:
                ax.set_ylabel(f'$\\theta_{c}$ [mrad]')
            ax.axhline(0.0, color='gray')
            ax.grid(axis='x')
            if c == 'x':
                if i_tr == 0:
                    if tr == 'hps':
                        ax.set_title('HPS Global Position')
                    else:
                        ax.set_title('SVT Global Position')
                else:
                    ax.set_title('Euler Angle\n$\\theta_x = atan(v_z, w_z)$, $\\theta_y = -asin(u_z)$, $\\theta_z = atan(u_y, u_x)$')
            if c == 'z':
                ax.set_xticks(
                    ax.get_xticks(),
                    ax.get_xticklabels(),
                    rotation=90
                )
    fig.legend(
        title = title,
        loc = 'lower center',
        bbox_to_anchor = (0.5, 0.9)
    )
    fig.savefig(output_file, bbox_inches='tight')
    plt.close()

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
        raise ValueError('local plotting not implemented yet')

    data = [
        (inf.stem, _load.glbl(inf).set_index(["sensor"]))
        for inf in input_file
    ]

    ref_name, ref_table = data[0]

    # subtract away the first detector provided
    data = [
        (name, (df-ref_table).reset_index())
        for name, df in data[1:]
    ]

    _table_fig(
        data,
        f"Different Relative to {ref_name}",
        out,
        which=which
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
        raise ValueError('local plotting not implemented yet')

    data = [
        (inf.stem, _load.glbl(inf))
        for inf in input_file
    ]

    _table_fig(
        data,
        "Absolute Position and Orientation",
        out,
        which=which
    )
