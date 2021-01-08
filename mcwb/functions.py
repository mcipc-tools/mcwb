"""Helper functions."""

from typing import Iterator

from mcipc.rcon.enumerations import Item

from mcwb.types import Anchor, Direction, Number, Offsets, Profile, Row, Vec3


__all__ = ['get_direction', 'normalize', 'offsets', 'validate']


def _get_offset(direction: Vec3, x_start: Number, y_start: Number,
                delta_y: Number, delta_xz: Number) -> Vec3:
    """Returns the offset for a given direction."""

    if direction.north:
        return Vec3(-x_start + delta_xz, y_start - delta_y, 0)

    if direction.south:
        return Vec3(x_start - delta_xz, y_start - delta_y, 0)

    if direction.east:
        return Vec3(0, y_start - delta_y, -x_start + delta_xz)

    if direction.west:
        return Vec3(0, y_start - delta_y, x_start - delta_xz)

    if direction.up:
        return Vec3(-x_start + delta_xz, 0, y_start - delta_y)

    if direction.down:
        return Vec3(-x_start + delta_xz, 0, -y_start + delta_y)

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

    for delta_y, row in enumerate(profile):
        for delta_xz, block in enumerate(row):
            vec3 = _get_offset(direction, x_start, y_start, delta_y, delta_xz)
            yield (block, vec3)


def validate(profile: Profile) -> bool:
    """Validates a profile to have rows with equal length."""

    rows = iter(profile)

    try:
        first = len(next(rows))
    except StopIteration:
        return True

    return all(len(row) == first for row in rows)
