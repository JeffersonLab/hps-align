"""Get survey data from OGP measurement files"""

import typer
from pathlib import Path
import json

from ._cli import app
from .._cli import typer_unpacker

from . import _survey


@app.command()
@typer_unpacker
def data(
    year: int = typer.Argument(..., help='year of detector'),
    input_file: Path = typer.Argument(..., help='file containing paths to survey data files'),
    output_file: str = typer.Option(None, help='output file to write data to')
):
    """some more explanation"""
    with open(input_file) as json_file:
        survey_files = json.load(json_file)

    if output_file is None:
        output_file = f'{year}_survey_results.xml'

    if year == 2019:
        survey = _survey.Survey2019(survey_files)
    else:
        raise ValueError(f'year {year} not supported')

    survey.print_results(output_file)
