"""load detector parameters dumped to a file"""

from pathlib import Path

import numpy as np
import pandas as pd


def _global(f: Path):
    r"""transform input global detdump into in-memory data table

    We calculate the Euler angles here which are just one definition.

    .. math::

        \tan\theta_x = \frac{v_z}{w_z}
        \sin\theta_y = -u_z
        \tan\theta_z = \frac{u_y}{u_x}

    """
    df = pd.read_csv(f)

    df['thetax'] = np.arctan2(df.vz, df.wz)
    df['thetay'] = -np.arcsin(df.uz)
    df['thetaz'] = np.arctan2(df.uy, df.ux)

    df.drop(
        df[df.sensor.str.contains('ECalScoring')].index,
        inplace=True
    )

    # shorten sensor name
    df['sensor'] = df.sensor.apply(lambda s: s.replace('module0_','').replace('_sensor0','').replace('halfmodule_','').replace('module_',''))
    df['lay'] = df.sensor.apply(lambda s: int(s[1]))
    df['vol'] = df.sensor.apply(lambda s: 1.0 if s[2] == 'b' else 0.0)
    df['tilt'] = df.sensor.apply(lambda s: 1.0 if (s[2] == 'b' and s[4] == 'a') or (s[2] == 't' and s[4] == 's') else 0.0)
    df['side'] = df.sensor.apply(lambda s: 1.0 if int(s[1]) > 4 and s[-1] == 't' else 0.0)
    df['sortval'] = 500.0*df.vol + 2.0*df.tilt + 1.0*df.side + 4.0*df.lay
    df = df.sort_values('sortval')
    return df


def _local(f: Path):
    """Load the alignment constants from the input path

    Also convert a alignment constant ID number into its t_r and u_v_w
    for later plot categorization.
    """

    df = pd.read_csv(f)
    df['value'] = df.value.apply(pd.eval)
    df['t_r'] = (df.parameter % 10000) // 1000
    df['u_v_w'] = (df.parameter % 1000) // 100
    df['individual'] = (df.parameter % 100 < 23) & (df.parameter % 100 > 0)
    df.sort_values('parameter', inplace=True)
    return df
