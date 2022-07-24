from pathlib import Path
from unittest import TestCase

from mcipc.rcon.enumerations import Item

from mcwb.api import polygon
from mcwb.itemlists import grab, load_items
from mcwb.types import Anchor3, Direction, Vec3
from mcwb.volume import Volume
from tests.mockclient import MockClient


class TestPoly(TestCase):
    def test_poly(self):
        client = MockClient(size=20)

        center = Vec3(x=0, y=0, z=0)
        corner = Vec3(x=-2, y=0, z=-2)

        polygon(
            client,  # type: ignore
            center=center,
            sides=4,
            height=2,
            diameter=5,
            item=Item.BLUE_CONCRETE,
            offset=None,
            direction=Direction.UP,
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

        assert client.compare(corner, expected)

        assert cuboid == expected

    def test_filled_poly(self):
        client = MockClient(size=20)

        center = Vec3(x=0, y=0, z=0)
        corner = Vec3(x=-2, y=0, z=-2)

        polygon(
            client,  # type: ignore
            center=center,
            sides=4,
            height=2,
            diameter=5,
            item=Item.BLUE_CONCRETE,
            offset=None,
            direction=Direction.UP,
            fill_item=Item.RED_CONCRETE,
        )

        # test against a saved cube
        cube_path = Path("tests/cubes/polyfill.cube")
        expected = load_items(cube_path)

        assert client.compare(corner, expected)
