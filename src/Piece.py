from typing import Literal


class Piece:
    unmodified: dict[str, list[list[str, str, str, str]]] = {
        "I": [
            [
                '....',
                '####',
                '....',
                '....'
            ], [
                '..#.',
                '..#.',
                '..#.',
                '..#.'
            ], [
                '....',
                '....',
                '####',
                '....'
            ], [
                '.#..',
                '.#..',
                '.#..',
                '.#..'
            ]
        ],

        "J": [
            [
                '....',
                '.##.',
                '.#..',
                '.#..'
            ], [
                '....',
                '###.',
                '..#.',
                '....'
            ], [
                '..#.',
                '..#.',
                '.##.',
                '....'
            ], [
                '....',
                '.#..',
                '.###',
                '....'
            ]
        ],

        "L": [
            [
                '....',
                '.###',
                '.#..',
                '....'
            ], [
                '....',
                '.##.',
                '..#.',
                '..#.'
            ], [
                '....',
                '..#.',
                '###.',
                '....'
            ], [
                '.#..',
                '.#..',
                '.##.',
                '....'
            ]
        ],

        "O": [
            [
                '....',
                '.##.',
                '.##.',
                '....'
            ], [
                '....',
                '.##.',
                '.##.',
                '....'
            ], [
                '....',
                '.##.',
                '.##.',
                '....'
            ], [
                '....',
                '.##.',
                '.##.',
                '....'
            ]
        ],

        "S": [
            [
                '....',
                '..##',
                '.##.',
                '....'
            ], [
                '....',
                '.#..',
                '.##.',
                '..#.'
            ], [
                '....',
                '.##.',
                '##..',
                '....'
            ], [
                '.#..',
                '.##.',
                '..#.',
                '....'
            ]
        ],

        "T": [
            [
                '....',
                '.###',
                '..#.',
                '....'
            ], [
                '....',
                '..#.',
                '.##.',
                '..#.'
            ], [
                '....',
                '.#..',
                '###.',
                '....'
            ], [
                '.#..',
                '.##.',
                '.#..',
                '....'
            ]
        ],

        "Z": [
            [
                '....',
                '.##.',
                '..##',
                '....'
            ], [
                '....',
                '..#.',
                '.##.',
                '.#..'
            ], [
                '....',
                '##..',
                '.##.',
                '....'
            ], [
                '..#.',
                '.##.',
                '.#..',
                '....'
            ]
        ]
    }
    pieces: list = list(unmodified.keys())
    x: int
    y: int
    id: int
    rot: Literal[0, 1, 2, 3]
    age: int

    def __init__(self, piece_id: int = 0) -> None:
        self.x = 3
        self.y = 19
        self.id = piece_id
        self.rot = 0
        self.age = 0
        pass

    def __str__(self) -> str:
        return f"{self.id}{self.name}, x:{self.x}, y:{self.y}, rot:{self.rot}"

    @property
    def name(self) -> Literal['I', 'J', 'L', 'O', 'S', 'T', 'Z']:
        """id: int -> key: str
        """
        return list(Piece.unmodified.keys())[self.id]

    @property
    def pos(self) -> tuple[int, int]:
        return self.x, self.y

    def get_char(self, x: int, y: int) -> Literal["#", "."]:
        return self.unmodified[self.name][self.rot][y][x]

# todo: def getNextPiece(field:Well) を書く。


if __name__ == "__main__":
    piece = Piece(0)
    print(piece.get_char(1, 0))
# while True:
#     piece.handle_input(input())
#     print(piece.y)

# print(Piece.unmodified["I"][0][1][1])
