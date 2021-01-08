"""Tests the functions module."""

from functools import partial
from itertools import product
from unittest import TestCase

from mcipc.rcon.enumerations import Item

from mcwb.functions import get_direction, normalize, offsets, validate
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
        self.directions = Direction
        self.anchors = Anchor
        self.results = [
            [
                (Item.RED_CONCRETE, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=0, y=0, z=1)),
                (Item.GREEN_CONCRETE, Vec3(x=0, y=0, z=2)),
                (Item.AIR, Vec3(x=0, y=-1, z=0)),
                (Item.AIR, Vec3(x=0, y=-1, z=1)),
                (Item.AIR, Vec3(x=0, y=-1, z=2)),
                (Item.BLUE_CONCRETE, Vec3(x=0, y=-2, z=0)),
                (Item.AIR, Vec3(x=0, y=-2, z=1)),
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=-2, z=2))
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
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=-2, z=0))
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
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=0, z=2))
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
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=0, z=0))
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
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=-1, z=1))
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
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=-2, z=-2))
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
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=-2, z=0))
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
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=0, z=-2))
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
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=0, z=0))
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
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=-1, z=-1))
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
                (Item.YELLOW_CONCRETE, Vec3(x=2, y=0, z=-2))
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
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=0, z=-2))
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
                (Item.YELLOW_CONCRETE, Vec3(x=2, y=0, z=0))
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
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=0, z=0))
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
                (Item.YELLOW_CONCRETE, Vec3(x=1, y=0, z=-1))
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
                (Item.YELLOW_CONCRETE, Vec3(x=2, y=0, z=2))
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
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=0, z=2))
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
                (Item.YELLOW_CONCRETE, Vec3(x=2, y=0, z=0))
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
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=0, z=0))
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
                (Item.YELLOW_CONCRETE, Vec3(x=1, y=0, z=1))
            ],
            [
                (Item.RED_CONCRETE, Vec3(x=0, y=0, z=0)),
                (Item.AIR, Vec3(x=-1, y=0, z=0)),
                (Item.GREEN_CONCRETE, Vec3(x=-2, y=0, z=0)),
                (Item.AIR, Vec3(x=0, y=-1, z=0)),
                (Item.AIR, Vec3(x=-1, y=-1, z=0)),
                (Item.AIR, Vec3(x=-2, y=-1, z=0)),
                (Item.BLUE_CONCRETE, Vec3(x=0, y=-2, z=0)),
                (Item.AIR, Vec3(x=-1, y=-2, z=0)),
                (Item.YELLOW_CONCRETE, Vec3(x=-2, y=-2, z=0))
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
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=-2, z=0))
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
                (Item.YELLOW_CONCRETE, Vec3(x=-2, y=0, z=0))
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
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=0, z=0))
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
                (Item.YELLOW_CONCRETE, Vec3(x=-1, y=-1, z=0))
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
                (Item.YELLOW_CONCRETE, Vec3(x=2, y=-2, z=0))
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
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=-2, z=0))
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
                (Item.YELLOW_CONCRETE, Vec3(x=2, y=0, z=0))
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
                (Item.YELLOW_CONCRETE, Vec3(x=0, y=0, z=0))
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
                (Item.YELLOW_CONCRETE, Vec3(x=1, y=-1, z=0))
            ]
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

    def test_validate(self):
        """Tests the validation of the profiles."""
        self.assertTrue(validate(self.valid_profile))
        self.assertFalse(validate(self.invalid_profile1))
        self.assertFalse(validate(self.invalid_profile2))
