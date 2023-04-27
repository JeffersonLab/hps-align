"""Main entrypoint when running this package

    python3 -m hps_align <args>

Calls into this module.
"""

from . import plot
from ._cli import app
import os
import warnings
from pathlib import Path
from typing import List

import typer
from typing import List

import ROOT
ROOT.gROOT.SetBatch(1)


# from . import plot_res_and_kinks


if __name__ == '__main__':
    app()
