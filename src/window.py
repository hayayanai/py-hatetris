from tkinter import Canvas, Tk

from game import Game
from well import Well

SIZE = 25

WIDTH = Well.WIDTH * SIZE + 400
HEIGHT = Well.DEPTH * SIZE


class RenderWindow(Tk):
    def __init__(self, env: Game) -> None:
        super().__init__()
        self.game: Game = env
        self.render_offset = 5
        self.geometry("%dx%d" % (
            WIDTH + self.render_offset * 2,
            HEIGHT + self.render_offset * 2
        )
        )
        self.canvas = Canvas(self,
                             width=WIDTH + self.render_offset * 2,
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
        for _y in range(0, Well.DEPTH):
            for x in range(Well.WIDTH):
                y = Well.DEPTH - _y - 1
                if (self.game.field.cellses[_y][x].landed):
                    self.canvas.create_rectangle(
                        x * SIZE, y * SIZE, (x + 1) * SIZE, (y + 1) * SIZE, fill="blue")
                else:
                    self.canvas.create_rectangle(
                        x * SIZE, y * SIZE, (x + 1) * SIZE, (y + 1) * SIZE, fill="white")

    def _render_piece(self):
        print(self.game.piece)
        for _y in range(0, 4):
            for x in range(0, 4):
                if (self.game.piece.get_char(x, _y) == "#"):
                    # y = -_y + Well.DEPTH - self.game.piece.y - 1
                    y = Well.DEPTH - self.game.piece.y + _y - 4
                    print(y)
                    self.canvas.create_rectangle(
                        (x + self.game.piece.x) * SIZE, y * SIZE, (x + self.game.piece.x + 1) * SIZE, (y + 1) * SIZE, fill="red")

    def _render_info(self):
        txt = f"""
        column_heights:
            {self.game.field.get_column_heights()}
        holes: {self.game.field.get_holes()}
        bumpiness: {self.game.field.get_bumpiness()}
        deviation: {self.game.field.get_deviation()}
        total_cleared_line: {self.game.total_cleared_line}
        total_piece: {self.game.total_piece}
        score: {self.game.score}
        """
        self.canvas.create_text(Well.WIDTH * SIZE + 150, 100, font=("", 18), text=txt)


# class RenderServer():
#     from flask import Flask

#     app = Flask(__name__, static_folder=None)

#     @app.route("/")
#     def processing():
#         response = """
#     <html>
#     <head>
#         <title>Processing</title>
#         <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.2/p5.min.js"></script>
#         </script>
#         <script id="processing-code">
#             function setup() {{
#                 createCanvas({w}, {h});
#             }}

#             function draw() {{
#                 background(51);
#             }}
#         </script>
#     </head>
#     <body>
#     </body>
#     """.format(w=WIDTH, h=HEIGHT)
#         return response


# if __name__ == "__main__":
#     server = RenderServer()
#     server.app.run(debug=True, host="0.0.0.0", port=5000)
