
import typer

from pathlib import Path
import xml.etree.ElementTree as ET
from ._write import OutputType, write_mapping
from ._cli import app


@app.command(
    short_help="dump millepede alignment constants",
    help="""
The millepede alignment constants are modifications on
the local coordinate frame and so they are kind of the
"local" coordinates relative to the local frame.
"""
)
def local_coordump(
    detpath: Path = typer.Argument(..., help='path to detector to dump'),
    output_file: str = typer.Option(None, help='output file to write data to, uses detector name by default'),
    output_type: OutputType = typer.Option(
        'json',
        help='type of output to write will be over-written by extension of output_file if provided')
):
    """dump coordinates in local frame

    This effectively dumps the alignment parameters
    since the "local" frame handles the global detector
    setup and the survey constnats.

    Parameters
    ----------
    detpath: str
        path to detector from which to get coordinates
    output_file: str
        output file to write coordinates to
    """

    tree = ET.parse(Path(detpath) / 'compact.xml')

    # use 'eval' so that python calculates the full value
    # from the potentially-several values connected with +-
    param_map = {
        element.get('name'): eval(element.get('value'))
        for element in tree.iter('millepede_constant')
    }

    write_mapping(output_file, param_map,
                  header=['parameter', 'value'],
                  getrow=lambda k, v: [k, v])
