
import math
import numpy as np

def normalize(vec):
	"""Normalize a vector"""
	return vec/np.linalg.norm(vec)

def normal_vector(az, el):
	"""Return normal vector from azimuth and elevation angles"""
	if (el < 0):
		az = az + math.pi
		el = -1.0 * el
	normal = np.array([math.cos(az) * math.cos(el),
		               math.sin(az) * math.cos(el),
		               math.sin(el)])

	return normal

def orthogonalize(vec1, vec2):
	"""Orthogonalize vec2 with respect to vec1"""
	return vec2 - np.dot(vec1, vec2)/np.linalg.norm(vec1) * vec1

def make_basis(vec1, vec2):
    """Make orthonormal basis from two vectors"""
    basis = np.empty([3,3])

    basis[0] = normalize(vec1)
    basis[1] = normalize(orthogonalize(vec1, vec2))
    basis[2] = np.cross(basis[0], basis[1])
    # TODO: check if this is RH coord sys

    return basis