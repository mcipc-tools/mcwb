"""Exposed API functions."""

import math
from typing import List

from mcipc.rcon.client import Client
from mcipc.rcon.enumerations import FillMode, Item

from mcwb.functions import get_direction, normalize, offsets, validate
from mcwb.types import Anchor, Profile, Vec3

__all__ = ['mktunnel']


def mktunnel(client: Client, profile: Profile, start: Vec3, *,
             end: Vec3 = None, direction: Vec3 = None, length: int = 1,
             anchor: Anchor = Anchor.BOTTOM_RIGHT, default: Item = Item.AIR,
             mode: FillMode = None, filter: str = None):
    """Creates a tunnel with the given profile."""

    start = Vec3(*start)    # Ensure Vec3 object.

    if validate(profile) != 2:
        raise ValueError('Invalid matrix.')

    if end is None:
        end = start + direction * length
    else:
        end = Vec3(*end)    # Ensure Vec3 object.

    calculated_direction = get_direction(start, end)
    profile = list(normalize(profile, default=default))

    for block, offset in offsets(profile, calculated_direction, anchor):
        client.fill(
            start + offset, end + offset, block, mode=mode, filter=filter
        )


def polygon(diameter: int, sides: int):
    """
    Creates a polygon with the given diameter and number of sides.
    """

    corners: List[Vec3] = []

    if sides < 3:
        raise ValueError('Number of sides must be at least 3.')

    radius = diameter // 2
    angle = 2 * math.pi / sides
    offset = angle / 2
    for i in range(sides):
        x = radius * math.cos(i * angle + offset)
        z = radius * math.sin(i * angle + offset)
        corners.append(Vec3(x, 0, z))

    return corners


def square(client: Client, center: Vec3, item: Item = Item.AIR):
    corners = polygon(diameter=12, sides=4)
    for i in range(len(corners)):
        make_line_xz(client, center + corners[i], center + corners[(i+1) % 4], item)


def make_line_xz(
    client: Client, start: Vec3, end: Vec3, item: Item = Item.AIR,
    overlap: int = 0
):
    """
    Creates a line of blocks from start to end.

    The line is at the height of the start block and has constant height.
    """

    start = Vec3(*start).with_ints()    # Ensure Vec3 object.
    end = Vec3(*end).with_ints()        # Ensure Vec3 object.
    x_step = 1 if start.x <= end.x else -1

    dx = end.x - start.x
    dz = end.z - start.z
    z_step = dz if dx == 0 else dz / abs(start.x - end.x)
    y, z = start.y, start.z

    for x in range(int(start.x), int(end.x + 1), x_step):
        next_z = z + z_step
        min_z, max_z = min(next_z, z), max(next_z, z)
        for tmp_z in range(round(min_z), round(max_z+1)):
            client.setblock(Vec3(x, y, tmp_z), item)
        z = next_z
