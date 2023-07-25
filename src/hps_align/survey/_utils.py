
import math
import numpy as np

def normalize(vec):
	return vec/np.linalg.norm(vec)

def normal_vector(az, el):
	if (el < 0):
		az = az + math.pi
		el = -1.0 * el
	normal = np.array([math.cos(az) * math.cos(el),
		               math.sin(az) * math.cos(el),
		               math.sin(el)])

	return normal
