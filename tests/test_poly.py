from pathlib import Path
from unittest import TestCase

from mcipc.rcon.enumerations import Item

from mcwb.api import polygon
from mcwb.itemlists import grab, load_items, save_items
from mcwb.types import Anchor3, Direction, Vec3
from mcwb.volume import Volume
from tests.mockclient import MockClient


class TestPoly(TestCase):
    def test_poly(self):
        center = Vec3(x=0, y=0, z=0)
        corner = Vec3(x=-2, y=0, z=-2)
        sides = 4
        diameter = 5
        offset = None
        height = 2
        direction = Direction.UP

        client = MockClient(size=20)

        item = Item.BLUE_CONCRETE
        polygon(
            client,  # type: ignore
            center=center,
            sides=sides,
            height=height,
            diameter=diameter,
            item=item,
            offset=offset,
            direction=direction,
        )

        # test against a saved cube
        cube_path = Path("tests/cubes/poly.cube")
        expected = load_items(cube_path)

        # also test using the grab function
        vol = Volume.from_anchor(center, Vec3(5, 5, 5), Anchor3.BOTTOM_CENTER)
        cuboid = grab(
            client,  # type: ignore
            vol,
        )

        cube_path2 = Path("tests/cubes/poly2.cube")
        save_items(cuboid, cube_path2)

        assert client.compare(corner, expected)

        assert cuboid == expected
