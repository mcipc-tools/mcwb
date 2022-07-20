"""Exposed API functions."""

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
):
    """
    Place a polygon in the world

    TODO - lots of arguments here - maybe should use classes for the API instead?
    Tunnel, Polygon ...
    """

    profile = poly_profile(sides=sides, diameter=diameter, item=item, offset=offset)
    make_tunnel(
        client,
        profile,
        center,
        length=height,
        direction=direction,
        mode=FillMode.REPLACE,
    )
