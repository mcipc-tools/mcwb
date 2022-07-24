"""
A mock client for testing functions that call the minecraft server.
This mocks a world of 100 blocks square with origin in the middle.
"""
from math import floor

import numpy as np
from mcipc.rcon.enumerations import FillMode, Item

from mcwb import Items, Vec3


class MockClient:
    def __init__(self, size=100):
        """create an empty mock world"""
        self.world = np.full((size, size, size), Item.AIR, dtype=Item)
        off = size // 2
        self.offset = Vec3(off, off, off)

    # the following are mock versions of the original Client Functions

    def setblock(self, position: Vec3, block: Item):
        """set the block at position in the world"""
        pos = position + self.offset
        self.world[pos.x, pos.y, pos.z] = block

    @property
    def loot(self):
        """
        Support the 'grab' command which looks like this:
        == client.loot.spawn(dump).mine(vol.start + Vec3(*idx)) ==
        It is the convoluted way to find what block is at a coordinate.
        """
        parent = self

        class spawn_cls:
            def spawn(self, dump):
                class mine_cls:
                    def mine(self, pos: Vec3):
                        return str(parent.getblock(pos))

                return mine_cls()

        return spawn_cls()

    def fill(
        self,
        start: Vec3,
        end: Vec3,
        block: Item,
        mode: FillMode = FillMode.KEEP,
        filter: str = "",
    ):
        block = Item(block)  # ensure enum
        if block == Item.AIR:
            return
        start += self.offset
        end += self.offset + 1
        lower = Vec3(min(start.x, end.x), min(start.y, end.y), min(start.z, end.z))
        upper = Vec3(max(start.x, end.x), max(start.y, end.y), max(start.z, end.z))
        self.world[
            floor(lower.x) : floor(upper.x),
            floor(lower.y) : floor(upper.y),
            floor(lower.z) : floor(upper.z),
        ] = block

    ###########################################################################
    # the following are additional functions for use in tests #################
    ###########################################################################

    def getblock(self, pos: Vec3) -> Item:
        """return the block at position in the world"""
        pos += self.offset
        return self.world[int(pos.x), int(pos.y), int(pos.z)]

    def compare(self, position: Vec3, cube: Items):
        """verify that the contents of the world at pos matches cube"""
        ncube = np.array(cube)
        pos = position + self.offset
        upper = pos + Vec3(*(ncube.shape))
        world_slice = self.world[pos.x : upper.x, pos.y : upper.y, pos.z : upper.z]

        return np.array_equal(world_slice, ncube)
