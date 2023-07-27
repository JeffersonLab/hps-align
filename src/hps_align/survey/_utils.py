
import math
import numpy as np


def normalize(vec):
    """Normalize a vector"""
    if np.linalg.norm(vec) == 0:
        return vec
    return vec/np.linalg.norm(vec)


def normal_vector(az, el):
    """Return normal vector from azimuth and elevation angles

    Parameters
    ----------
    az : float
        Azimuth angle in radians
    el : float
        Elevation angle in radians

    Returns
    -------
    normal : np.array
        Normal vector
    """
    if (el < 0):
        az = az + math.pi
        el = -1.0 * el
    # def of el shifted by 90 deg compared to standard spherical coords
    normal = np.array([math.cos(az) * math.cos(el),
                       math.sin(az) * math.cos(el),
                       math.sin(el)])

    return normal


def orthogonalize(vec1, vec2):
    """Orthogonalize vec2 with respect to vec1"""
    if np.dot(vec1, vec1) == 0:
        return vec2
    return vec2 - np.dot(vec1, vec2)/np.dot(vec1, vec1) * vec1


def make_basis(vec1, vec2):
    """Make orthonormal basis from two vectors
    
    Parameters
    ----------
    vec1 : np.array
        First vector, will be normalized
    vec2 : np.array
        Second vector, will be orthogonalized with respect to vec1, then normalized

    Returns
    -------
    basis : np.array
        Orthonormal basis
    """
    basis = np.empty([3, 3])

    basis[0] = normalize(vec1)
    basis[1] = normalize(orthogonalize(vec1, vec2))
    basis[2] = np.cross(basis[0], basis[1])

    return basis


def project_to_plane(vec, plane_origin, plane_normal):
    """Project a vector onto a plane"""
    # TODO check this
    return vec - np.dot(vec - plane_origin, plane_normal) * plane_normal


if __name__ == '__main__':
    print(normalize(np.array([1, 0, 0])))
