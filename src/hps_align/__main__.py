"""Main entrypoint when running this package

Call into this module and run the app constructed by typer::

    python3 -m hps_align <args>

Besides running the app constructed by typer, we also make
sure to inform ROOT that this is a batch script. This 
prevents ROOT from opening any GUI windows while constructing
plots.
"""

from ._cli import app

import ROOT
ROOT.gROOT.SetBatch(1)

if __name__ == '__main__':
    app()
