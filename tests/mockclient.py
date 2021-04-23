"""
A mock client for testing functions that call the minecraft server.
This mocks a world of 100 blocks square with origin in the middle.
"""

from mcwb.types import Items, Vec3
import numpy as np

from mcipc.rcon.enumerations import Item


class MockClient:
    def __init__(self):
        """ create an empty mock world """
        self.world = np.full((100, 100, 100), Item.AIR, dtype=Item)
        self.offset = Vec3(50, 50, 50)

    # the following are mock versions of the original Client Functions

    def setblock(self, position: Vec3, block: Item):
        """ set the block at position in the world """
        pos = position - self.offset
        self.world[pos.x, pos.y, pos.z] = block

    def fill(self, start: Vec3, end: Vec3, block: Item):
        block = Item(block)  # ensure enum
        start -= self.offset
        end -= self.offset - 1
        self.world[start.x:end.x, start.y:end.y, start.z:end.z] = block

    # the following are additional functions for use in tests

    def getblock(self, position: Vec3) -> Item:
        """ return the block at position in the world """
        pos = position - self.offset
        return self.world[pos.x, pos.y, pos.z]

    def compare(self, position: Vec3, cube: Items):
        """ verify that the contents of the world at pos matches cube """
        ncube = np.array(cube)
        pos = position - self.offset
        upper = pos + Vec3(*(ncube.shape))
        world_slice = self.world[pos.x:upper.x, pos.y:upper.y, pos.z:upper.z]

        return np.array_equal(world_slice, ncube)
