"""Tests the functions module."""

from functools import partial
from itertools import product
from unittest import TestCase

from mcipc.rcon.enumerations import Item

from mcwb.functions import get_direction, normalize, offsets, validate, y_rotate
from mcwb.types import Anchor, Direction, Vec3


class TestGetDirection(TestCase):
    """Tests the get_direction() function."""

    def setUp(self):
        """Sets example directions."""
        self.valid_direction_x = (Vec3(10, -9, 3), Vec3(91, -9, 3))
        self.direction_vector_x = Vec3(81, 0, 0)
        self.valid_direction_y = (Vec3(10, -9, 3), Vec3(10, 200, 3))
        self.direction_vector_y = Vec3(0, 209, 0)
        self.valid_direction_z = (Vec3(10, -9, 3), Vec3(10, -9, -5))
        self.direction_vector_z = Vec3(0, 0, -8)
        self.invalid_direction = (Vec3(1, 2, -3), Vec3(-4, -5, 6))

    def test_valid_direction_x(self):
        """Tests the results of get_direction()."""
        self.assertEqual(get_direction(*self.valid_direction_x),
                         self.direction_vector_x)
        self.assertEqual(get_direction(*self.valid_direction_y),
                         self.direction_vector_y)
        self.assertEqual(get_direction(*self.valid_direction_z),
                         self.direction_vector_z)
        self.assertRaises(ValueError,
                          partial(get_direction, *self.invalid_direction))


class TestNormalize(TestCase):
    """Tests the normalize() function."""

    def setUp(self):
        """Sets example profiles."""
        self.valid_profile_template = [
            [Item.RED_CONCRETE, None, Item.GREEN_CONCRETE],
            [None, None, None],
            [Item.BLUE_CONCRETE, None, Item.YELLOW_CONCRETE],
        ]
        self.valid_profile_air = [
            [Item.RED_CONCRETE, Item.AIR, Item.GREEN_CONCRETE],
            [Item.AIR, Item.AIR, Item.AIR],
            [Item.BLUE_CONCRETE, Item.AIR, Item.YELLOW_CONCRETE],
        ]

    def test_normalize(self):
        """Tests the normalization of the profile template."""
        self.assertEqual(
            list(normalize(self.valid_profile_template, Item.AIR)),
            self.valid_profile_air)


class TestOffsets(TestCase):
    """Tests the offsets() function."""

    def setUp(self):
        """Sets example profiles, directions and vectors."""
        self.valid_profile = [
            [Item.RED_CONCRETE, Item.AIR, Item.GREEN_CONCRETE],
            [Item.AIR, Item.AIR, Item.AIR],
            [Item.BLUE_CONCRETE, Item.AIR, Item.YELLOW_CONCRETE],
        ]
        self.directions = Direction.all()
        self.anchors = Anchor
        self.results = [
            [
                (Item.RED_CONCRETE, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=-1, y=0, z=0)),
                (Item.GREEN_CONCRETE, Vec3(x=-2, y=0, z=0)),
                (Item.AIR, Vec3(x=0, y=-1, z=0)),
                (Item.AIR, Vec3(x=-1, y=-1, z=0)),
                (Item.AIR, Vec3(x=-2, y=-1, z=0)),
                (Item.BLUE_CONCRETE, Vec3(x=0, y=-2, z=0)),
                (Item.AIR, Vec3(x=-1, y=-2, z=0)),
                (Item.YELLOW_CONCRETE, Vec3(x=-2, y=-2, z=0)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=2, y=0, z=0)),
                (Item.AIR, Vec3(x=1, y=0, z=0)),
                (Item.GREEN_CONCRETE, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=2, y=-1, z=0)),
                (Item.AIR, Vec3(x=1, y=-1, z=0)),
                (Item.AIR, Vec3(x=0, y=-1, z=0)),
                (Item.BLUE_CONCRETE, Vec3(x=2, y=-2, z=0)),
                (Item.AIR, Vec3(x=1, y=-2, z=0)),
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=-2, z=0)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=0, y=2, z=0)),
                (Item.AIR, Vec3(x=-1, y=2, z=0)),
                (Item.GREEN_CONCRETE, Vec3(x=-2, y=2, z=0)),
                (Item.AIR, Vec3(x=0, y=1, z=0)),
                (Item.AIR, Vec3(x=-1, y=1, z=0)),
                (Item.AIR, Vec3(x=-2, y=1, z=0)),
                (Item.BLUE_CONCRETE, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=-1, y=0, z=0)),
                (Item.YELLOW_CONCRETE, Vec3(x=-2, y=0, z=0)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=2, y=2, z=0)),
                (Item.AIR, Vec3(x=1, y=2, z=0)),
                (Item.GREEN_CONCRETE, Vec3(x=0, y=2, z=0)),
                (Item.AIR, Vec3(x=2, y=1, z=0)),
                (Item.AIR, Vec3(x=1, y=1, z=0)),
                (Item.AIR, Vec3(x=0, y=1, z=0)),
                (Item.BLUE_CONCRETE, Vec3(x=2, y=0, z=0)),
                (Item.AIR, Vec3(x=1, y=0, z=0)),
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=0, z=0)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=1, y=1, z=0)),
                (Item.AIR, Vec3(x=0, y=1, z=0)),
                (Item.GREEN_CONCRETE, Vec3(x=-1, y=1, z=0)),
                (Item.AIR, Vec3(x=1, y=0, z=0)),
                (Item.AIR, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=-1, y=0, z=0)),
                (Item.BLUE_CONCRETE, Vec3(x=1, y=-1, z=0)),
                (Item.AIR, Vec3(x=0, y=-1, z=0)),
                (Item.YELLOW_CONCRETE, Vec3(x=-1, y=-1, z=0)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=0, y=0, z=-1)),
                (Item.GREEN_CONCRETE, Vec3(x=0, y=0, z=-2)),
                (Item.AIR, Vec3(x=0, y=-1, z=0)),
                (Item.AIR, Vec3(x=0, y=-1, z=-1)),
                (Item.AIR, Vec3(x=0, y=-1, z=-2)),
                (Item.BLUE_CONCRETE, Vec3(x=0, y=-2, z=0)),
                (Item.AIR, Vec3(x=0, y=-2, z=-1)),
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=-2, z=-2)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=0, y=0, z=2)),
                (Item.AIR, Vec3(x=0, y=0, z=1)),
                (Item.GREEN_CONCRETE, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=0, y=-1, z=2)),
                (Item.AIR, Vec3(x=0, y=-1, z=1)),
                (Item.AIR, Vec3(x=0, y=-1, z=0)),
                (Item.BLUE_CONCRETE, Vec3(x=0, y=-2, z=2)),
                (Item.AIR, Vec3(x=0, y=-2, z=1)),
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=-2, z=0)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=0, y=2, z=0)),
                (Item.AIR, Vec3(x=0, y=2, z=-1)),
                (Item.GREEN_CONCRETE, Vec3(x=0, y=2, z=-2)),
                (Item.AIR, Vec3(x=0, y=1, z=0)),
                (Item.AIR, Vec3(x=0, y=1, z=-1)),
                (Item.AIR, Vec3(x=0, y=1, z=-2)),
                (Item.BLUE_CONCRETE, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=0, y=0, z=-1)),
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=0, z=-2)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=0, y=2, z=2)),
                (Item.AIR, Vec3(x=0, y=2, z=1)),
                (Item.GREEN_CONCRETE, Vec3(x=0, y=2, z=0)),
                (Item.AIR, Vec3(x=0, y=1, z=2)),
                (Item.AIR, Vec3(x=0, y=1, z=1)),
                (Item.AIR, Vec3(x=0, y=1, z=0)),
                (Item.BLUE_CONCRETE, Vec3(x=0, y=0, z=2)),
                (Item.AIR, Vec3(x=0, y=0, z=1)),
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=0, z=0)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=0, y=1, z=1)),
                (Item.AIR, Vec3(x=0, y=1, z=0)),
                (Item.GREEN_CONCRETE, Vec3(x=0, y=1, z=-1)),
                (Item.AIR, Vec3(x=0, y=0, z=1)),
                (Item.AIR, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=0, y=0, z=-1)),
                (Item.BLUE_CONCRETE, Vec3(x=0, y=-1, z=1)),
                (Item.AIR, Vec3(x=0, y=-1, z=0)),
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=-1, z=-1)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=1, y=0, z=0)),
                (Item.GREEN_CONCRETE, Vec3(x=2, y=0, z=0)),
                (Item.AIR, Vec3(x=0, y=-1, z=0)),
                (Item.AIR, Vec3(x=1, y=-1, z=0)),
                (Item.AIR, Vec3(x=2, y=-1, z=0)),
                (Item.BLUE_CONCRETE, Vec3(x=0, y=-2, z=0)),
                (Item.AIR, Vec3(x=1, y=-2, z=0)),
                (Item.YELLOW_CONCRETE, Vec3(x=2, y=-2, z=0)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=-2, y=0, z=0)),
                (Item.AIR, Vec3(x=-1, y=0, z=0)),
                (Item.GREEN_CONCRETE, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=-2, y=-1, z=0)),
                (Item.AIR, Vec3(x=-1, y=-1, z=0)),
                (Item.AIR, Vec3(x=0, y=-1, z=0)),
                (Item.BLUE_CONCRETE, Vec3(x=-2, y=-2, z=0)),
                (Item.AIR, Vec3(x=-1, y=-2, z=0)),
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=-2, z=0)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=0, y=2, z=0)),
                (Item.AIR, Vec3(x=1, y=2, z=0)),
                (Item.GREEN_CONCRETE, Vec3(x=2, y=2, z=0)),
                (Item.AIR, Vec3(x=0, y=1, z=0)),
                (Item.AIR, Vec3(x=1, y=1, z=0)),
                (Item.AIR, Vec3(x=2, y=1, z=0)),
                (Item.BLUE_CONCRETE, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=1, y=0, z=0)),
                (Item.YELLOW_CONCRETE, Vec3(x=2, y=0, z=0)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=-2, y=2, z=0)),
                (Item.AIR, Vec3(x=-1, y=2, z=0)),
                (Item.GREEN_CONCRETE, Vec3(x=0, y=2, z=0)),
                (Item.AIR, Vec3(x=-2, y=1, z=0)),
                (Item.AIR, Vec3(x=-1, y=1, z=0)),
                (Item.AIR, Vec3(x=0, y=1, z=0)),
                (Item.BLUE_CONCRETE, Vec3(x=-2, y=0, z=0)),
                (Item.AIR, Vec3(x=-1, y=0, z=0)),
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=0, z=0)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=-1, y=1, z=0)),
                (Item.AIR, Vec3(x=0, y=1, z=0)),
                (Item.GREEN_CONCRETE, Vec3(x=1, y=1, z=0)),
                (Item.AIR, Vec3(x=-1, y=0, z=0)),
                (Item.AIR, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=1, y=0, z=0)),
                (Item.BLUE_CONCRETE, Vec3(x=-1, y=-1, z=0)),
                (Item.AIR, Vec3(x=0, y=-1, z=0)),
                (Item.YELLOW_CONCRETE, Vec3(x=1, y=-1, z=0)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=0, y=0, z=1)),
                (Item.GREEN_CONCRETE, Vec3(x=0, y=0, z=2)),
                (Item.AIR, Vec3(x=0, y=-1, z=0)),
                (Item.AIR, Vec3(x=0, y=-1, z=1)),
                (Item.AIR, Vec3(x=0, y=-1, z=2)),
                (Item.BLUE_CONCRETE, Vec3(x=0, y=-2, z=0)),
                (Item.AIR, Vec3(x=0, y=-2, z=1)),
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=-2, z=2)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=0, y=0, z=-2)),
                (Item.AIR, Vec3(x=0, y=0, z=-1)),
                (Item.GREEN_CONCRETE, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=0, y=-1, z=-2)),
                (Item.AIR, Vec3(x=0, y=-1, z=-1)),
                (Item.AIR, Vec3(x=0, y=-1, z=0)),
                (Item.BLUE_CONCRETE, Vec3(x=0, y=-2, z=-2)),
                (Item.AIR, Vec3(x=0, y=-2, z=-1)),
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=-2, z=0)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=0, y=2, z=0)),
                (Item.AIR, Vec3(x=0, y=2, z=1)),
                (Item.GREEN_CONCRETE, Vec3(x=0, y=2, z=2)),
                (Item.AIR, Vec3(x=0, y=1, z=0)),
                (Item.AIR, Vec3(x=0, y=1, z=1)),
                (Item.AIR, Vec3(x=0, y=1, z=2)),
                (Item.BLUE_CONCRETE, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=0, y=0, z=1)),
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=0, z=2)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=0, y=2, z=-2)),
                (Item.AIR, Vec3(x=0, y=2, z=-1)),
                (Item.GREEN_CONCRETE, Vec3(x=0, y=2, z=0)),
                (Item.AIR, Vec3(x=0, y=1, z=-2)),
                (Item.AIR, Vec3(x=0, y=1, z=-1)),
                (Item.AIR, Vec3(x=0, y=1, z=0)),
                (Item.BLUE_CONCRETE, Vec3(x=0, y=0, z=-2)),
                (Item.AIR, Vec3(x=0, y=0, z=-1)),
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=0, z=0)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=0, y=1, z=-1)),
                (Item.AIR, Vec3(x=0, y=1, z=0)),
                (Item.GREEN_CONCRETE, Vec3(x=0, y=1, z=1)),
                (Item.AIR, Vec3(x=0, y=0, z=-1)),
                (Item.AIR, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=0, y=0, z=1)),
                (Item.BLUE_CONCRETE, Vec3(x=0, y=-1, z=-1)),
                (Item.AIR, Vec3(x=0, y=-1, z=0)),
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=-1, z=1)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=1, y=0, z=0)),
                (Item.GREEN_CONCRETE, Vec3(x=2, y=0, z=0)),
                (Item.AIR, Vec3(x=0, y=0, z=-1)),
                (Item.AIR, Vec3(x=1, y=0, z=-1)),
                (Item.AIR, Vec3(x=2, y=0, z=-1)),
                (Item.BLUE_CONCRETE, Vec3(x=0, y=0, z=-2)),
                (Item.AIR, Vec3(x=1, y=0, z=-2)),
                (Item.YELLOW_CONCRETE, Vec3(x=2, y=0, z=-2)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=-2, y=0, z=0)),
                (Item.AIR, Vec3(x=-1, y=0, z=0)),
                (Item.GREEN_CONCRETE, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=-2, y=0, z=-1)),
                (Item.AIR, Vec3(x=-1, y=0, z=-1)),
                (Item.AIR, Vec3(x=0, y=0, z=-1)),
                (Item.BLUE_CONCRETE, Vec3(x=-2, y=0, z=-2)),
                (Item.AIR, Vec3(x=-1, y=0, z=-2)),
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=0, z=-2)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=0, y=0, z=2)),
                (Item.AIR, Vec3(x=1, y=0, z=2)),
                (Item.GREEN_CONCRETE, Vec3(x=2, y=0, z=2)),
                (Item.AIR, Vec3(x=0, y=0, z=1)),
                (Item.AIR, Vec3(x=1, y=0, z=1)),
                (Item.AIR, Vec3(x=2, y=0, z=1)),
                (Item.BLUE_CONCRETE, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=1, y=0, z=0)),
                (Item.YELLOW_CONCRETE, Vec3(x=2, y=0, z=0)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=-2, y=0, z=2)),
                (Item.AIR, Vec3(x=-1, y=0, z=2)),
                (Item.GREEN_CONCRETE, Vec3(x=0, y=0, z=2)),
                (Item.AIR, Vec3(x=-2, y=0, z=1)),
                (Item.AIR, Vec3(x=-1, y=0, z=1)),
                (Item.AIR, Vec3(x=0, y=0, z=1)),
                (Item.BLUE_CONCRETE, Vec3(x=-2, y=0, z=0)),
                (Item.AIR, Vec3(x=-1, y=0, z=0)),
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=0, z=0)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=-1, y=0, z=1)),
                (Item.AIR, Vec3(x=0, y=0, z=1)),
                (Item.GREEN_CONCRETE, Vec3(x=1, y=0, z=1)),
                (Item.AIR, Vec3(x=-1, y=0, z=0)),
                (Item.AIR, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=1, y=0, z=0)),
                (Item.BLUE_CONCRETE, Vec3(x=-1, y=0, z=-1)),
                (Item.AIR, Vec3(x=0, y=0, z=-1)),
                (Item.YELLOW_CONCRETE, Vec3(x=1, y=0, z=-1)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=1, y=0, z=0)),
                (Item.GREEN_CONCRETE, Vec3(x=2, y=0, z=0)),
                (Item.AIR, Vec3(x=0, y=0, z=1)),
                (Item.AIR, Vec3(x=1, y=0, z=1)),
                (Item.AIR, Vec3(x=2, y=0, z=1)),
                (Item.BLUE_CONCRETE, Vec3(x=0, y=0, z=2)),
                (Item.AIR, Vec3(x=1, y=0, z=2)),
                (Item.YELLOW_CONCRETE, Vec3(x=2, y=0, z=2)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=-2, y=0, z=0)),
                (Item.AIR, Vec3(x=-1, y=0, z=0)),
                (Item.GREEN_CONCRETE, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=-2, y=0, z=1)),
                (Item.AIR, Vec3(x=-1, y=0, z=1)),
                (Item.AIR, Vec3(x=0, y=0, z=1)),
                (Item.BLUE_CONCRETE, Vec3(x=-2, y=0, z=2)),
                (Item.AIR, Vec3(x=-1, y=0, z=2)),
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=0, z=2)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=0, y=0, z=-2)),
                (Item.AIR, Vec3(x=1, y=0, z=-2)),
                (Item.GREEN_CONCRETE, Vec3(x=2, y=0, z=-2)),
                (Item.AIR, Vec3(x=0, y=0, z=-1)),
                (Item.AIR, Vec3(x=1, y=0, z=-1)),
                (Item.AIR, Vec3(x=2, y=0, z=-1)),
                (Item.BLUE_CONCRETE, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=1, y=0, z=0)),
                (Item.YELLOW_CONCRETE, Vec3(x=2, y=0, z=0)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=-2, y=0, z=-2)),
                (Item.AIR, Vec3(x=-1, y=0, z=-2)),
                (Item.GREEN_CONCRETE, Vec3(x=0, y=0, z=-2)),
                (Item.AIR, Vec3(x=-2, y=0, z=-1)),
                (Item.AIR, Vec3(x=-1, y=0, z=-1)),
                (Item.AIR, Vec3(x=0, y=0, z=-1)),
                (Item.BLUE_CONCRETE, Vec3(x=-2, y=0, z=0)),
                (Item.AIR, Vec3(x=-1, y=0, z=0)),
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=0, z=0)),

            ],
            [
                (Item.RED_CONCRETE, Vec3(x=-1, y=0, z=-1)),
                (Item.AIR, Vec3(x=0, y=0, z=-1)),
                (Item.GREEN_CONCRETE, Vec3(x=1, y=0, z=-1)),
                (Item.AIR, Vec3(x=-1, y=0, z=0)),
                (Item.AIR, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=1, y=0, z=0)),
                (Item.BLUE_CONCRETE, Vec3(x=-1, y=0, z=1)),
                (Item.AIR, Vec3(x=0, y=0, z=1)),
                (Item.YELLOW_CONCRETE, Vec3(x=1, y=0, z=1)),

            ],
        ]

    def test_offsets(self):
        """Tests multiple offsets."""
        for index, (direction, anchor) in enumerate(product(
                self.directions, self.anchors)):
            self.assertEqual(
                list(offsets(self.valid_profile, direction, anchor)),
                self.results[index])


class TestValidate(TestCase):
    """Test the validate() function."""

    def setUp(self):
        """Sets example profiles."""
        self.valid_profile = [
            [Item.RED_CONCRETE, Item.AIR, Item.GREEN_CONCRETE],
            [Item.AIR, Item.AIR, Item.AIR],
            [Item.BLUE_CONCRETE, Item.AIR, Item.YELLOW_CONCRETE],
        ]
        self.invalid_profile1 = [
            [Item.RED_CONCRETE, Item.AIR, Item.GREEN_CONCRETE],
            [Item.AIR, Item.AIR],
            [Item.BLUE_CONCRETE, Item.AIR, Item.YELLOW_CONCRETE],
        ]
        self.invalid_profile2 = [
            [],
            [Item.AIR, Item.AIR, Item.AIR],
            [Item.BLUE_CONCRETE, Item.AIR, Item.YELLOW_CONCRETE],
        ]
        # self.invalid_profile0  = [Item.AIR, "wheelbarrow"]
        self.valid_cuboid = [self.valid_profile, self.valid_profile]
        self.invalid_cuboid1 = [self.invalid_profile1, self.invalid_profile1]
        self.valid_row = [Item.RED_CONCRETE, Item.AIR, Item.GREEN_CONCRETE]
        self.invalid_row1 = [Item.RED_CONCRETE, self.valid_profile]

    def test_validate(self):
        """Tests the validation of the profiles."""

        # TODO is there a quick way to verify that all elements are type Item?
        # self.assertEqual(validate(self.invalid_profile0), 0)

        self.assertEqual(validate(self.invalid_profile1), 0)
        self.assertEqual(validate(self.invalid_profile2), 0)
        self.assertEqual(validate(self.invalid_cuboid1), 0)

        self.assertEqual(validate(self.valid_profile), 2)

        self.assertEqual(validate(self.valid_cuboid), 3)
        self.assertEqual(validate(self.invalid_cuboid1), 0)

        self.assertEqual(validate(self.valid_row), 1)
        self.assertEqual(validate(self.invalid_row1), 0)


class TestDirection(TestCase):
    """Test Cardinal Direction Functions"""

    def test_y_rotate(self):
        d = Direction.SOUTH

        d = y_rotate(d)
        self.assertEqual(d, Direction.WEST)
        d = y_rotate(d)
        self.assertEqual(d, Direction.NORTH)
        d = y_rotate(d)
        self.assertEqual(d, Direction.EAST)
        d = y_rotate(d)
        self.assertEqual(d, Direction.SOUTH)
        d = y_rotate(d)
        self.assertEqual(d, Direction.WEST)

        d = y_rotate(d, False)
        self.assertEqual(d, Direction.SOUTH)
        d = y_rotate(d, False)
        self.assertEqual(d, Direction.EAST)
        d = y_rotate(d, False)
        self.assertEqual(d, Direction.NORTH)
        d = y_rotate(d, False)
        self.assertEqual(d, Direction.WEST)
        d = y_rotate(d, False)
        self.assertEqual(d, Direction.SOUTH)

    def test_facing(self):
        p1 = Vec3(100, 0, 100)

        p2s = [
            Vec3(100, 0, 100),
            Vec3(205, 0, 100),
            Vec3(-150, 0, 120),
            Vec3(106, 0, -105),
            Vec3(199, 0, 200),
            Vec3(100, 0, 101),
        ]
        dirs = [
            Direction.EAST,
            Direction.EAST,
            Direction.WEST,
            Direction.NORTH,
            Direction.SOUTH,
            Direction.SOUTH,
        ]

        for p2, direction in zip(p2s, dirs):
            assert Direction.facing(p1, p2) == direction
