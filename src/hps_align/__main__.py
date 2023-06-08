"""Main entrypoint when running this package

Call into this module and run the app constructed by typer::

    python3 -m hps_align <args>

Besides running the app constructed by typer, we also make
sure to inform ROOT that this is a batch script. This
prevents ROOT from opening any GUI windows while constructing
plots.
"""

import ROOT
import importlib

from . import plot

from ._cli import app

for module_name in ['detdump']:
    module = importlib.import_module('.'+module_name, 'hps_align')
    app.add_typer(
        module.app,
        name=module_name,
        help=module.__doc__
    )

ROOT.gROOT.SetBatch(1)

if __name__ == '__main__':
    app()
