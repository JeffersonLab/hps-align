"""load detector parameters dumped to a file"""

from pathlib import Path

import numpy as np
import pandas as pd

from .._write import OutputType

def _read_multitype(f: Path):
    """Load the input file from any of the supported detdump output types

    Parameters
    ----------
    f : str | Path
      file path to file with detector dump

    Returns
    -------
    pd.DataFrame
        dataframe loaded from that file
    """

    if not isinstance(f, Path):
        f = Path(f)

    if not f.is_file():
        raise ValueError(f'File {f} does not exist.')

    if not OutputType.valid(f):
        raise ValueError(f'File {f} does not have a supported extension.')

    if f.suffix == '.csv':
        return pd.read_csv(f)
    elif f.suffix == '.json':
        return pd.read_json(f).transpose()
    else:
        return NotImplemented


def glbl(f: Path):
    r"""transform input global detdump into in-memory data table

    We calculate the Euler angles here which are just one definition.

    .. math::

        \tan\theta_x = \frac{v_z}{w_z}
        \sin\theta_y = -u_z
        \tan\theta_z = \frac{u_y}{u_x}

    """
    df = _read_multitype(f)
    meas_cols = ['hps_position','svt_position','u','v','w']
    for meas in meas_cols:
        df[[f'{meas}x',f'{meas}y',f'{meas}z']] = df[meas].tolist()
    df.rename(
        columns = lambda colname : colname[:3]+colname[-1] if 'position' in colname and colname != 'position' else colname,
        inplace=True
    )
    df.drop(columns = meas_cols, inplace=True)

    df['thetax'] = np.arctan2(df.vz, df.wz)
    df['thetay'] = -np.arcsin(df.uz)
    df['thetaz'] = np.arctan2(df.uy, df.ux)

    df.reset_index(names='sensor', inplace=True)
    df.drop(
        df[df.sensor.str.contains('ECalScoring')].index,
        inplace=True
    )

    # shorten sensor name
    df['sensor'] = df.sensor.apply(lambda s: s.replace('module0_','').replace('_sensor0','').replace('halfmodule_','').replace('module_',''))
    return df


def lcl(f: Path):
    """Load the alignment constants from the input path

    Also convert a alignment constant ID number into its t_r and u_v_w
    for later plot categorization.
    """

    df = _read_multitype(f)
    df['value'] = df.value.apply(pd.eval)
    df['t_r'] = (df.parameter % 10000) // 1000
    df['u_v_w'] = (df.parameter % 1000) // 100
    df.sort_values('parameter', inplace=True)
    return df