from itertools import product
from unittest import TestCase

from mcwb import Anchor3, Vec3, Volume


class TestVolume(TestCase):
    """Tests the Volume constructor."""

    def test_anchors_odd_size(self):
        size = Vec3(3, 3, 3)
        position = Vec3(0, 0, 0)

        v = Volume.from_anchor(position, size, anchor=Anchor3.MIDDLE)
        self.assertTrue(v.position == position)
        self.assertTrue(v.start == Vec3(-1, -1, -1))
        self.assertTrue(v.end == Vec3(1, 1, 1))
        self.assertTrue(v.size == size)

        v = Volume.from_anchor(position, size, anchor=Anchor3.BOTTOM_NW)
        self.assertTrue(v.position == position)
        self.assertTrue(v.start == Vec3(0, 0, 0))
        self.assertTrue(v.end == Vec3(2, 2, 2))
        self.assertTrue(v.size == size)

        v = Volume.from_anchor(position, size, anchor=Anchor3.BOTTOM_NE)
        self.assertTrue(v.position == position)
        self.assertTrue(v.start == Vec3(-2, 0, 0))
        self.assertTrue(v.end == Vec3(0, 2, 2))
        self.assertTrue(v.size == size)

        v = Volume.from_anchor(position, size, anchor=Anchor3.BOTTOM_SE)
        self.assertTrue(v.position == position)
        self.assertTrue(v.start == Vec3(-2, 0, -2))
        self.assertTrue(v.end == Vec3(0, 2, 0))
        self.assertTrue(v.size == size)

        v = Volume.from_anchor(position, size, anchor=Anchor3.BOTTOM_SW)
        self.assertTrue(v.position == position)
        self.assertTrue(v.start == Vec3(0, 0, -2))
        self.assertTrue(v.end == Vec3(2, 2, 0))
        self.assertTrue(v.size == size)

        v = Volume.from_anchor(position, size, anchor=Anchor3.BOTTOM_MIDDLE)
        self.assertTrue(v.position == position)
        self.assertTrue(v.start == Vec3(-1, 0, -1))
        self.assertTrue(v.end == Vec3(1, 2, 1))
        self.assertTrue(v.size == size)

        v = Volume.from_anchor(position, size, anchor=Anchor3.TOP_NW)
        self.assertTrue(v.position == position)
        self.assertTrue(v.start == Vec3(0, -2, 0))
        self.assertTrue(v.end == Vec3(2, 0, 2))
        self.assertTrue(v.size == size)

        v = Volume.from_anchor(position, size, anchor=Anchor3.TOP_NE)
        self.assertTrue(v.position == position)
        self.assertTrue(v.start == Vec3(-2, -2, 0))
        self.assertTrue(v.end == Vec3(0, 0, 2))
        self.assertTrue(v.size == size)

        v = Volume.from_anchor(position, size, anchor=Anchor3.TOP_SE)
        self.assertTrue(v.position == position)
        self.assertTrue(v.start == Vec3(-2, -2, -2))
        self.assertTrue(v.end == Vec3(0, 0, 0))
        self.assertTrue(v.size == size)

        v = Volume.from_anchor(position, size, anchor=Anchor3.TOP_SW)
        self.assertTrue(v.position == position)
        self.assertTrue(v.start == Vec3(0, -2, -2))
        self.assertTrue(v.end == Vec3(2, 0, 0))
        self.assertTrue(v.size == size)

        v = Volume.from_anchor(position, size, anchor=Anchor3.TOP_MIDDLE)
        self.assertTrue(v.position == position)
        self.assertTrue(v.start == Vec3(-1, -2, -1))
        self.assertTrue(v.end == Vec3(1, 0, 1))
        self.assertTrue(v.size == size)

    def test_anchors_even_size(self):
        size = Vec3(4, 4, 4)
        position = Vec3(0, 0, 0)

        v = Volume.from_anchor(position, size, anchor=Anchor3.MIDDLE)
        self.assertTrue(v.position == position)
        self.assertTrue(v.start == Vec3(-2, -2, -2))
        self.assertTrue(v.end == Vec3(1, 1, 1))
        self.assertTrue(v.size == size)

        v = Volume.from_anchor(position, size, anchor=Anchor3.BOTTOM_NW)
        self.assertTrue(v.position == position)
        self.assertTrue(v.start == Vec3(0, 0, 0))
        self.assertTrue(v.end == Vec3(3, 3, 3))
        self.assertTrue(v.size == size)

        v = Volume.from_anchor(position, size, anchor=Anchor3.BOTTOM_NE)
        self.assertTrue(v.position == position)
        self.assertTrue(v.start == Vec3(-3, 0, 0))
        self.assertTrue(v.end == Vec3(0, 3, 3))
        self.assertTrue(v.size == size)

    def test_bounds_odd_size(self):
        size = Vec3(3, 3, 3)
        position = Vec3(-1, -1, -1)

        for x, y, z in product([1, -1], [1, -1], [1, -1]):
            start = Vec3(x, y, z)
            opposite = Vec3(-x, -y, -z)
            print(start, opposite)
            v = Volume.from_corners(start, end=opposite)
            print(v.start, v.end, v.position, v.size)
            self.assertTrue(v.position == position)
            self.assertTrue(v.size == size)
