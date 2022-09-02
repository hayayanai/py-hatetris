from tkinter import Canvas, Tk

from Game import Game
from Well import Well

SIZE = 20

WIDHT = Well.wellWidth * SIZE
HEIGHT = Well.wellDepth * SIZE


class RenderWindow(Tk):
    def __init__(self, env: Game) -> None:
        super().__init__()
        self.game: Game = env
        self.render_offset = 5
        self.geometry("%dx%d" % (
            WIDHT + self.render_offset * 2,
            HEIGHT + self.render_offset * 2
        )
        )
        self.canvas = Canvas(self,
                             width=WIDHT + self.render_offset * 2,
                             height=HEIGHT + self.render_offset * 2,
                             bg="#fff"
                             )
        self.canvas.place(x=1, y=1)

    def render(self) -> None:
        self.canvas.delete("all")
        self._render_wells()
        self._render_piece()
        self._render_info()

    def _render_wells(self) -> None:
        for _y in range(0, Well.wellDepth):
            for x in range(Well.wellWidth):
                y = Well.wellDepth - _y - 1
                if (self.game.field.cellses[_y][x].landed):
                    self.canvas.create_rectangle(
                        x * SIZE, y * SIZE, (x + 1) * SIZE, (y + 1) * SIZE, fill="blue")
                else:
                    self.canvas.create_rectangle(
                        x * SIZE, y * SIZE, (x + 1) * SIZE, (y + 1) * SIZE, fill="white")

    def _render_piece(self):
        for _y in range(0, 4):
            for x in range(0, 4):
                if (self.game.piece.get_char(x, _y) == "#"):
                    y = -_y + Well.wellDepth - self.game.piece.y - 1
                    self.canvas.create_rectangle(
                        (x + self.game.piece.x) * SIZE, y * SIZE, (x + self.game.piece.x + 1) * SIZE, (y + 1) * SIZE, fill="red")

    def _render_info(self):
        pass
