"""Helper functions."""

from typing import Iterator, Union

import numpy as np
from mcipc.rcon.enumerations import Item

from mcwb.types import Anchor, Direction, Items, Number, Offsets, Profile, Row, Vec3

__all__ = ["get_direction", "normalize", "offsets", "validate"]


def _get_offset(
    direction: Vec3, x_start: Number, y_start: Number, delta_y: Number, delta_xz: Number
) -> Vec3:
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

    raise ValueError("Cannot determine offset.")


def get_direction(start: Vec3, end: Vec3) -> Vec3:
    """Checks whether the vetors form a line
    and returns the direction vector.
    """

    if sum(coord1 != coord2 for coord1, coord2 in zip(start, end)) != 1:
        raise ValueError("Not one direction given.")

    return end - start


def y_rotate(direction: Vec3, clockwise: bool = True) -> Vec3:
    """rotate a cardinal direction about the y axis"""

    current = Direction.cardinals.index(direction)
    rotated = current + (1 if clockwise else -1)
    return Direction.cardinals[rotated % len(Direction.cardinals)]


def normalize(
    profile: Union[Profile, np.ndarray], default: Item = Item.AIR
) -> Iterator[Row]:
    """Normalizes a profile."""

    for row in profile:
        yield [default if block is None else Item(block) for block in row]


def offsets(profile: Profile, direction: Vec3, anchor: Anchor) -> Offsets:
    """Yields block offsets dependent on the given direction."""

    height = len(profile)
    width = len(profile[0])
    x_start = y_start = 0

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


def validate(items: Items):
    """
    Validates a row, profile or cuboid, ensuring consistent dimensions
    """
    ragged = False

    # np ragged array is deprecated but only supplys a warning currently
    with np.warnings.catch_warnings(record=True) as warning:
        np.warnings.simplefilter("always")
        narray = np.array(items)
        if warning and "ragged nested" in str(warning[-1].message):
            ragged = True

    return int(narray.ndim) if narray.dtype == Item and not ragged else 0


def shift(arr: np.ndarray, vec: Vec3, fill: Item = Item.AIR) -> np.ndarray:
    """shift a 3d array of Item by vec, discarding the cells that are
    shifted out and filling the new space with Item fill
    """

    # this is the fastest approach in python, see 1d Benchmark at
    # https://stackoverflow.com/questions/30399534/shift-elements-in-a-numpy-array
    result: np.ndarray = np.array(np.full_like(arr, fill), dtype=Item)
    if vec.y > 0:
        result[:, : vec.y, :] = fill
        result[:, vec.y :, :] = arr[:, : -vec.y, :]
    elif vec.y < 0:
        result[:, vec.y :, :] = fill
        result[:, : vec.y, :] = arr[:, -vec.y :, :]
    if vec.x > 0:
        result[: vec.x, :, :] = fill
        result[vec.x :, :, :] = arr[: -vec.x, :, :]
    elif vec.x < 0:
        result[vec.x :, :, :] = fill
        result[: vec.x, :, :] = arr[-vec.x :, :, :]
    if vec.z > 0:
        result[:, :, : vec.z :] = fill
        result[:, :, vec.z :] = arr[:, :, : -vec.z]
    elif vec.z < 0:
        result[:, :, vec.z :] = fill
        result[:, :, : vec.z] = arr[:, :, -vec.z :]

    return result
