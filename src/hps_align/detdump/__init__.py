"""dump detector parameters for analysis"""

from typing_extensions import Annotated
from pathlib import Path
from enum import Enum

import typer

from .._cli import app, typer_unpacker

from . import _global
from . import _local


class System(Enum):
    GLOBAL = "global"
    LOCAL = "local"


@app.command()
@typer_unpacker
def detdump(
        system: System,
        det: str,
        output_file: str = typer.Option(None, help='output file to write data to'),
        input_file: str = typer.Option(None, help='input slcio file (only required for global)'),
        jar: str = typer.Option(
            str(Path.home() /
                '.m2' / 'repository' / 'org' / 'hps' /
                'hps-distribution' / '5.2-SNAPSHOT' / 'hps-distribution-5.2-SNAPSHOT-bin.jar'),
            help='java bin jar to use to run geometry printer (only used for global system)'
        )
):
    """dump detector parameters for later analysis"""

    if output_file is None:
        # deduce default to be name of detector + csv
        #  may need to strip trailing '/' to help basename work
        output_file = os.path.basename(det.strip('/'))+'.csv'

    if system == System.LOCAL:
        if os.path.isdir(detname):
            _local.coordump(detname, output_file)
        else:
            raise ValueError('Local system deduction needs path to detector directory.')
    elif system == System.GLOBAL:
        if input_file is None:
            raise ValueError('Input file required for global system deduction')
        _global.coordump(detname, input_file, jar, output_file)
