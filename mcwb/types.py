"""Builder data types."""

from __future__ import annotations
from enum import Enum
from math import ceil, floor, sqrt
from typing import Iterator, List, NamedTuple, Tuple, Union

from mcipc.rcon.enumerations import Item


__all__ = [
    'Anchor',
    'Direction',
    'Number',
    'Offset',
    'Offsets',
    'Profile',
    'Row',
    'Vec3'
]


Number = Union[float, int]


class Anchor(Enum):
    """Anchor point for tunnels."""

    TOP_LEFT = 'top_left'
    TOP_RIGHT = 'top_right'
    BOTTOM_LEFT = 'bottom_left'
    BOTTOM_RIGHT = 'bottom_right'
    MIDDLE = CENTER = CENTRE = 'middle'


class Vec3(NamedTuple):
    """A 3D vector."""

    x: Number = 0
    y: Number = 0
    z: Number = 0

    def __abs__(self):
        return type(self)(abs(self.x), abs(self.y), abs(self.z))

    def __add__(self, other):
        if isinstance(other, Vec3):
            return type(self)(self.x + other.x, self.y + other.y,
                              self.z + other.z)

        return type(self)(self.x + other, self.y + other, self.z + other)

    def __ceil__(self):
        return type(self)(ceil(self.x), ceil(self.y), ceil(self.z))

    def __floor__(self):
        return type(self)(floor(self.x), floor(self.y), floor(self.z))

    def __floordiv__(self, other):
        if isinstance(other, Vec3):
            return type(self)(self.x // other.x, self.y // other.y,
                              self.z // other.z)

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
        return self     # No operation necessary.

    def __round__(self, ndigits: int = 0):
        return type(self)(round(self.x, ndigits), round(self.y, ndigits),
                          round(self.z, ndigits))

    def __sub__(self, other):
        if isinstance(other, Vec3):
            return type(self)(self.x - other.x, self.y - other.y,
                              self.z - other.z)

        return type(self)(self.x - other, self.y - other, self.z - other)

    def __truediv__(self, other):
        if isinstance(other, Vec3):
            return type(self)(self.x / other.x, self.y / other.y,
                              self.z / other.z)

        return type(self)(self.x / other, self.y / other, self.z / other)

    def keys(self):
        """Returns the keys."""
        return self._fields

    def with_ints(self):
        """Coerce all coordinates to int."""
        return type(self)(int(self.x), int(self.y), int(self.z))

    @property
    def volume(self):
        """Returns the volume of the space described by (0,0,0) -> self."""
        return self.dx * self.dy * self.dz

    @property
    def is_direction(self):
        """Determines whether this is a direction vector."""
        return sum(coord != 0 for coord in self) == 1

    @property
    def dx(self):   # pylint: disable=C0103
        """Returns the absolute x value."""
        return abs(self.x)

    @property
    def dy(self):   # pylint: disable=C0103
        """Returns the absolute y value."""
        return abs(self.y)

    @property
    def dz(self):   # pylint: disable=C0103
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
    def up(self):   # pylint: disable=C0103
        """Checks whether the vector points up."""
        return self.y > 0


class Direction(Enum):
    """Available directions."""

    EAST = Vec3(+1, 0, 0)
    WEST = Vec3(-1, 0, 0)
    UP = Vec3(0, +1, 0)
    DOWN = Vec3(0, -1, 0)
    SOUTH = Vec3(0, 0, +1)
    NORTH = Vec3(0, 0, -1)


Row = List[Union[Item, None]]
Profile = List[Row]
Offset = Tuple[Item, Vec3]
Offsets = Iterator[Offset]
