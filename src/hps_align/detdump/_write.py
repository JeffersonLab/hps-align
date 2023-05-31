
from enum import Enum
import json
import csv


class OutputType(Enum):
    CSV = "csv"
    JSON = "json"


def __get_row_default(k, v):
    """default implementation of getrow"""
    return [str(k), str(v)]


def write_mapping(output_file, data, *, header=None, getrow=__get_row_default):
    """write a mapping to an output file as either a CSV or a JSON file

    Parameters
    ----------
    output_file: str
        path to output file to write
        must have a 'csv' or 'json' extension
    data: Mapping
        object to write
    header: List[str]
        list of header rows to write to csv
        no header written if not provided
    getrow: callable
        produce a row given a key, val pair from the mapping as arguments
        default is to just write the key and value as two columns
    """
    if output_file.endswith('csv'):
        if getrow is None:
            raise ValueError('getrow necessary if attempting to write to CSV')
        with open(output_file, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            if header is not None:
                csvwriter.writerow(header)
            for name, val in data.items():
                csvwriter.writerow(getrow(name, val))
    elif output_file.endswith('json'):
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    else:
        raise ValueError(f'Unable to deduce output type from extension of {output_file}')
