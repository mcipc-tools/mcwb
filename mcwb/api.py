"""Exposed API functions."""

import math
from time import sleep
from typing import List, Optional

from mcipc.rcon.client import Client
from mcipc.rcon.enumerations import FillMode, Item

from mcwb.functions import get_direction, normalize, offsets, validate
from mcwb.types import Anchor, Profile, Vec3

__all__ = ["mktunnel"]


def mktunnel(
    client: Client,
    profile: Profile,
    start: Vec3,
    *,
    end: Vec3 = None,
    direction: Vec3 = None,
    length: int = 1,
    anchor: Anchor = Anchor.BOTTOM_RIGHT,
    default: Item = Item.AIR,
    mode: FillMode = None,
    filter: str = None,
):
    """Creates a tunnel with the given profile."""

    start = Vec3(*start)  # Ensure Vec3 object.

    if validate(profile) != 2:
        raise ValueError("Invalid matrix.")

    if end is None:
        end = start + direction * length
    else:
        end = Vec3(*end)  # Ensure Vec3 object.

    calculated_direction = get_direction(start, end)
    profile = list(normalize(profile, default=default))

    for block, offset in offsets(profile, calculated_direction, anchor):
        client.fill(start + offset, end + offset, block, mode=mode, filter=filter)


def polygon(diameter: int, sides: int, offset: Optional[float] = None):
    """
    Creates a polygon with the given diameter and number of sides.
    """

    corners: List[Vec3] = []

    if sides < 3:
        raise ValueError("Number of sides must be at least 3.")

    radius = diameter // 2
    angle = 2 * math.pi / sides
    offset = angle / 2 if offset is None else offset
    for i in range(sides):
        x = round(radius * math.cos(i * angle + offset))
        z = round(radius * math.sin(i * angle + offset))
        corners.append(Vec3(x, 0, z))

    return corners


def poly(
    client: Client, center: Vec3, sides=4, dia=15, item: Item = Item.AIR, offset=None
):
    corners = polygon(diameter=dia, sides=sides, offset=offset)
    for i in range(len(corners)):
        make_line_xz(
            client, center + corners[i], center + corners[(i + 1) % sides], item
        )
        sleep(1)


def make_line_xz(
    client: Client, start: Vec3, end: Vec3, item: Item = Item.AIR, overlap: int = 0
):
    """
    Creates a line of blocks from start to end.

    The line is at the height of the start block and has constant height.
    """

    def d_range(n1, n2):
        if n1 > n2:
            return -1, range(n1, n2 - 1, -1), n1 - n2
        else:
            return 1, range(n1, n2 + 1), n2 - n1

    start = Vec3(*start).with_ints()  # Ensure Vec3 object.
    end = Vec3(*end).with_ints()  # Ensure Vec3 object.

    dir_x, range_x, delta_x = d_range(start.x, end.x)
    dir_z, range_z, delta_z = d_range(start.z, end.z)

    steps = int(max(delta_x, delta_z))

    z_step = delta_z / steps * dir_z
    x_step = delta_x / steps * dir_x

    x, y, z = start.x, start.y, start.z
    next_x, next_z = x, z

    client.setblock(Vec3(x, y, z), item)

    for i in range(steps + 1):
        if (x, z) != (round(next_x), round(next_z)):
            x, z = round(next_x), round(next_z)
            client.setblock(Vec3(x, y, z), item)
        next_z += z_step
        next_x += x_step
