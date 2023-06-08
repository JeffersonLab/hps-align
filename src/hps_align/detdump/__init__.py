"""dump detector parameters for analysis"""

from typing_extensions import Annotated
from pathlib import Path
from enum import Enum
import os

import typer

from .._cli import app, typer_unpacker

from . import _global
from . import _local
from . import _write


class System(Enum):
    """choose which coordinate system to dump"""
    GLOBAL = "global"
    LOCAL = "local"


@app.command()
@typer_unpacker
def detdump(
        system: System = typer.Argument(
            ...,
            help="coordinate system to dump - local is relative to sensor frame, i.e. dump the millepede constants"
            " and global is relative to the entire HPS detector frame"),
        det: str = typer.Argument(
            ...,
            help='detector to dump (directory path for local system, name for global system)'),
        output_file: str = typer.Option(None, help='output file to write data to, uses detector name by default'),
        output_type: _write.OutputType = typer.Option(
            'json',
            help='type of output to write will be over-written by extension of output_file if provided'),
        input_file: str = typer.Option(None, help='input slcio file (only required for global)'),
        run_number: int = typer.Option(None, help='run number pertaining to year (only required for global)'),
        jar: str = typer.Option(
            str(Path.home() /
                '.m2' / 'repository' / 'org' / 'hps' /
                'hps-distribution' / '5.2-SNAPSHOT' / 'hps-distribution-5.2-SNAPSHOT-bin.jar'),
            help='java bin jar to use to run geometry printer (only used for global system)'
        )
):
    """dump detector parameters for later analysis

    Currently, there are two types of "systems" that we can dump.
    "global" refers to the position and orientation of the sensors
    in the global HPS detector frame. "local" refers to the position and
    oritentation of the sensors relative to their own local frame i.e.
    "local" is a dump of the millepede alignment parameters while "global"
    is a dump of the final position and orientation.
    """

    if output_file is None:
        # deduce default to be name of detector + extension
        #  may need to strip trailing '/' to help basename work
        output_file = f'{os.path.basename(det.strip("/"))}-{system.value}.{output_type.value}'
    else:
        # output file provided, make sure extension is appropriate
        filename, ext = os.path.splitext(output_file)
        if ext == '':
            ext = output_type.value
        else:
            allowed_extensions = ['.'+e.value for e in OutputType.__members__.values()]
            if ext not in allowed_extensions:
                raise ValueError(f'{ext} not one of the allowed extensions {allowed_extensions}')
        output_file = filename+ext

    if system == System.LOCAL:
        if os.path.isdir(det):
            _local.coordump(det, output_file)
        else:
            raise ValueError('Local system deduction needs path to detector directory.')
    elif system == System.GLOBAL:
        if os.path.isdir(det):
            # need to have the detector name not the full path
            det = os.path.basename(det.strip('/'))
        if input_file is None:
            raise ValueError('Input file required for global system deduction')
        _global.coordump(det, input_file, jar, run_number, output_file)
