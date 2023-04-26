"""Main entrypoint when running this package

    python3 -m hps_align <args>

Calls into this module.
"""

import os
import warnings
from pathlib import Path
from typing import List

import typer
from typing import List

import ROOT
ROOT.gROOT.SetBatch(1)

from ._cli import app
from ._cfg import cfg

#from . import plot_res_and_kinks
from . import choose


def generate_legend_names(input_files):
    """! Generate legend names from input file names"""

    print("SETUP:: Generating legend names from input names.")
    legend_names = []
    for file in input_files:
        pos1 = file.find('HPS')
        pos2 = file.find('iter') + 5

        if pos1 == -1 or pos2 == -1:
            raise Exception(
                "Detector naming pattern deviates from default; the legend names have to be entered manually")

        legName = file[pos1:pos2]
        legend_names.append(legName)
    return legend_names


@app.callback()
def main(
        plot_list: str = typer.Option(
            (Path(__file__).parent.resolve() / "data" / "plot_list.json"),
            help='JSON plot config file'
        ),
        input_files: List[str] = typer.Option([],
                                              help='Input files for plotting'),
        legend: List[str] = typer.Option([],
                                         help='Labels for legend if not deduced from input file names'),
        out_dir: str = typer.Option(os.getcwd(),
                                    help='output directory to put plots'),
        html: bool = typer.Option(True,
                                  help='write an HTML file for viewing plots'),
        is2016 : bool = typer.Option(False,
                                     help='if we are looking at 2016 plots or not'),
        ext: str = typer.Option('png',
                                help='plot file extension (png or pdf)'),
        config: str = typer.Option(None,
                                   help='JSON config for plotting inputs rather than command line.')
):
    """
    run alignment sub commands
    """

    if config is not None:
        # read the JSON config instead of command line parameters

        with open(config) as json_file:
            c = json.load(json_file)

            if c['inputFiles']:
                input_files = c['inputFiles']

            if c['outdir']:
                out_dir = c['outdir']

            if c['do_HTML']:
                html = c['do_HTML']

            if c['oFext']:
                ext = c['oFext']

            if c['legend']:
                legend = c['legend']

    if len(input_files) == 0:
        #raise ValueError('No input files given.')
        warnings.warn('No input files given.')

    if legend is None or len(legend) == 0:
        legend = generate_legend_names(input_files)
    elif len(input_files) != len(legend):
        #raise ValueError("Number of legend labels does not equal number of input files.")
        warnings.warn('Number of legend labels does not equal number of input files.')

    cfg.cfg(
        plot_list_file=plot_list,
        input_files=input_files,
        legend_labels=legend,
        out_dir=out_dir,
        html=html,
        ext=ext,
        is2016 = is2016,
    )


if __name__ == '__main__':
    app()
