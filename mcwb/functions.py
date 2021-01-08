"""Helper functions."""

from typing import Iterator

from mcipc.rcon.enumerations import Item

from mcwb.types import Anchor, Direction, Number, Offsets, Profile, Row, Vec3


__all__ = ['get_direction', 'normalize', 'offsets', 'validate']


def _get_offset(direction: Vec3, x_start: Number, y_start: Number,
                y: Number, xz: Number) -> Vec3:     # pylint: disable=C0103
    """Returns the offset for a given direction."""

    if direction.north:
        return Vec3(-x_start + xz, y_start - y, 0)

    if direction.south:
        return Vec3(x_start - xz, y_start - y, 0)

    if direction.east:
        return Vec3(0, y_start - y, -x_start + xz)

    if direction.west:
        return Vec3(0, y_start - y, x_start - xz)

    if direction.up:
        return Vec3(-x_start + xz, 0, y_start - y)

    if direction.down:
        return Vec3(-x_start + xz, 0, -y_start + y)

    raise ValueError('Cannot determine offset.')


def get_direction(start: Vec3, end: Vec3) -> Vec3:
    """Checks whether the vetors form a line
    and returns the direction vector.
    """

    if sum(coord1 != coord2 for coord1, coord2 in zip(start, end)) != 1:
        raise ValueError('Not one direction given.')

    return end - start


def normalize(profile: Profile, default: Item = Item.AIR) -> Iterator[Row]:
    """Normalizes a profile."""

    for row in profile:
        yield [default if block is None else Item(block) for block in row]


def offsets(profile: Profile, direction: Vec3, anchor: Anchor) -> Offsets:
    """Yields block offsets dependent on the given direction."""

    height = len(profile)
    width = len(profile[0])
    x_start = y_start = 0

    if isinstance(direction, Direction):
        direction = direction.value

    if anchor in {Anchor.BOTTOM_LEFT, Anchor.BOTTOM_RIGHT}:
        y_start = height - 1
    if anchor in {Anchor.TOP_RIGHT, Anchor.BOTTOM_RIGHT}:
        x_start = width - 1
    elif anchor == Anchor.MIDDLE:
        x_start = int(width / 2)
        y_start = int(height / 2)

    for y, row in enumerate(profile):  # pylint: disable=C0103
        for xz, block in enumerate(row):  # pylint: disable=C0103
            vec3 = _get_offset(direction, x_start, y_start, y, xz)
            yield (block, vec3)


def validate(profile: Profile) -> bool:
    """Sanitizes a matrix."""

    rows = iter(profile)

    try:
        first = len(next(rows))
    except StopIteration:
        return True

    return all(len(row) == first for row in rows)
