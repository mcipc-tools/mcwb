"""Exposed API functions."""

import re
from typing import Optional, Union

import numpy as np
from mcipc.rcon.client import Client
from mcipc.rcon.enumerations import FillMode, Item

from mcwb.functions import get_direction, normalize, offsets, validate
from mcwb.polygon import poly_profile
from mcwb.types import Anchor, Direction, Profile, Vec3

__all__ = ["make_tunnel"]


def make_tunnel(
    client: Client,
    profile: Union[Profile, np.ndarray],
    start: Vec3,
    *,
    end: Optional[Vec3] = None,
    direction: Vec3 = Direction.UP,
    length: int = 1,
    anchor: Anchor = Anchor.CENTER,
    default: Item = Item.AIR,
    mode: FillMode = FillMode.KEEP,
    filter: Optional[str] = None,
):
    """Creates a tunnel with the given profile."""

    start = Vec3(*start)  # Ensure Vec3 object.

    if validate(profile) != 2:
        raise ValueError("Invalid matrix.")

    if end is None:
        end = start + direction * (length - 1)
    else:
        end = Vec3(*end)  # Ensure Vec3 object.

    direction = direction or get_direction(start, end)
    profile = list(normalize(profile, default=default))

    for block, offset in offsets(profile, direction, anchor):
        client.fill(start + offset, end + offset, block, mode=mode, filter=filter)


def polygon(
    client: Client,
    center: Vec3,
    height: int,
    diameter: int,
    sides=4,
    direction=Direction.UP,
    item: Item = Item.STONE,
    offset=None,
    mode=FillMode.KEEP,
    fill_item: Item = Item.AIR,
):
    """
    Place a polygon in the world

    TODO - lots of arguments here - maybe should use classes for the API instead?
    Tunnel, Polygon ...
    """

    profile = poly_profile(
        sides=sides, diameter=diameter, item=item, offset=offset, fill_item=fill_item
    )
    make_tunnel(client, profile, center, length=height, direction=direction, mode=mode)


_bottom = -64  # the bottom of the world - only compatible with MC 1.19 upwards
_extract_item = re.compile(r".*minecraft\:(?:blocks\/)?(.+)$")


def get_block(client: Client, pos: Vec3):
    """Get the block at the given position."""

    # loot.spawn creates an entity - We choose to dump it into the void.
    # We choose the point right below pos to avoid any issues with
    # the block being in an chunk that is not loaded.
    dump = (pos.x, _bottom, pos.z)

    # currently the only way to test for a block is to use the loot spawn
    # command, this creates an entity that falls into the void
    output = client.loot.spawn(dump).mine(pos)
    match = _extract_item.search(output)
    if not match:
        raise ValueError(f"unexpected response from loot spawn: {output}")
    name = match.group(1)
    if name == "empty":
        name = "air"

    return Item(name)
