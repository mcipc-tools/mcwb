"""Representation of 3D spaces."""

from __future__ import annotations

from mcipc.rcon.enumerations import Item
from mcipc.rcon.je import Client

from mcwb import Anchor, Anchor3, Anchor3Face, Direction, Vec3, make_tunnel

__all__ = ["Volume"]

MAX_MINECRAFT_FILL_COMMAND = 32768


class Volume:
    """
    Describes a 3d space in a Minecraft world using one of:
      - a starting point and size. The starting point can be any vertex or
        the middle of one of the horizontal faces, using the cardinal
        terminology defined in Anchor3.
      - two opposite corners
    """

    def __init__(self):
        self.start = Vec3(0, 0, 0)  # lowest coordinate in the volume
        self.end = Vec3(0, 0, 0)  # highest coordinate in the volume
        self.size = Vec3(0, 0, 0)  # the dimensions of the volume

        # NOTE: position == start when self.anchor == Anchor3.BOTTOM_NW
        self.anchor = Anchor3.BOTTOM_NW  # the anchor point for position
        self.position = Vec3(0, 0, 0)  # the positon of the anchor point

    @classmethod
    def from_anchor(cls, position: Vec3, size: Vec3, anchor: Anchor3) -> Volume:
        """a factory function to create a Volume using anchor and size"""
        volume = Volume()
        volume.position = Vec3(*position)
        volume.size = Vec3(*size)
        volume.anchor = anchor

        offset = Vec3(0, 0, 0)
        if anchor in Anchor3Face.TOP:
            offset += Vec3(0, 1 - size.y, 0)
        if anchor in Anchor3Face.SOUTH:
            offset += Vec3(0, 0, 1 - size.z)
        if anchor in Anchor3Face.EAST:
            offset += Vec3(1 - size.x, 0, 0)
        if anchor in Anchor3Face.MIDDLE_FACE:  # middle of top or bottom
            offset -= Vec3(int(size.x / 2), 0, int(size.z / 2))
        elif anchor is Anchor3.MIDDLE:
            offset = Vec3(-1, -1, -1) * (size / 2).with_ints()

        volume.start = position + offset
        volume.end = volume.start + (volume.size - 1)

        return volume

    @classmethod
    def from_corners(cls, start: Vec3, end: Vec3) -> Volume:
        """a factory function to define Volume using opposite corners"""
        volume = Volume()
        start = Vec3(*start).with_ints()
        end = Vec3(*end).with_ints()

        # normalize start and end so all start coords are minima
        volume.position = volume.start = Vec3(
            min(start.x, end.x), min(start.y, end.y), min(start.z, end.z)
        )
        volume.end = Vec3(max(start.x, end.x), max(start.y, end.y), max(start.z, end.z))
        volume.size = (volume.end - volume.start) + 1

        return volume

    def inside(
        self, position: Vec3, xtol: int = 0, ytol: int = 0, ztol: int = 0
    ) -> bool:
        """determine if position is within the Volume"""
        return (
            self.start.x - xtol <= position.x <= self.end.x + xtol
            and self.start.y - ytol <= position.y <= self.end.y + ytol
            and self.start.z - ztol <= position.z <= self.end.z + ztol
        )

    def move(self, distance: Vec3) -> None:
        """move the volume's location in space by distance"""
        self.start += distance
        self.end += distance
        self.position += distance

    def move_to(self, position: Vec3) -> None:
        """move the volume's location in space to position"""
        self.start += position - self.position
        self.end += position - self.position
        self.position = position

    def fill(self, client: Client, block: Item = Item.AIR):
        """Fill the Volume with a single block type, supports large volumes"""
        if self.size.volume < MAX_MINECRAFT_FILL_COMMAND:
            client.fill(self.start, self.end, block.value)
        else:
            profile = [[block] * int(self.size.x)] * int(self.size.y)
            make_tunnel(
                client,
                profile,
                self.start,
                direction=Direction.UP,
                anchor=Anchor.BOTTOM_LEFT,
                length=int(self.size.dz),
            )

    def walls(
        self,
        client: Client,
        block: Item,
        *,
        thickness: int = 1,
        top: bool = True,
        bottom: bool = True,
        north: bool = True,
        south: bool = True,
        east: bool = True,
        west: bool = True,
    ) -> None:
        """renders walls at the faces of the volume"""
        t = thickness - 1
        b = block.value
        if north:
            client.fill(self.start, Vec3(self.end.x, self.end.y, self.start.z + t), b)
        if south:
            client.fill(self.end, Vec3(self.start.x, self.start.y, self.end.z - t), b)
        if west:
            client.fill(self.start, Vec3(self.start.x + t, self.end.y, self.end.z), b)
        if east:
            client.fill(self.end, Vec3(self.end.x - t, self.start.y, self.start.z), b)
        if top:
            client.fill(self.end, Vec3(self.start.x, self.end.y - t, self.start.z), b)
        if bottom:
            client.fill(self.start, Vec3(self.end.x, self.start.y + 1, self.end.z), b)
