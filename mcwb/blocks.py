""" render and transform cuboids of blocks in minecraft space """
from pathlib import Path
from typing import Any, Union

import numpy as np
from mcipc.rcon.enumerations import Item
from mcipc.rcon.je import Client

from mcwb.functions import shift
from mcwb.itemlists import grab, load_items, save_items
from mcwb.types import Anchor3, Cuboid, Items, Planes3d, Vec3
from mcwb.volume import Volume


class Blocks:
    """
    Represents a cubiod of arbitrary blocks in a minecraft world with functions
    for transforming and rendering those blocks in the world
    """

    def __init__(
        self,
        client: Client,
        position: Vec3,
        cube: Union[Items, np.ndarray],
        anchor: Anchor3 = Anchor3.BOTTOM_NW,
        render: bool = True,
    ) -> None:
        self._client = client
        self.anchor = anchor
        self.position = position

        if isinstance(cube, np.ndarray):
            self.ncube = cube
        else:
            self.ncube = np.array(cube, dtype=Item)

        self._create()

        if render:
            self._render()

    def _create(self) -> None:
        if self.ncube.ndim != 3:
            raise ValueError("invalid cube specification")

        self.volume = Volume.from_anchor(
            self.position, Vec3(*self.ncube.shape), self.anchor
        )
        self._solid: Any = self.ncube != Item.AIR

    @classmethod
    def from_volume(cls, client: Client, volume: Volume) -> "Blocks":
        """create a Blocks object from a Volume"""
        cuboid = grab(client, volume)
        return cls(client, volume.position, cuboid)

    def _render(self) -> None:
        """render the blocks into Minecraft"""
        for idx, block in np.ndenumerate(self.ncube):
            if self._solid[idx]:
                self._client.setblock(self.volume.start + Vec3(*idx), block)

    def _unrender(self, vector: Vec3, old_start: Vec3) -> None:
        """clear away exposed blocks from the previous move"""
        moved = shift(self.ncube, vector * 1)

        mask: Any = (moved == Item.AIR) & (self.ncube != Item.AIR)

        for idx, block in np.ndenumerate(self.ncube):
            if mask[idx]:
                self._client.setblock(old_start + Vec3(*idx), Item.AIR.value)

    def rotate(self, plane: Planes3d, steps: int = 1, clear=True) -> None:
        """rotate the blocks in place"""
        self.ncube = np.rot90(self.ncube, k=steps, axes=plane.value)

        if clear:  # TODO implement unrender for rotated blocks (challenging?)
            self.volume.fill(self._client)

        self._solid = self.ncube != Item.AIR
        self.volume = Volume.from_anchor(
            self.volume.position, Vec3(*self.ncube.shape), self.anchor
        )

        self._render()

    def move(self, vector: Vec3, clear: bool = True) -> None:
        """moves the cuboid by vector and redraws it"""
        old_start = self.volume.start
        self.volume = Volume.from_anchor(
            self.volume.position + vector, Vec3(*self.ncube.shape), self.anchor
        )

        self._render()

        if clear:
            self._unrender(vector, old_start)

    def move_to(self, position: Vec3, clear: bool = True) -> None:
        """moves the cuboid to position and redraws it"""
        old_volume = self.volume
        self.volume = Volume.from_anchor(position, Vec3(*self.ncube.shape), self.anchor)

        self._render()

        if clear:
            old_volume.fill(self._client)

    def to_cuboid(self) -> Cuboid:
        """return the blocks' contents as a Cuboid"""
        return self.ncube.tolist() # type: ignore

    def save_blocks(self, file: Path) -> None:
        """save the blocks to a file"""
        save_items(self.ncube, file)

    def load_blocks(self, file: Path) -> None:
        """load the blocks from a file"""
        cube = load_items(file)
        self.ncube = np.array(cube, dtype=Item)
        self._create()
        self._render()
