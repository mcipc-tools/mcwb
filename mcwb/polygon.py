"""
functions for creating polygons in profiles (2d lists of Items)
"""
import math
import operator
from typing import List, Optional, Tuple

import numpy as np
from mcipc.rcon.enumerations import Item


def poly_points(diameter: int, sides: int, offset: Optional[float] = None):
    """
    Returns a set of 2d points tp make a polygon with the given diameter and
    number of sides.
    """

    x_points: List[int] = []
    z_points: List[int] = []

    if sides < 3:
        raise ValueError("Number of sides must be at least 3.")

    radius = diameter // 2
    angle = 2 * math.pi / sides
    offset = angle / 2 if offset is None else offset
    for i in range(sides):
        x_points.append(round(radius * math.cos(i * angle + offset)))
        z_points.append(round(radius * math.sin(i * angle + offset)))

    return x_points, z_points


def poly_profile(
    sides=4, diameter=15, item: Item = Item.STONE, offset=None
) -> np.ndarray:
    """
    Create a profile containing a polygon. The dimensions of the profile
    will be just large enough to contain the specified polygon.
    """

    x_points, z_points = poly_points(diameter=diameter, sides=sides, offset=offset)
    x_size = max(x_points) - min(x_points) + 1
    z_size = max(z_points) - min(z_points) + 1
    vertices = [(x, z) for x, z in zip(x_points, z_points)]

    profile = np.full(shape=(x_size, z_size), fill_value=Item.AIR)
    center = math.floor(x_size / 2), math.floor(z_size / 2)

    return poly_draw(profile, vertices, center, item)


def poly_draw(
    profile: np.ndarray,
    vertices: List[Tuple[int, int]],
    center: Tuple[int, int],
    item: Item,
) -> np.ndarray:
    """
    Take a list of 2d points and draw lines between them to make a polygon
    inside of a profile (2d array of Item).
    """

    def add_2d(x, z):
        return tuple(map(operator.add, x, z))

    sides = len(vertices)

    for i in range(sides):
        draw_line_xz(
            profile,
            add_2d(center, vertices[i]),
            add_2d(center, vertices[(i + 1) % sides]),
            item,
        )
    return profile


def draw_line_xz(
    profile: np.ndarray,
    start: Tuple[int, int],  # x, z
    end: Tuple[int, int],  # x, z
    item: Item = Item.AIR,
    overlap: int = 0,
):
    """
    Creates a line of blocks from start to end inside a 2d profile.
    """

    def delta(n1, n2):
        return (-1, n1 - n2) if n1 > n2 else (1, n2 - n1)

    dir_x, delta_x = delta(start[0], end[0])
    dir_z, delta_z = delta(start[1], end[1])

    steps = max(delta_x, delta_z) or 1

    x_step = delta_x / steps * dir_x
    z_step = delta_z / steps * dir_z

    x, z = start[0], start[1]
    next_x, next_z = x, z

    profile[x][z] = item

    for i in range(steps + 1):
        if (x, z) != (round(next_x), round(next_z)):
            x, z = round(next_x), round(next_z)
            profile[x][z] = item
        next_z += z_step
        next_x += x_step
