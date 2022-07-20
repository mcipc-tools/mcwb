"""Builder data types."""

from __future__ import annotations

from enum import Enum
from math import atan2, ceil, floor, pi, sqrt
from typing import Iterator, List, NamedTuple, Tuple, Union

import numpy as np
from mcipc.rcon.enumerations import Item

__all__ = [
    "Anchor",
    "Anchor3",
    "Cuboid",
    "Direction",
    "Items",
    "Number",
    "Offset",
    "Offsets",
    "Profile",
    "Row",
    "Vec3",
]


Number = Union[float, int]


class Anchor(Enum):
    """Anchor point for tunnels."""

    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"
    MIDDLE = CENTER = CENTRE = "middle"


class Anchor3(Enum):
    """Anchor point for cuboids."""

    MIDDLE = CENTER = CENTRE = "middle"
    BOTTOM_MIDDLE = BOTTOM_CENTER = BOTTOM_CENTRE = "bottom_middle"
    TOP_MIDDLE = TOP_CENTER = TOP_CENTRE = "top_middle"

    BOTTOM_SW = "bottom_sw"
    BOTTOM_NW = "bottom_nw"
    BOTTOM_NE = "bottom_ne"
    BOTTOM_SE = "bottom_se"

    TOP_SW = "top_sw"
    TOP_NW = "top_nw"
    TOP_NE = "top_ne"
    TOP_SE = "top_se"

    def __str__(self):
        return f"{self.value}"


class Anchor3Face:
    """Groupings of Anchor3 based on which face of the volume they inhabit"""

    TOP = {
        Anchor3.TOP_SW,
        Anchor3.TOP_NW,
        Anchor3.TOP_NE,
        Anchor3.TOP_SE,
        Anchor3.TOP_MIDDLE,
    }
    BOTTOM = {
        Anchor3.BOTTOM_SW,
        Anchor3.BOTTOM_NW,
        Anchor3.BOTTOM_NE,
        Anchor3.BOTTOM_SE,
    }
    # middle of top or bottom face
    MIDDLE_FACE = CENTER_FACE = CENTRE_FACE = {
        Anchor3.BOTTOM_MIDDLE,
        Anchor3.TOP_MIDDLE,
    }
    NORTH = {Anchor3.TOP_NW, Anchor3.TOP_NE, Anchor3.BOTTOM_NW, Anchor3.BOTTOM_NE}
    SOUTH = {Anchor3.TOP_SW, Anchor3.TOP_SE, Anchor3.BOTTOM_SW, Anchor3.BOTTOM_SE}
    EAST = {Anchor3.TOP_NE, Anchor3.TOP_SE, Anchor3.BOTTOM_NE, Anchor3.BOTTOM_SE}
    WEST = {Anchor3.TOP_SW, Anchor3.TOP_NW, Anchor3.BOTTOM_SW, Anchor3.BOTTOM_NW}


class Vec3(NamedTuple):
    """A 3D vector."""

    x: Number = 0
    y: Number = 0
    z: Number = 0

    def __abs__(self):
        return type(self)(abs(self.x), abs(self.y), abs(self.z))

    def __add__(self, other):
        if isinstance(other, Vec3):
            return type(self)(self.x + other.x, self.y + other.y, self.z + other.z)

        return type(self)(self.x + other, self.y + other, self.z + other)

    def __ceil__(self):
        return type(self)(ceil(self.x), ceil(self.y), ceil(self.z))

    def __floor__(self):
        return type(self)(floor(self.x), floor(self.y), floor(self.z))

    def __floordiv__(self, other):
        if isinstance(other, Vec3):
            return type(self)(self.x // other.x, self.y // other.y, self.z // other.z)

        return type(self)(self.x // other, self.y // other, self.z // other)

    def __getitem__(self, index_or_key: Union[int, str]):
        """Returns an item by index or key."""
        if index_or_key in self.keys():
            return getattr(self, index_or_key)

        # Explicitely call to tuple, since
        # super() does not work in NamedTuples.
        return tuple.__getitem__(self, index_or_key)

    def __mul__(self, other):
        if isinstance(other, Vec3):
            return self.__matmul__(other)

        return type(self)(self.x * other, self.y * other, self.z * other)

    def __matmul__(self, other: Vec3):
        return type(self)(self.x * other.x, self.y * other.y, self.z * other.z)

    def __neg__(self):
        return type(self)(-self.x, -self.y, -self.z)

    def __pos__(self):
        return self  # No operation necessary.

    def __round__(self, ndigits: int = 0):
        return type(self)(
            round(self.x, ndigits), round(self.y, ndigits), round(self.z, ndigits)
        )

    def __sub__(self, other):
        if isinstance(other, Vec3):
            return type(self)(self.x - other.x, self.y - other.y, self.z - other.z)

        return type(self)(self.x - other, self.y - other, self.z - other)

    def __truediv__(self, other):
        if isinstance(other, Vec3):
            return type(self)(self.x / other.x, self.y / other.y, self.z / other.z)

        return type(self)(self.x / other, self.y / other, self.z / other)

    def keys(self):
        """Returns the keys."""
        return self._fields

    def with_ints(self):
        """Coerce all coordinates to int."""
        # floor is consistent with minecraft's handling of negative coords
        return type(self)(floor(self.x), floor(self.y), floor(self.z))

    @property
    def volume(self):
        """Returns the volume of the space described by (0,0,0) -> self."""
        return self.dx * self.dy * self.dz

    @property
    def is_direction(self):
        """Determines whether this is a direction vector."""
        return sum(coord != 0 for coord in self) == 1

    @property
    def dx(self):  # pylint: disable=C0103
        """Returns the absolute x value."""
        return abs(self.x)

    @property
    def dy(self):  # pylint: disable=C0103
        """Returns the absolute y value."""
        return abs(self.y)

    @property
    def dz(self):  # pylint: disable=C0103
        """Returns the absolute z value."""
        return abs(self.z)

    @property
    def length(self):
        """Returns the length of the spatial diagonal."""
        return sqrt(pow(self.dx, 2) + pow(self.dy, 2) + pow(self.dz, 2))

    @property
    def west(self):
        """Checks whether the vector points west."""
        return self.x < 0

    @property
    def east(self):
        """Checks whether the vector points east."""
        return self.x > 0

    @property
    def north(self):
        """Checks whether the vector points north."""
        return self.z < 0

    @property
    def south(self):
        """Checks whether the vector points south."""
        return self.z > 0

    @property
    def down(self):
        """Checks whether the vector points down."""
        return self.y < 0

    @property
    def up(self):  # pylint: disable=C0103
        """Checks whether the vector points up."""
        return self.y > 0


class Direction:
    """Available directions."""

    # the cardinals match the order of entity data 'Rotation'
    SOUTH = Vec3(0, 0, +1)
    WEST = Vec3(-1, 0, 0)
    NORTH = Vec3(0, 0, -1)
    EAST = Vec3(+1, 0, 0)
    UP = Vec3(0, +1, 0)
    DOWN = Vec3(0, -1, 0)

    # Direction.name() gets an NBT 'facing' field value from a Direction vector
    _names = ["south", "west", "north", "east", "up", "down"]

    # An indexed lookup like an Enum, useful for quadrant math
    @classmethod
    @property
    def values(cls) -> List[Vec3]:
        return [cls.SOUTH, cls.WEST, cls.NORTH, cls.EAST, cls.UP, cls.DOWN]

    @classmethod
    @property
    def all(cls) -> List[Vec3]:
        return [val for val in vars(cls).values() if isinstance(val, Vec3)]

    @classmethod
    @property
    def cardinals(cls) -> List[Vec3]:
        return list(cls.all[:-2])

    @classmethod
    def name(cls, direction: Vec3) -> str:
        idx = cls.all.index(direction)
        return cls._names[idx]

    @classmethod
    def facing(cls, p1: Vec3, p2: Vec3) -> Vec3:
        """
        return a vector representing the cardinal direction when facing point p2
        from the perspective of point p1
        """
        angle = atan2(p2.z - p1.z, p2.x - p1.x)
        angle += pi * 5 / 4
        angle /= pi / 2
        quarter = int(angle)
        quarter = (quarter + 1) % 4
        return cls.values[quarter]


class Planes3d(Enum):
    """
    Represents all 3 planes in a 3d space as a pair of
    dimension indices as used in np.array: 0=X 1=Y 2=Z
    """

    XY = (0, 1)
    XZ = (0, 2)
    YZ = (1, 2)


Row = Union[List[Item], np.ndarray]
Profile = Union[List[Row], np.ndarray]
Cuboid = Union[List[Profile], np.ndarray]

Items = Union[Cuboid, Profile, Row]

Offset = Tuple[Item, Vec3]
Offsets = Iterator[Offset]
