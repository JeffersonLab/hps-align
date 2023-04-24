"""Main entrypoint when running this package

    python3 -m hps_align <args>

Calls into this module.
"""

import os
from pathlib import Path
from typing import List

import typer

from ._cli import app
from ._cfg import cfg

from . import plot_res_and_kinks

@app.callback()
def main(
        config : str =  typer.Option(
            (Path(__file__).parent.resolve() / "data" / "plot_list.json"),
            help='JSON plot config file'
            )
        ):
    """
    run alignment sub commands
    """
    cfg.cfg(plot_list_file = config)


if __name__ == '__main__' :
    app()
