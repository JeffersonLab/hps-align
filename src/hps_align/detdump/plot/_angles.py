"""module for calculating different angles from coordinate axes"""

import numpy as np
import pandas as pd


def angle_calculator(f):
    """decorator for registering angle calculators"""
    angle_calculator.__registry__[f.__name__] = f
    # set default title
    f.__title__ = f.__name__
    return f


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


@angle_calculator
def expected_axis(df: pd.DataFrame):
    r"""Calculate the angles relative to the known global axes
    the local axes are close to and applying flips when we
    expect them to occur.

    .. math::

        \theta_x = \arccos(\pm v_x)

    .. math::

        \theta_y = \arccos(\pm u_y)

    .. math::

        \theta_z = \arccos(\pm w_z)

    The +/- sign comes from knowledge of how the detector
    was built and is summarized the the following tables.

    .. list-table:: Front
       :widths: 50 25 25 25
       :header-rows: 1

       * - Sensor Type
         - :math:`sign(u \cdot y)`
         - :math:`sign(v \cdot x)`
         - :math:`sign(w \cdot z)`
       * - L12-axial-top
         - :math:`+`
         - :math:`+`
         - :math:`-`
       * - L12-stereo-top
         - :math:`+`
         - :math:`-`
         - :math:`+`
       * - L34-axial-top
         - :math:`+`
         - :math:`+`
         - :math:`-`
       * - L34-stereo-top
         - :math:`-`
         - :math:`+`
         - :math:`+`
       * - L12-axial-bottom
         - :math:`-`
         - :math:`+`
         - :math:`+`
       * - L12-stereo-bottom
         - :math:`-`
         - :math:`-`
         - :math:`-`
       * - L34-axial-bottom
         - :math:`-`
         - :math:`+`
         - :math:`+`
       * - L34-stereo-bottom
         - :math:`+`
         - :math:`+`
         - :math:`-`

    .. list-table:: Back
       :widths: 50 25 25 25
       :header-rows: 1

       * - Sensor Type
         - :math:`sign(u \cdot y)`
         - :math:`sign(v \cdot x)`
         - :math:`sign(w \cdot z)`
       * - axial-slot-top
         - :math:`-`
         - :math:`-`
         - :math:`-`
       * - axial-hole-top
         - :math:`+`
         - :math:`+`
         - :math:`-`
       * - stereo-slot-top
         - :math:`+`
         - :math:`-`
         - :math:`+`
       * - stereo-hole-top
         - :math:`-`
         - :math:`+`
         - :math:`+`
       * - axial-slot-bottom
         - :math:`+`
         - :math:`-`
         - :math:`+`
       * - axial-hole-bottom
         - :math:`-`
         - :math:`+`
         - :math:`+`
       * - stereo-slot-bottom
         - :math:`-`
         - :math:`-`
         - :math:`-`
       * - stereo-hole-bottom
         - :math:`+`
         - :math:`+`
         - :math:`-`


    Parameters
    ----------
    df : pd.DataFrame
        dataframe with u, v, w coordinate vectors
    """

    vx_neg_sl = (
        ((df.lay < 2.5) & (df.sensor.str.contains('stereo'))) |
        (df.sensor.str.contains('slot'))
    )
    uy_neg_sl = (
        ((df.lay > 2.5) & (df.lay < 4.5) & (df.sensor.str.contains('t_stereo')))
        | ((df.lay < 4.5) & (df.sensor.str.contains('b_axial')))
        | ((df.lay < 2.5) & (df.sensor.str.contains('b_stereo')))
        | (df.sensor.str.contains('t_axial_slot'))
        | (df.sensor.str.contains('t_stereo_hole'))
        | (df.sensor.str.contains('b_axial_hole'))
        | (df.sensor.str.contains('b_stereo_slot'))
    )
    wz_neg_sl = (
        df.sensor.str.contains('t_axial')
        | df.sensor.str.contains('b_stereo')
    )

    # check for 2016
    if not any(df.sensor.str.contains('L7')):
        # change slices for 2016
        #   Front only has three layers now
        #   All three front layers behave together
        #   (i.e. no L12/L34 separate like there is above
        vx_neg_sl = (
            (df.sensor.str.contains('slot'))
        )
        uy_neg_sl = (
            ((df.lay < 3.5) & (df.sensor.str.contains('t_stereo')))
            | ((df.lay < 3.5) & (df.sensor.str.contains('b_axial')))
            | (df.sensor.str.contains('t_axial_slot'))
            | (df.sensor.str.contains('t_stereo_hole'))
            | (df.sensor.str.contains('b_axial_hole'))
            | (df.sensor.str.contains('b_stereo_slot'))
        )

    df['thetax'] = np.arccos((-1*vx_neg_sl+1*(~vx_neg_sl))*df.vx)
    df['thetay'] = np.arccos((-1*uy_neg_sl+1*(~uy_neg_sl))*df.uy)
    df['thetaz'] = np.arccos((-1*wz_neg_sl+1*(~wz_neg_sl))*df.wz)


axis.__title__ = r"""Expected Axis Angles
$\theta_x = acos(\pm v_x)$ $\theta_y = acos(\pm u_y)$ $\theta_z = acos(\pm w_z)$"""
