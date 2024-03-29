
import typer

from pathlib import Path
import subprocess
import os
from ._write import write_mapping
from ._cli import app


@app.command(
    short_help="dump coordinates and orientations of sensors in the global frame",
    help="""
This is done by running a specific driver in hps-java and then processing its output.
Since we are running hps-java there are unfortunately many required inputs.

Run numbers: 2015 use 5772, 2016 use 7800, 2019 use 10716, and 2021 use 14166.
"""
)
def global_coord(
    detname: str = typer.Argument(..., help='name of detector to dump'),
    input_file: Path = typer.Argument(
        ..., help='input slcio file to "run over", data within this file is never used just needs '
        'to have at least one event in it so hps-java can get to the detector loading stage of processing.'),
    run_number: int = typer.Argument(
        ...,
        help='run number roughly corresponding to year of detector, again only necessary so '
        'hps-java can get to loading the detector'),
    jar: Path = typer.Option(
        (Path.home() / '.m2' / 'repository' / 'org' / 'hps' /
         'hps-distribution' / '5.2-SNAPSHOT' / 'hps-distribution-5.2-SNAPSHOT-bin.jar'),
        help='java bin jar to use to run geometry printer'
    ),
    output_file: str = typer.Option(None, help='output file to write data to, uses detector name by default')
):
    """dump coordinates of sensors in global frame

    This is done by running a specific driver in hps-java
    and then processing its output. Since we are running
    hps-java there are a few required inputs.

    Run Number Look-Up-Table
    ------------------------

    Each year has a different set of "base" conditions that need to be
    used; otherwise, the hps-java run isn't able to get to the geometry
    construction.

    * 2015: 5772
    * 2016: 7800 (7000-8999)
    * 2019: 10716
    * 2021: 14166

    Since the 2019 and 2021 conditions have the same "shape", we can use
    the same (somewhat arbitrary) run number if desired.

    Auto-Deduced java Arguments
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^

    java args
        we aren't doing any strong processing or using GBL
        so we just have a default set of java arguments

    steering file
        we use the steering file that is stored in this module

    outputFile
        nothing is written to it so we just supply a dummy name

    number of events
        we just need one to trigger the functionality of loading the detector

    Parameters
    ----------

    detname : str
        The name of the detector to load
    input_file : Path
        the driver does not look at any
        of the events in the slcio file so it just needs to
        be /any/ slcio file with at least one event in it.
    run_number : int
        The run number needs to be a valid run number for that year
        so that hps-java can pull down condition
        databases, but it doesn't need to pertain to the
        detector being used
    jar : Path, optional
        the PrintGeometryDriver has been on
        hps-java master for awhile so this does not need to
        be incredibly recent. The default is the path to the 5.2-SNAPSHOT
        located in the user's home maven repository.

    """

    if output_file is None:
        # deduce default to be name of detector + extension
        output_file = f'{detname}-global.csv'

    if Path(output_file).suffix == '':
        # no extension provided, add it manually
        output_file += '.csv'

    geo_print_result = subprocess.run(
        [
            'java',
            '-XX:+UseSerialGC',
            '-Xmx3000m',
            '-jar', str(jar),
            str(Path(__file__).parent / 'geoPrint.lcsim'),
            '-i', str(input_file),
            '-d', detname,
            '-R', str(run_number),
            '-n', '1'
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True
    )

    sensor_map = {}
    svtFrameCount = False
    svtFrameLine = 0

    for line in geo_print_result.stdout.splitlines():
        line = line.decode('utf-8')
        if 'sensor' in line and ':' in line:
            svtFrameCount = True
            # line printing sensor name and coordinate position
            #   <name>: [ X, Y, Z] [ ux, uy, uz] [ vx, vy, vz] [ wx, wy, wz]
            line_elements = line.strip().split()
            # drop colon at end of name
            name = line_elements[0][:-1]
            # drop either comma or closing square bracket
            position = [float(line_elements[i][:-1]) for i in range(2, 5)]
            u = [float(line_elements[i][:-1]) for i in range(6, 9)]
            v = [float(line_elements[i][:-1]) for i in range(10, 13)]
            w = [float(line_elements[i][:-1]) for i in range(14, 17)]
            sensor_map[name] = dict(
                hps_position=position,
                u=u, v=v, w=w
            )
        if svtFrameCount:
            svtFrameLine += 1
        if svtFrameLine == 14:
            svtFrameLine = 0
            svtFrameCount = False
            line_elements = line.strip().split()
            position = [float(line_elements[i][:-1]) for i in range(1, 4)]
            sensor_map[name]['svt_position'] = position

    write_mapping(output_file, sensor_map,
                  header=['sensor',
                          'hpsx', 'hpsy', 'hpsz',
                          'svtx', 'svty', 'svtz',
                          'ux', 'uy', 'uz',
                          'vx', 'vy', 'vz',
                          'wx', 'wy', 'wz'],
                  getrow=lambda sensor, loc:
                  [sensor,
                   *loc['hps_position'],
                   *loc['svt_position'],
                   *loc['u'],
                   *loc['v'],
                   *loc['w']
                   ])
