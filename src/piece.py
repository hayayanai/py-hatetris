from enum import Enum
from typing import Literal


class Mino(Enum):
    I = 0
    J = 1
    L = 2
    O = 3
    S = 4
    T = 5
    Z = 6


class Piece():
    UNMODIFIED: dict[str, list] = {
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
    PIECES: list = list(UNMODIFIED.keys())
    x: int
    y: int
    id: int
    rot: int
    age: int

    def __init__(self, piece: int | Mino = Mino.I) -> None:
        self.x = 3
        self.y = 19
        if isinstance(piece, int):
            self.id = piece
        elif isinstance(piece, Mino):
            self.id = piece.value
        self.rot = 0
        self.age = 0

    def __str__(self) -> str:
        return f"{self.id}{self.name}, x:{self.x}, y:{self.y}, rot:{self.rot}"

    @property
    def name(self) -> str:
        """id: int -> key: str
        ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
        """
        return list(Piece.UNMODIFIED.keys())[self.id]

    @property
    def pos(self) -> tuple[int, int]:
        return self.x, self.y

    def get_char(self, x: int, y: int) -> Literal["#", "."]:
        return self.UNMODIFIED[self.name][self.rot][y][x]


if __name__ == "__main__":
    pass
