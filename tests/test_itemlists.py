
import shutil
import tempfile
from pathlib import Path
from unittest import TestCase

from mcipc.rcon.item import Item
from mcwb.itemlists import load_items, save_items


class TestItemLists(TestCase):
    """Tests saving and loading lists of Items"""

    def setUp(self):
        """Sets example shapes and a temporary directory."""
        self.test_dir = Path(tempfile.mkdtemp())

        self.blue_row = [
            Item.BLUE_CONCRETE,
            Item.BLUE_CONCRETE,
            Item.BLUE_CONCRETE
        ]
        self.red_row = [
            Item.RED_CONCRETE,
            Item.RED_CONCRETE,
            Item.RED_CONCRETE
        ]
        self.hollow_row = [
            Item.RED_CONCRETE,
            Item.AIR,
            Item.RED_CONCRETE
        ]
        self.top_profile = [
            self.blue_row,
            self.red_row,
            self.red_row
        ]
        self.middle_profile = [
            self.blue_row,
            self.hollow_row,
            self.red_row
        ]
        self.bottom_profile = [
            self.blue_row,
            self.blue_row,
            self.red_row
        ]
        self.cube = [
            self.top_profile,
            self.middle_profile,
            self.bottom_profile
        ]

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(str(self.test_dir))

    def test_save_row(self):
        p = self.test_dir / "row_test.json"
        save_items(self.blue_row, p)
        items = load_items(p, 1)

        self.assertEqual(items, self.blue_row)

    def test_save_profile(self):
        p = self.test_dir / "row_profile.json"
        save_items(self.middle_profile, p)
        items = load_items(p, 2)

        self.assertEqual(items, self.middle_profile)

    def test_save_cuboid(self):
        p = self.test_dir / "row_cuboid.json"
        save_items(self.cube, p)
        items = load_items(p, 3)

        self.assertEqual(items, self.cube)

        # validate failed dimension check
        with self.assertRaises(ValueError):
            load_items(p, 2)

        # validate the 'any dimensions' call to load_items
        items = load_items(p)
        self.assertEqual(items, self.cube)
