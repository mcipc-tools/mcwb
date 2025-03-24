"""
Functions for manipulating lists of Items
    1d = Row
    2d = Profile
    3d = Cuboid
"""

import codecs
import json
from pathlib import Path
from typing import Union

import numpy as np
from numpy.typing import NDArray
from mcipc.rcon.enumerations import Item
from mcipc.rcon.je import Client

from mcwb.api import get_block
from mcwb.functions import validate
from mcwb.types import Cuboid, Items, Vec3
from mcwb.volume import Volume

ITEM_KEY = "__Item__"


def save_items(items: Items, filename: Path) -> None:
    """save a Profile, Cuboid or Row to a json file"""

    if isinstance(items, np.ndarray):
        items = items.tolist() # type: ignore

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


def load_items(filename: Union[Path, str], dimensions: int = 0) -> Items:
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

    if dimensions != 0 and valid_dims != dimensions:
        raise ValueError(
            "file {filename} contains {valid_dims} dimension Items"
            "but {dimensions} dimensions was requested"
        )

    return result


def grab(client: Client, vol: Volume) -> Cuboid:
    """copy blocks from a Volume in the minecraft world into a cuboid of Item"""
    cube: NDArray[Item] = np.ndarray(vol.size.i_tuple, dtype=Item)

    for idx, _ in np.ndenumerate(cube):
        cube[idx] = get_block(client, vol.start + Vec3(*idx))

    result = cube.tolist()
    return result # type: ignore
