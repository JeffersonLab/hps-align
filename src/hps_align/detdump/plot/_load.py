"""load detector parameters dumped to a file"""

from pathlib import Path

import numpy as np
import pandas as pd

from ._angles import axis


def _global(f: Path, angle_calculator=axis):
    r"""transform input global detdump into in-memory data table

    We also take this opportunity to reformat the sensor names into
    something more readable and sort the dataframe in a special way
    so that the order of the sensors in the plot is more natural.

    Parameters
    ----------
    f : Path
        file to load global sensor information from
    angle_calculator : Callable
        calculate the three angles representing the orientation of the sensor.
        This function is provided the parsed pandas DataFrame and then is
        expected to set the three columns [thetax, thetay, thetaz] to there
        calculated values.
        The default calculator is :meth:`axis`.

    Returns
    -------
    pd.DataFrame
        dataframe holding the global sensor information along with the calculated
        angles
    """
    df = pd.read_csv(f)

    df.drop(
        df[df.sensor.str.contains('ECalScoring')].index,
        inplace=True
    )

    # shorten sensor name
    df['sensor'] = df.sensor.apply(lambda s: s.replace('module0_', '').replace('_sensor0', '').replace('halfmodule_', '').replace('module_', ''))
    df['lay'] = df.sensor.apply(lambda s: int(s[1]))
    df['vol'] = df.sensor.apply(lambda s: 1.0 if s[2] == 'b' else 0.0)
    df['tilt'] = df.sensor.apply(lambda s: 1.0 if (s[2] == 'b' and s[4] == 'a') or (s[2] == 't' and s[4] == 's') else 0.0)
    df['side'] = df.sensor.apply(lambda s: 1.0 if s[-1] == 't' else 0.0)
    df['sortval'] = 500.0*df.vol + 2.0*df.tilt + 1.0*df.side + 4.0*df.lay
    df = df.sort_values('sortval')
    angle_calculator(df)
    return df


def _global_is2016(df: pd.DataFrame):
    """check if the input dataframe holdinging geometry information is from 2016 or not

    This check is currently only valid for global coordinates.

    For global coordinates, the distinguishing factor between 2016 and post-upgrade
    years is the presence of a 7th layer.

    Parameters
    ----------
    df: pd.DataFrame
        dataframe of sensor coordinates and positions


    Returns
    -------
    bool:
        True if dataframe represents a 2016 detector
    """

    return not any(df.sensor.str.contains('L7'))


_global_remap2016 = {
    'L1t_axial': 'L2t_axial',
    'L1t_stereo': 'L2t_stereo',
    'L2t_axial': 'L3t_axial',
    'L2t_stereo': 'L3t_stereo',
    'L3t_axial': 'L4t_axial',
    'L3t_stereo': 'L4t_stereo',
    'L4t_axial_hole': 'L5t_axial_hole',
    'L4t_stereo_hole': 'L5t_stereo_hole',
    'L4t_axial_slot': 'L5t_axial_slot',
    'L4t_stereo_slot': 'L5t_stereo_slot',
    'L5t_axial_hole': 'L6t_axial_hole',
    'L5t_stereo_hole': 'L6t_stereo_hole',
    'L5t_axial_slot': 'L6t_axial_slot',
    'L5t_stereo_slot': 'L6t_stereo_slot',
    'L6t_axial_hole': 'L7t_axial_hole',
    'L6t_stereo_hole': 'L7t_stereo_hole',
    'L6t_axial_slot': 'L7t_axial_slot',
    'L6t_stereo_slot': 'L7t_stereo_slot',
    'L1b_axial': 'L2b_axial',
    'L1b_stereo': 'L2b_stereo',
    'L2b_axial': 'L3b_axial',
    'L2b_stereo': 'L3b_stereo',
    'L3b_axial': 'L4b_axial',
    'L3b_stereo': 'L4b_stereo',
    'L4b_axial_hole': 'L5b_axial_hole',
    'L4b_stereo_hole': 'L5b_stereo_hole',
    'L4b_axial_slot': 'L5b_axial_slot',
    'L4b_stereo_slot': 'L5b_stereo_slot',
    'L5b_axial_hole': 'L6b_axial_hole',
    'L5b_stereo_hole': 'L6b_stereo_hole',
    'L5b_axial_slot': 'L6b_axial_slot',
    'L5b_stereo_slot': 'L6b_stereo_slot',
    'L6b_axial_hole': 'L7b_axial_hole',
    'L6b_stereo_hole': 'L7b_stereo_hole',
    'L6b_axial_slot': 'L7b_axial_slot',
    'L6b_stereo_slot': 'L7b_stereo_slot',
}


def _local(f: Path):
    """Load the alignment constants from the input path

    Also convert a alignment constant ID number into its t_r and u_v_w
    for later categorization into different plots. The conversion from
    ID number into differet categories is listed below.

    t_r
        acquired by getting the 2nd digit of the 5-digit ID number.

    u_v_w
        getting the 3rd digit of the 5-digit ID number

    individual
        True if the last two digits are greater than 0 and less than 23

    Parameters
    ----------
    f : Path
        file to load local alignment constants from

    Returns
    -------
    pd.DataFrame
        dataframe holding the constants and the deduced categorical variables
    """

    df = pd.read_csv(f)
    df['value'] = df.value.apply(pd.eval)
    df['t_r'] = (df.parameter % 10000) // 1000
    df['u_v_w'] = (df.parameter % 1000) // 100
    df['individual'] = (df.parameter % 100 < 23) & (df.parameter % 100 > 0)
    df.sort_values('parameter', inplace=True)
    return df


def _local_is2016(df: pd.DataFrame):
    """determine if a local-coordinate dataframe is 2016

    not implemented
    """
    return False


_local_remap2016 = dict()
