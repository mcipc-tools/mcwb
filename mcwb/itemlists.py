"""
Functions for manipulating lists of Items
    1d = Row
    2d = Profile
    3d = Cuboid
"""

import codecs
import json
import re
from pathlib import Path
from typing import Union

import numpy as np
from mcipc.rcon.enumerations import Item
from mcipc.rcon.je import Client

from mcwb import Cuboid, Vec3, Volume, Items
from mcwb.functions import validate


ITEM_KEY = "__Item__"


def save_items(items: Items, filename: Path) -> None:
    """save a Profile, Cuboid or Row to a json file"""

    def json_item(item: Item):
        return {ITEM_KEY: item.value}

    if validate(items) == 0:
        raise ValueError("items is not a valid Row, Profile or Cuboid")

    json.dump(
        items,
        codecs.open(str(filename), "w", encoding="utf-8"),
        separators=(",", ":"),
        sort_keys=True,
        indent=4,
        default=json_item,
    )


def load_items(filename: Union[Path, str], dimensions: int = None) -> Items:
    """load a JSON file of Items - returns a Cuboid, Profile or Row"""

    def as_item(dct: dict):
        if ITEM_KEY in dct:
            return Item(dct[ITEM_KEY])

        return dct

    result = json.load(
        codecs.open(str(filename), "r", encoding="utf-8"), object_hook=as_item
    )
    valid_dims = validate(result)

    if valid_dims == 0:
        raise ValueError("file {filename} contains invalid JSON")

    if dimensions is not None and valid_dims != dimensions:
        raise ValueError(
            "file {filename} contains {valid_dims} dimension Items"
            "but {dimensions} dimensions was requested"
        )

    return result


dump = Vec3(0, 0, 0)
extract_item = re.compile(r".*minecraft\:(?:blocks\/)?(.+)$")


def grab(client: Client, vol: Volume) -> Cuboid:
    """copy blocks from a Volume in the minecraft world into a cuboid of Item"""
    ncube = np.ndarray(vol.size, dtype=Item)

    for idx, _ in np.ndenumerate(ncube):
        # currently the only way to test for a block is to use the loot spawn
        # command, this creates an entity at 0, 0, 0 that falls into the void
        output = client.loot.spawn(dump).mine(vol.start + Vec3(*idx))
        match = extract_item.search(output)
        if not match:
            raise ValueError(f"unexpected response from loot spawn: {output}")
        name = match.group(1)
        if name == "empty":
            name = "air"
        ncube[idx] = Item(name)

    result = ncube.tolist()
    return result
