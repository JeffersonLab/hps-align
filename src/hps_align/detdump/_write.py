
from pathlib import Path
from enum import Enum
import json
import csv


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
        produce a row given a key, val pair from the mapping as arguments.
        The default is to just write the key and value as two columns
        :meth:`__get_row_default`
    """
    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        if header is not None:
            csvwriter.writerow(header)
        for name, val in data.items():
            csvwriter.writerow(getrow(name, val))
