import unittest
from tests.core import TestCore
from pyrep.objects.shape import Shape
from pyrep.const import PrimitiveShape, TextureMappingMode
from tests.core import ASSET_DIR
from os import path
import numpy as np


class TestShapes(TestCore):

    def setUp(self):
        super().setUp()
        self.dynamic_cube = Shape('dynamic_cube')

    def test_create_primitive_simple(self):
        pr = Shape.create(
            PrimitiveShape.CUBOID, size=[1., 1., 1.])
        self.assertIsInstance(pr, Shape)

    def test_create_primitive_complex(self):
        pr = Shape.create(
            PrimitiveShape.CUBOID, size=[1., 1., 1.], mass=2.0,
            smooth=True, respondable=True, static=False,
            position=[1.1, 1.2, 1.3], orientation=[0.1, 0.2, 0.3],
            color=[0.7, 0.8, 0.9])
        self.assertIsInstance(pr, Shape)
        self.assertTrue(np.allclose(pr.get_position(), [1.1, 1.2, 1.3]))
        self.assertTrue(np.allclose(pr.get_orientation(), [0.1, 0.2, 0.3]))
        self.assertTrue(np.allclose(pr.get_color(), [0.7, 0.8, 0.9]))

    def test_import_mesh(self):
        ob = Shape.import_mesh(
            path.join(ASSET_DIR, 'test_mesh_bowl.obj'))
        self.assertIsInstance(ob, Shape)

    def test_create_mesh(self):
        ob = Shape.create_mesh(
            vertices=[-0.1, -0.1, 0.0,
                      -0.1, 0.1, 0.0,
                      0.1, 0.0, 0.0], indices=[0, 1, 2])
        self.assertIsInstance(ob, Shape)

    def test_convex_decompose(self):
        ob = Shape.import_mesh(
            path.join(ASSET_DIR, 'test_mesh_bowl.obj'))
        self.assertIsInstance(ob, Shape)
        cd_1 = ob.get_convex_decomposition()
        self.assertIsInstance(cd_1, Shape)
        self.assertNotEqual(ob, cd_1)
        cd_2 = ob.get_convex_decomposition(morph=True)
        self.assertIsInstance(cd_2, Shape)
        self.assertEqual(ob, cd_2)

    def test_get_set_color(self):
        self.dynamic_cube.set_color([.5] * 3)
        self.assertEqual(self.dynamic_cube.get_color(), [.5] * 3)

    def test_get_set_mass(self):
        self.dynamic_cube.set_mass(3.5)
        self.assertEqual(self.dynamic_cube.get_mass(), 3.5)

    def test_get_set_respondable(self):
        self.dynamic_cube.set_respondable(False)
        self.assertFalse(self.dynamic_cube.is_respondable())
        self.dynamic_cube.set_respondable(True)
        self.assertTrue(self.dynamic_cube.is_respondable())

    def test_get_set_dynamic(self):
        self.dynamic_cube.set_dynamic(False)
        self.assertFalse(self.dynamic_cube.is_dynamic())
        self.dynamic_cube.set_dynamic(True)
        self.assertTrue(self.dynamic_cube.is_dynamic())

    def test_get_mesh_data(self):
        vertices, indices, normals = self.dynamic_cube.get_mesh_data()
        self.assertEqual(len(vertices), 24)
        self.assertEqual(len(indices), 36)
        self.assertEqual(len(normals), 108)

    def test_set_texture(self):
        _, texture = self.pyrep.create_texture(
            path.join(ASSET_DIR, 'wood_texture.jpg'))
        self.dynamic_cube.set_texture(texture, TextureMappingMode.CUBE)
        self.assertEqual(texture.get_texture_id(),
                         self.dynamic_cube.get_texture().get_texture_id())


if __name__ == '__main__':
    unittest.main()
