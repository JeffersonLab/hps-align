
import unittest
import numpy as np
import hps_align.survey._utils as utils


class TestNormalize(unittest.TestCase):

    def test_length(self):
        vec = np.array([1, 2, 3])
        norm = utils.normalize(vec)
        self.assertAlmostEqual(1, np.linalg.norm(norm))

        vec = np.array([0.1, 0, 0])
        norm = utils.normalize(vec)
        self.assertAlmostEqual(1, np.linalg.norm(norm))

        vec = np.array([2, -1, 3])
        norm = utils.normalize(vec)
        self.assertAlmostEqual(1, np.linalg.norm(norm))

        vec = np.array([0, 0, 0])
        norm = utils.normalize(vec)
        self.assertEqual(0, np.linalg.norm(norm))

        vec = np.array([0.05, -0.1, -0.3])
        norm = utils.normalize(vec)
        self.assertAlmostEqual(1, np.linalg.norm(norm))

    def test_direction(self):
        vec = np.array([1, 2, 3])
        norm = utils.normalize(vec)
        self.assertAlmostEqual(vec[0]/vec[1], norm[0]/norm[1])
        self.assertAlmostEqual(vec[0]/vec[2], norm[0]/norm[2])
        self.assertAlmostEqual(vec[1]/vec[2], norm[1]/norm[2])

        vec = np.array([0.1, 0, 0])
        norm = utils.normalize(vec)
        self.assertEqual(1, norm[0])

        vec = np.array([2, -1, 3])
        norm = utils.normalize(vec)
        self.assertAlmostEqual(vec[0]/vec[1], norm[0]/norm[1])
        self.assertAlmostEqual(vec[0]/vec[2], norm[0]/norm[2])
        self.assertAlmostEqual(vec[1]/vec[2], norm[1]/norm[2])

        vec = np.array([0.05, -0.1, -0.3])
        norm = utils.normalize(vec)
        self.assertAlmostEqual(vec[0]/vec[1], norm[0]/norm[1])
        self.assertAlmostEqual(vec[0]/vec[2], norm[0]/norm[2])
        self.assertAlmostEqual(vec[1]/vec[2], norm[1]/norm[2])


class TestNormalVector(unittest.TestCase):

    def test_direction(self):
        normal_vector = utils.normal_vector(0, 0)
        self.assertAlmostEqual(1, normal_vector[0])
        self.assertAlmostEqual(0, normal_vector[1])
        self.assertAlmostEqual(0, normal_vector[2])

        normal_vector = utils.normal_vector(np.pi/2, 0)
        self.assertAlmostEqual(0, normal_vector[0])
        self.assertAlmostEqual(1, normal_vector[1])
        self.assertAlmostEqual(0, normal_vector[2])

        normal_vector = utils.normal_vector(0, np.pi/2)
        self.assertAlmostEqual(0, normal_vector[0])
        self.assertAlmostEqual(0, normal_vector[1])
        self.assertAlmostEqual(1, normal_vector[2])

        normal_vector = utils.normal_vector(2, np.pi/2)
        self.assertAlmostEqual(0, normal_vector[0])
        self.assertAlmostEqual(0, normal_vector[1])
        self.assertAlmostEqual(1, normal_vector[2])

        normal_vector = utils.normal_vector(0, -np.pi/2)
        self.assertAlmostEqual(0, normal_vector[0])
        self.assertAlmostEqual(0, normal_vector[1])
        self.assertAlmostEqual(1, normal_vector[2])

        normal_vector = utils.normal_vector(np.pi/2, np.pi/4)    
        self.assertAlmostEqual(0, normal_vector[0])
        self.assertAlmostEqual(1/np.sqrt(2), normal_vector[1])
        self.assertAlmostEqual(1/np.sqrt(2), normal_vector[2])

        normal_vector = utils.normal_vector(np.pi/2, -np.pi/4)    
        self.assertAlmostEqual(0, normal_vector[0])
        self.assertAlmostEqual(-1/np.sqrt(2), normal_vector[1])
        self.assertAlmostEqual(1/np.sqrt(2), normal_vector[2])   


class TestOrthogonalize(unittest.TestCase):

    def test_direction(self):
        vec1 = np.array([1, 0, 0])
        vec2 = np.array([1, 1, 0])
        ortho = utils.orthogonalize(vec1, vec2)
        self.assertAlmostEqual(0, ortho[0])
        self.assertAlmostEqual(1, ortho[1])
        self.assertAlmostEqual(0, ortho[2])
        self.assertAlmostEqual(0, np.dot(vec1, ortho))

        vec1 = np.array([1, 0, 0])
        vec2 = np.array([0, 1, 1])
        ortho = utils.orthogonalize(vec1, vec2)
        self.assertAlmostEqual(0, ortho[0])
        self.assertAlmostEqual(1, ortho[1])
        self.assertAlmostEqual(1, ortho[2])
        self.assertAlmostEqual(0, np.dot(vec1, ortho))

        vec1 = np.array([1, 0, 1])
        vec2 = np.array([2, 3, 1])
        ortho = utils.orthogonalize(vec1, vec2)
        self.assertAlmostEqual(0.5, ortho[0])
        self.assertAlmostEqual(3, ortho[1])
        self.assertAlmostEqual(-0.5, ortho[2])
        self.assertAlmostEqual(0, np.dot(vec1, ortho))

        vec1 = np.array([1, 0, 0])
        vec2 = np.array([-1, 1, 0])
        ortho = utils.orthogonalize(vec1, vec2)
        self.assertAlmostEqual(0, ortho[0])
        self.assertAlmostEqual(1, ortho[1])
        self.assertAlmostEqual(0, ortho[2])
        self.assertAlmostEqual(0, np.dot(vec1, ortho))

        vec1 = np.array([1, 0, -1])
        vec2 = np.array([-2, -3, 1])
        ortho = utils.orthogonalize(vec1, vec2)
        self.assertAlmostEqual(-0.5, ortho[0])
        self.assertAlmostEqual(-3, ortho[1])
        self.assertAlmostEqual(-0.5, ortho[2])
        self.assertAlmostEqual(0, np.dot(vec1, ortho))

        vec1 = np.array([1, 0, 0])
        vec2 = np.array([0, 0, 0])
        ortho = utils.orthogonalize(vec1, vec2)
        self.assertAlmostEqual(0, ortho[0])
        self.assertAlmostEqual(0, ortho[1])
        self.assertAlmostEqual(0, ortho[2])
        self.assertAlmostEqual(0, np.dot(vec1, ortho))

        vec1 = np.array([0, 0, 0])
        vec2 = np.array([1, 0, 0])
        ortho = utils.orthogonalize(vec1, vec2)
        self.assertAlmostEqual(1, ortho[0])
        self.assertAlmostEqual(0, ortho[1])
        self.assertAlmostEqual(0, ortho[2])
        self.assertAlmostEqual(0, np.dot(vec1, ortho))


class TestMakeBasis(unittest.TestCase):

    def test_direction(self):
        basis = utils.make_basis(np.array([1, 0, 0]), np.array([0, 1, 0]))
        self.assertAlmostEqual(1, basis[0][0])
        self.assertAlmostEqual(0, basis[0][1])
        self.assertAlmostEqual(0, basis[0][2])
        self.assertAlmostEqual(0, basis[1][0])
        self.assertAlmostEqual(1, basis[1][1])
        self.assertAlmostEqual(0, basis[1][2])
        self.assertAlmostEqual(0, basis[2][0])
        self.assertAlmostEqual(0, basis[2][1])
        self.assertAlmostEqual(1, basis[2][2])

        basis = utils.make_basis(np.array([1, 0, 0]), np.array([0, 0, 1]))
        self.assertAlmostEqual(1, basis[0][0])
        self.assertAlmostEqual(0, basis[0][1])
        self.assertAlmostEqual(0, basis[0][2])
        self.assertAlmostEqual(0, basis[1][0])
        self.assertAlmostEqual(0, basis[1][1])
        self.assertAlmostEqual(1, basis[1][2])
        self.assertAlmostEqual(0, basis[2][0])
        self.assertAlmostEqual(-1, basis[2][1])
        self.assertAlmostEqual(0, basis[2][2])

        basis = utils.make_basis(np.array([0, 1, 0]), np.array([0, 0, 1]))
        self.assertAlmostEqual(0, basis[0][0])
        self.assertAlmostEqual(1, basis[0][1])
        self.assertAlmostEqual(0, basis[0][2])
        self.assertAlmostEqual(0, basis[1][0])
        self.assertAlmostEqual(0, basis[1][1])
        self.assertAlmostEqual(1, basis[1][2])
        self.assertAlmostEqual(1, basis[2][0])
        self.assertAlmostEqual(0, basis[2][1])
        self.assertAlmostEqual(0, basis[2][2])

        basis = utils.make_basis(np.array([1, 0, 0]), np.array([1, 1, 0]))
        self.assertAlmostEqual(1, basis[0][0])
        self.assertAlmostEqual(0, basis[0][1])
        self.assertAlmostEqual(0, basis[0][2])
        self.assertAlmostEqual(0, basis[1][0])
        self.assertAlmostEqual(1, basis[1][1])
        self.assertAlmostEqual(0, basis[1][2])
        self.assertAlmostEqual(0, basis[2][0])
        self.assertAlmostEqual(0, basis[2][1])
        self.assertAlmostEqual(1, basis[2][2])

        basis = utils.make_basis(np.array([1, 0, -1]), np.array([-2, -3, 1]))
        self.assertAlmostEqual(1/np.sqrt(2), basis[0][0])
        self.assertAlmostEqual(0, basis[0][1])
        self.assertAlmostEqual(-1/np.sqrt(2), basis[0][2])
        self.assertAlmostEqual(-0.5/np.sqrt(9.5), basis[1][0])
        self.assertAlmostEqual(-3/np.sqrt(9.5), basis[1][1])
        self.assertAlmostEqual(-0.5/np.sqrt(9.5), basis[1][2])
        self.assertAlmostEqual(-3/np.sqrt(19), basis[2][0])
        self.assertAlmostEqual(1/np.sqrt(19), basis[2][1])
        self.assertAlmostEqual(-3/np.sqrt(19), basis[2][2])

        basis = utils.make_basis(np.array([1, 0, 0]), np.array([0, 0, 0]))
        self.assertAlmostEqual(1, basis[0][0])
        self.assertAlmostEqual(0, basis[0][1])
        self.assertAlmostEqual(0, basis[0][2])
        self.assertAlmostEqual(0, basis[1][0])
        self.assertAlmostEqual(0, basis[1][1])
        self.assertAlmostEqual(0, basis[1][2])
        self.assertAlmostEqual(0, basis[2][0])
        self.assertAlmostEqual(0, basis[2][1])
        self.assertAlmostEqual(0, basis[2][2])

    def test_length(self):
        basis = utils.make_basis(np.array([1, 0, -1]), np.array([-2, -3, 0]))
        self.assertAlmostEqual(1, np.linalg.norm(basis[0]))
        self.assertAlmostEqual(1, np.linalg.norm(basis[1]))
        self.assertAlmostEqual(1, np.linalg.norm(basis[2]))

        basis = utils.make_basis(np.array([-0.8, 0.05, 0]), np.array([0, 0.1, 0]))
        self.assertAlmostEqual(1, np.linalg.norm(basis[0]))
        self.assertAlmostEqual(1, np.linalg.norm(basis[1]))
        self.assertAlmostEqual(1, np.linalg.norm(basis[2]))

        basis = utils.make_basis(np.array([0, 0, 0]), np.array([0, 0, 0]))
        self.assertAlmostEqual(0, np.linalg.norm(basis[0]))
        self.assertAlmostEqual(0, np.linalg.norm(basis[1]))
        self.assertAlmostEqual(0, np.linalg.norm(basis[2]))

        basis = utils.make_basis(np.array([102.45, -237, 0.003]), np.array([-0.0001, 20.5, 3333]))
        self.assertAlmostEqual(1, np.linalg.norm(basis[0]))
        self.assertAlmostEqual(1, np.linalg.norm(basis[1]))
        self.assertAlmostEqual(1, np.linalg.norm(basis[2]))


class TestProjectToPlane(unittest.TestCase):

    def test_direction(self):
        vec = np.array([5, 1, 0])
        plane_origin = np.array([0, 0, 0])
        plane_normal = np.array([1, 0, 0])
        proj = utils.project_to_plane(vec, plane_origin, plane_normal)
        self.assertAlmostEqual(0, proj[0])
        self.assertAlmostEqual(1, proj[1])
        self.assertAlmostEqual(0, proj[2])

        vec = np.array([5, 1, 0])
        plane_origin = np.array([2, 0, 0])
        plane_normal = np.array([1, 0, 0])
        proj = utils.project_to_plane(vec, plane_origin, plane_normal)
        self.assertAlmostEqual(2, proj[0])
        self.assertAlmostEqual(1, proj[1])
        self.assertAlmostEqual(0, proj[2])

        vec = np.array([5, 1, 0])
        plane_origin = np.array([0, 0, 0])
        plane_normal = np.array([0, 1, 0])
        proj = utils.project_to_plane(vec, plane_origin, plane_normal)
        self.assertAlmostEqual(5, proj[0])
        self.assertAlmostEqual(0, proj[1])
        self.assertAlmostEqual(0, proj[2])

        vec = np.array([-5, 1, 0])
        plane_origin = np.array([0, 0, 0])
        plane_normal = np.array([1, 0, 0])
        proj = utils.project_to_plane(vec, plane_origin, plane_normal)
        self.assertAlmostEqual(0, proj[0])
        self.assertAlmostEqual(1, proj[1])
        self.assertAlmostEqual(0, proj[2])

        vec = np.array([5, 1, 0])
        plane_origin = np.array([0, 1, 0])
        plane_normal = np.array([0, 0, 1])
        proj = utils.project_to_plane(vec, plane_origin, plane_normal)
        self.assertAlmostEqual(5, proj[0])
        self.assertAlmostEqual(1, proj[1])
        self.assertAlmostEqual(0, proj[2])


if __name__ == '__main__':
    unittest.main()
