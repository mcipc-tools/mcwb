"""Exposed API functions."""

from mcipc.rcon.client import Client
from mcipc.rcon.enumerations import FillMode, Item

from mcwb.functions import get_direction
from mcwb.functions import offsets
from mcwb.functions import normalize
from mcwb.functions import validate
from mcwb.types import Anchor, Direction, Profile, Vec3


__all__ = ['mktunnel']


def mktunnel(client: Client, profile: Profile, start: Vec3, *,
             end: Vec3 = None, direction: Direction = None, length: int = 1,
             anchor: Anchor = Anchor.BOTTOM_RIGHT, default: Item = Item.AIR,
             mode: FillMode = None, filter: str = None):
    """Creates a tunnel with the given profile."""

    start = Vec3(*start)    # Ensure Vec3 object.

    if not validate(profile):
        raise ValueError('Invalid matrix.')

    if end is None:
        end = start + direction.value * length
    else:
        end = Vec3(*end)    # Ensure Vec3 object.

    calculated_direction = get_direction(start, end)
    profile = list(normalize(profile, default=default))

    for block, offset in offsets(profile, calculated_direction, anchor):
        client.fill(
            start + offset, end + offset, block, mode=mode, filter=filter
        )
