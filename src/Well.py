from typing import Literal

from dataclasses import dataclass


@dataclass
class Cell:
    landed: bool
    live: bool


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

    def get_cells_2d(self) -> list[list[Literal[0, 1]]]:
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

    def get_cells_1d(self) -> list[Literal[0, 1]]:
        res = []
        for y in range(0, self.wellDepth):
            for x in range(0, self.wellWidth):
                if (self.cellses[y][x].landed):
                    res.append(1)
                else:
                    res.append(0)
        return res

    def get_cells_decimal(self) -> int:
        return int(("".join(map(str, self.get_cells_1d()))), 2)

    def delete_lines(self) -> int:
        """
        ラインを消去し、消去したライン数を返す。
        """
        count = 0
        while self._filled_line() != -1:
            self._cut_line(self._filled_line())
            count += 1
        return count

    def _filled_line(self) -> int:
        """埋まっている段を一つ返す。なければ-1。
        """
        for y in range(Well.wellDepth):
            is_filled = True
            for x in range(Well.wellWidth):
                if not self.at(x, y).landed:
                    is_filled = False
                    break
            if is_filled:
                return y
        return -1

    def _cut_line(self, y: int) -> None:
        if (y <= -1):
            raise ValueError("Invalid line for this method!")
        else:
            del self.cellses[y]
            cells = []
            for _ in range(Well.wellWidth):
                cells.append(Cell(landed=False, live=False))
            self.cellses.append(cells)

    def get_column_heights(self) -> list[int]:
        res = [0] * Well.wellWidth
        for x in range(Well.wellWidth):
            for y in range(0, Well.wellDepth)[::-1]:
                if (self.at(x, y).landed):
                    res[x] = y
                    break
        return res

    def get_holes(self) -> int:
        """
        空白のうち、上方向に1つでもブロックが存在する穴の個数(int)
        """
        count = 0
        for y in range(0, self.wellDepth)[::-1]:
            for x in range(0, self.wellWidth):
                if (not self.at(x, y).landed):
                    for yy in range(y + 1, self.wellDepth):
                        if (self.at(x, yy).landed):
                            count += 1
                            break
        return count

    def render_wells(self):
        for y in range(0, Well.wellDepth)[::-1]:
            for x in range(0, Well.wellWidth):
                if (self.cellses[y][x].landed):
                    print("#", end="")
                else:
                    print(".", end="")
            print()


if __name__ == "__main__":
    field = Well()
    field.cellses[20][1].landed = True
    field.cellses
    print(field.get_cells_1d())
