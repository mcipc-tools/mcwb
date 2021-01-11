from mcipc.rcon.enumerations import Item
from mcipc.rcon.errors import InvalidArgument
from mcipc.rcon.je import Client

from mcwb import Anchor, Anchor3, Direction, Vec3, mktunnel

__all__ = ['Volume']


class Volume:
    """
    Describes a 3d space in a Minecraft world using a starting point and
    size. The starting point can be any vertex or the middle of one of the
    horizontal faces, using the cardinal terminology defined in Anchor3.
    """

    def __init__(
        self,
        position: Vec3,
        size: Vec3 = None,
        anchor: Anchor3 = Anchor3.BOTTOM_NW,
        end: Vec3 = None,  # opposite corner instead of size and anchor
    ):
        if (size is None) == (end is None):
            raise InvalidArgument(
                "Volume constructor takes only one of size or end")
        position = Vec3(*position)

        if end is None:
            size = Vec3(*size)
            offset = Vec3(0, 0, 0)
            if anchor.value in Anchor3.TOP.value:
                offset += Vec3(0, 1 - size.y, 0)
            if anchor.value in Anchor3.SOUTH.value:
                offset += Vec3(0, 0, 1 - size.z)
            if anchor.value in Anchor3.EAST.value:
                offset += Vec3(1 - size.x, 0, 0)
            if anchor.value in Anchor3.MIDDLE_FACE.value:
                offset -= Vec3(int(size.x / 2), 0, int(size.z / 2))
            elif anchor.value == Anchor3.MIDDLE.value:
                offset = Vec3(-1, -1, -1) * (size / 2).with_ints()

            self.start = position + offset
            self.end = self.start + (size - 1)
        else:
            end = Vec3(*end)
            # normalize start(position) and end so all start coords are minima
            position = self.start = Vec3(
                min(position.x, end.x), min(
                    position.y, end.y), min(position.z, end.z)
            )
            self.end = Vec3(
                max(position.x, end.x), max(
                    position.y, end.y), max(position.z, end.z)
            )
            size = end - position + 1
            anchor = Anchor3.BOTTOM_NW

        self.size = size
        self.position = position
        self.anchor = anchor

    def inside(
        self, position: Vec3, xtol: int = 0, ytol: int = 0, ztol: int = 0
    ) -> bool:
        """ determine if position is within the Volume """
        return (
            self.start.x - xtol <= position.x <= self.end.x + xtol
            and self.start.y - ytol <= position.y <= self.end.y + ytol
            and self.start.z - ztol <= position.z <= self.end.z + ztol
        )

    def move(self, distance: Vec3) -> None:
        """ move the volume's location in space by distance """
        self.start += distance
        self.position += distance

    def move_to(self, position: Vec3) -> None:
        """ move the volume's location in space to position """
        self.start += position - self.position
        self.position = position

    def fill(self, client: Client, block: Item = Item.AIR):
        """ Fill the Volume with a single block type, supports large volumes """
        if self.size.volume < 32768:
            client.fill(self.start, self.end, block.value)
        else:
            profile = [[block.value] * int(self.size.x)] * int(self.size.y)
            mktunnel(
                client,
                profile,
                self.start,
                direction=Direction.UP,
                anchor=Anchor.BOTTOM_LEFT,
                length=int(self.size.dz),
            )

    def walls(
        self,
        client: Client,
        block: Item,
        thickness: int = 1,
        top: bool = True,
        bottom: bool = True,
        n: bool = True,
        s: bool = True,
        e: bool = True,
        w: bool = True,
    ) -> None:
        """ renders walls around the volume """
        t = thickness - 1
        b = block.value
        if n:
            client.fill(self.start, Vec3(
                self.end.x, self.end.y, self.start.z + t), b)
        if s:
            client.fill(self.end, Vec3(
                self.start.x, self.start.y, self.end.z - t), b)
        if w:
            client.fill(self.start, Vec3(
                self.start.x + t, self.end.y, self.end.z), b)
        if e:
            client.fill(self.end, Vec3(self.end.x - t,
                                       self.start.y, self.start.z), b)
        if top:
            client.fill(self.end, Vec3(
                self.start.x, self.end.y - t, self.start.z), b)
        if bottom:
            client.fill(self.start, Vec3(
                self.end.x, self.start.y + 1, self.end.z), b)
