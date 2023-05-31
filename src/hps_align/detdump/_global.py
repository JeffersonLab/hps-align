
from pathlib import Path
import subprocess
import os
from ._write import write_mapping


def coordump(detname: str, input_file: Path, jar: Path, output_file: Path):
    """dump coordinates of sensors in global frame

    This is done by running a specific driver in hps-java
    and then processing its output. Since we are running
    hps-java there are a few required inputs.

    ## User
    1. bin.jar file : the PrintGeometryDriver has been on
      hps-java master for awhile so this does not need to
      be incredibly recent.
    2. input slcio file : the driver does not look at any
      of the events in the slcio file so it just needs to
      be /any/ slcio file with at least one event in it.
    3. detname : name of detector

    ## Auto
    1. java args : we aren't doing any strong processing
      or using GBL so we just have a default set of java
      arguments
    2. steering file : we use the steering file that
      is stored in this module
    3. outputFile : nothing is written to it so we just
      supply a dummy name
    4. number of events : we just need one to trigger
      the functionality of loading the detector
    5. run number : the run number needs to be a valid
      run number so that hps-java can pull down condition
      databases, but it doesn't need to pertain to the
      detector being used
    """

    geo_print_result = subprocess.run(
        [
            'java',
            '-XX:+UseSerialGC',
            '-Xmx3000m',
            '-jar', str(jar),
            str(Path(__file__).parent / 'geoPrint.lcsim'),
            '-i', str(input_file),
            '-d', detname,
            '-R', '7800',
            '-n', '1'
        ],
        capture_output=True,
        check=True
    )

    sensor_map = {}

    for line in geo_print_result.stdout.splitlines():
        line = line.decode('utf-8')
        if 'sensor' in line and ':' in line:
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
                position=position,
                u=u, v=v, w=w
            )

    write_mapping(output_file, sensor_map,
                  header=['sensor',
                          'x', 'y', 'z',
                          'ux', 'uy', 'uz',
                          'vx', 'vy', 'vz',
                          'wx', 'wy', 'wz'],
                  getrow=lambda sensor, loc:
                  [sensor,
                   *loc['position'],
                   *loc['u'],
                   *loc['v'],
                   *loc['w']
                   ])
