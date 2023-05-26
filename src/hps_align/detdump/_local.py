
import xml.etree.ElementTree as ET
import csv


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

    with open(output_file, 'w', newline='') as csvfile:
        csvwrite = csv.writer(csvfile)
        csvwriter.writerow(['parameter', 'value'])
        for element in tree.iter('millepede_constant'):
            # use 'eval' so that python calculates the full value
            # from the potentially-several values connected with +-
            csvwriter.writerow([element.name, eval(element.value)])
