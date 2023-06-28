"""module for calculating different angles from coordinate axes"""

import functools

import numpy as np
import pandas as pd


def angle_calculator(f):
    """decorator for registering angle calculators"""
    angle_calculator.__registry__[f.__name__] = f
    # set default title
    f.__title__ = f.__name__

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapper


angle_calculator.__registry__ = dict()
"""registry of angle calculators"""


@angle_calculator
def euler(df: pd.DataFrame):
    r"""One definition of the Euler angles

    This code is not currently being used by the global loader
    but it is here for easy drop-in if users wish. Just change
    which angle_calculator is used when the global loader
    is being called.

    .. math::

        \theta_x = \arctan\left(\frac{v_z}{w_z}\right)

    .. math::

        \theta_y = -\arcsin(u_z)

    .. math::

        \theta_z = \arctan\left(\frac{u_y}{u_x}\right)

    Parameters
    ----------
    df : pd.DataFrame
        dataframe with u, v, w coordinate vectors

    Returns
    -------
    Tuple[pd.Series]
        the three-tuple of the three euler angles
    """
    df['thetax'] = np.arctan2(df.vz, df.wz)
    df['thetay'] = -np.arcsin(df.uz)
    df['thetaz'] = np.arctan2(df.uy, df.ux)


euler.__title__ = r"""Euler Angles
$\theta_x = atan(v_z/w_z)$ $\theta_y = -asin(u_z)$ $\theta_z = atan(u_y/u_x)$"""


@angle_calculator
def axis(df: pd.DataFrame):
    r"""Calculate the angles relative to the known global axes
    the local axes are close to.

    .. math::

        \theta_x = \arccos(v_x)

    .. math::

        \theta_y = \arccos(u_y)

    .. math::

        \theta_z = \arccos(w_z)

    Parameters
    ----------
    df : pd.DataFrame
        dataframe with u, v, w coordinate vectors
    """
    df['thetax'] = np.arccos(df.vx)
    df['thetay'] = np.arccos(df.uy)
    df['thetaz'] = np.arccos(df.wz)


axis.__title__ = r"""Axis Angles
$\theta_x = acos(v_x)$ $\theta_y = acos(u_y)$ $\theta_z = acos(w_z)$"""
