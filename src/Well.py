from typing import Literal
from Cell import Cell


class Well:
    cellses: list[list[Cell]]
    wellDepth: int = 23
    wellWidth: int = 10

    def __init__(self) -> None:
        self.cellses: list[list[Cell]] = []

        for y in range(0, self.wellDepth):
            cells = []
            for x in range(0, self.wellWidth):
                # landed = (well is not None) and (well[y] & (1 << x)) != 0

                # live: bool
                # if (piece is None):
                #     live = False
                # else:
                #     orientation: Orientation = rotationSystem.rotations[piece.id][piece.o]
                #     y2 = y - piece.y - orientation.yMin
                #     x2 = x - piece.x - orientation.xMin
                #     live = (y2 >= 0 and y2 < orientation.yDim and x2 >= 0 and x2 <
                #             orientation.xDim and (orientation.rows[y2] & (1 << x2)) != 0)

                cells.append(Cell(landed=False, live=False))
            self.cellses.append(cells)

    def at(self, x: int, y: int) -> Cell:
        """
        Negative index value raises IndexError.
        """
        if (x < 0 or y < 0):
            raise IndexError("index out of range.")
        return self.cellses[y][x]

    def getcells2D(self) -> list[list[Literal[0, 1]]]:
        res = []
        for y in range(0, self.wellDepth):
            cells = []
            for x in range(0, self.wellWidth):
                if (self.cellses[y][x].landed):
                    cells.append(1)
                else:
                    cells.append(0)
            res.append(cells)
        return res

    def getcells1D(self) -> list[Literal[0, 1]]:
        res = []
        for y in range(0, self.wellDepth):
            for x in range(0, self.wellWidth):
                if (self.cellses[y][x].landed):
                    res.append(1)
                else:
                    res.append(0)
        return res

    def renderWells(self):
        for y in range(0, self.wellDepth)[::-1]:
            for x in range(0, self.wellWidth):
                if (self.cellses[y][x].landed):
                    print("#", end="")
                else:
                    print(".", end="")
            print()