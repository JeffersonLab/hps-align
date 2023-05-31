
from pathlib import Path
import xml.etree.ElementTree as ET
from ._write import write_mapping


def coordump(detpath: str, output_file: str):
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
