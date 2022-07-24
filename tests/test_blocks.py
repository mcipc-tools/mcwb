from pathlib import Path
from typing import cast
from unittest import TestCase

from mcipc.rcon import Client

from mcwb.blocks import Blocks
from mcwb.itemlists import load_items
from mcwb.types import Planes3d, Vec3
from tests.mockclient import MockClient

cubes_dir = Path(__file__).parent / "cubes"


class TestRotation(TestCase):
    """Test the rotate() function."""

    def setUp(self):
        self.client = MockClient()
        self.cube = load_items(cubes_dir / "RGB.cube")
        self.start = Vec3(0, 0, 0)

    def test_XY(self):
        world_cube = Blocks(cast(Client, self.client), self.start, self.cube)
        for rot in range(1, 4):
            world_cube.rotate(Planes3d.XY)
            rotated = load_items(cubes_dir / f"RGBrotateXY{rot}.cube")

            self.assertTrue(self.client.compare(self.start, rotated))

        # 4th rotation returns to original state
        world_cube.rotate(Planes3d.XY)
        self.assertTrue(self.client.compare(self.start, self.cube))

    def test_XZ(self):
        world_cube = Blocks(cast(Client, self.client), self.start, self.cube)
        world_cube.rotate(Planes3d.XZ)
        rotated = load_items(cubes_dir / "RGBrotateXZ1.cube")

        self.assertTrue(self.client.compare(self.start, rotated))

    def test_YZ(self):
        world_cube = Blocks(cast(Client, self.client), self.start, self.cube)
        world_cube.rotate(Planes3d.YZ)
        rotated = load_items(cubes_dir / "RGBrotateYZ1.cube")

        self.assertTrue(self.client.compare(self.start, rotated))
