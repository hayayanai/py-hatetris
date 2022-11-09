from dataclasses import dataclass


@dataclass
class Cell:
    landed: bool
    # live: bool


class Well:
    cellses: list[list[Cell]]
    DEPTH: int = 23
    WIDTH: int = 10
    XS: list[int] = list(range(WIDTH))
    YS: list[int] = list(range(DEPTH))

    def __init__(self) -> None:
        self.cellses: list[list[Cell]] = []

        for _ in Well.YS:
            cells = []
            for _ in Well.XS:
                cells.append(Cell(landed=False))
            self.cellses.append(cells)

    def __deepcopy__(self, memo):
        well = Well()
        cellses = []
        for y in range(0, Well.DEPTH):
            cells = []
            for x in range(0, Well.WIDTH):
                cells.append(Cell(landed=self.at(x, y).landed))
            cellses.append(cells)
        return well

    def at(self, x: int, y: int) -> Cell:
        """
        Negative index value raises IndexError.
        """
        if (x < 0 or y < 0):
            raise IndexError("index out of range.")
        return self.cellses[y][x]

    def get_cells_2d(self) -> list[list[int]]:
        """
        Return 2d list of empty: 0 and filled: 1
        """
        res = []
        for y in range(0, Well.DEPTH):
            cells = []
            for x in range(0, Well.WIDTH):
                if (self.cellses[y][x].landed):
                    cells.append(1)
                else:
                    cells.append(0)
            res.append(cells)
        return res

    def get_cells_1d(self) -> list[int]:
        res = []
        for y in range(0, Well.DEPTH):
            for x in range(0, Well.WIDTH):
                if (self.cellses[y][x].landed):
                    res.append(1)
                else:
                    res.append(0)
        return res

    def _get_cells_decimal(self) -> int:
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
        for y in range(Well.DEPTH):
            is_filled = True
            for x in range(Well.WIDTH):
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
            for _ in range(Well.WIDTH):
                cells.append(Cell(landed=False))
            self.cellses.append(cells)

    def get_column_heights(self) -> list[int]:
        """
        それぞれの列の一番上にあるブロックの高さ(int)
        """
        res = [0] * Well.WIDTH
        for x in Well.XS:
            for y in range(0, Well.DEPTH)[::-1]:
                if (self.at(x, y).landed):
                    res[x] = y + 1
                    break
        return res

    def get_heights_diff(self) -> list[int]:
        lis = self.get_column_heights()
        ans = [0] * (Well.WIDTH - 1)
        for x in range(Well.WIDTH - 1):
            ans[x] = abs(lis[x] - lis[x + 1])
        return ans

    def get_heights_diff_limit(self) -> list[int]:
        lis = self.get_column_heights()
        ans = [0] * (Well.WIDTH - 1)
        for x in range(Well.WIDTH - 1):
            val = abs(lis[x] - lis[x + 1])
            ans[x] = val if val <= 3 else 3
        return ans

    def get_holes(self) -> int:
        """
        空白のうち、上方向に1つでもブロックが存在する穴の個数(int)
        """
        count = 0
        r_cellses = list(reversed(self.cellses))
        for x in Well.XS:
            below = False
            for y in Well.YS:
                empty = r_cellses[y][x].landed is False
                if not below and not empty:
                    below = True
                elif below and empty:
                    count += 1
        return count

    def get_enclosed_holes(self) -> int:
        """
        上方向にブロックがある空白のうち、空白を辿ったとき、最上部に到達できない空白の個数
        """
        count = 0
        lis = []
        for y in range(0, Well.DEPTH)[::-1]:
            for x in range(0, Well.WIDTH):
                if (not self.at(x, y).landed):
                    for yy in range(y + 1, Well.DEPTH):
                        if (self.at(x, yy).landed):
                            lis.append((x, y))
        for p in lis:
            x, y = p
            s_y = y
            while s_y < Well.DEPTH:
                s_y += 1
        return count

    def get_bumpiness(self) -> int:
        """
        隣との高さの差の絶対値の合計。
        すなわち、表面が凸凹なほどプラス
        """
        v = 0
        lis = self.get_column_heights()
        for x in range(Well.WIDTH - 1):
            v += abs(lis[x] - lis[x + 1])
        return v

    def get_deviation(self) -> int | float:
        """
        各列の高さ - 高さの平均 の絶対値の合計
        """
        v = 0
        lis = self.get_column_heights()
        mean = sum(lis) / len(lis)
        for x in lis:
            v += abs(x - mean)
        return v

    def get_row_transitions(self) -> int:
        """Returns the number of horizontal cell transitions."""
        total = 0
        for y in reversed(range(Well.DEPTH)):
            row_count = 0
            last_empty = False
            for x in Well.XS:
                empty = self.cellses[y][x].landed == 0
                if last_empty != empty:
                    row_count += 1
                    last_empty = empty

            if last_empty:
                row_count += 1

            if last_empty and row_count == 2:
                continue

            total += row_count
        return total

    def get_column_transitions(self) -> int:
        """Returns the number of vertical cell transitions."""
        total = 0
        for x in Well.XS:
            column_count = 0
            last_empty = False
            for y in range(Well.DEPTH):
                empty = self.cellses[y][x].landed == 0
                if last_empty and not empty:
                    column_count += 2
                last_empty = empty

            if last_empty and column_count == 1:
                continue

            total += column_count
        return total

    def get_cumulative_wells(self) -> int:
        """Returns the sum of all wells."""
        wells = [0] * Well.WIDTH
        r_cellses = list(reversed(self.cellses))
        for y, row in enumerate(r_cellses):
            left_empty = True
            for x, code in enumerate(row):
                if code.landed is False:
                    well = False
                    right_empty = Well.WIDTH > x + 1 >= 0 and r_cellses[y][x + 1].landed is False
                    if left_empty or right_empty:
                        well = True
                    wells[x] = 0 if well else wells[x] + 1
                    left_empty = True
                else:
                    left_empty = False
        return sum(wells)

    def render_wells(self) -> None:
        for y in range(0, Well.DEPTH)[::-1]:
            for x in range(0, Well.WIDTH):
                if (self.cellses[y][x].landed):
                    print("#", end="")
                else:
                    print(".", end="")
            print()


if __name__ == "__main__":
    field = Well()
    board_blueprint = [
        "          ",
        "          ",
        "          ",
        "          ",
        "          ",
        "          ",
        "          ",
        "   ##     ",
        "   ##    #",
        "   ##    #",
        "   ###   #",
        "# ##### ##",
        "# ### # ##",
        "# ########",
        "# ####### ",
        "#### #####",
        " ####   ##",
        " #########",
        " #########",
        " #########",
    ]
    board_blueprint.reverse()
    for y in range(len(board_blueprint)):
        for x in range(Well.WIDTH):
            field.at(x, y).landed = True if board_blueprint[y][x] == "#" else False
    field.render_wells()
