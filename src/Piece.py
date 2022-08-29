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
    x: int
    y: int
    id: int
    age: int

    def __init__(self, piece_id: int = 0) -> None:
        self.x = 3
        self.y = 19
        self.id = piece_id
        self.age = 0
        pass

    def __str__(self) -> str:
        return f"x: {self.x}, y:{self.y}"

    @property
    def name(self) -> str:
        """id -> str
        # Return
        'I', 'J', 'L', 'O', 'S', 'T', 'Z'
        """
        return list(Piece.unmodified.keys())[self.id]

    @property
    def pos(self) -> tuple[int, int]:
        return self.x, self.y

# todo: def getNextPiece(field:Well) を書く。

    def handle_input(self, action: str) -> None:
        if (action == "D"):
            if (self.y > 0):
                self.y -= 1
        elif (action == "L"):
            if (self.x > 0):
                self.x -= 1
        elif (action == "R"):
            if (self.x < 9):
                self.x += 1
        elif (action == "U"):
            pass


piece = Piece(0)
print(piece.name)
# while True:
#     piece.handle_input(input())
#     print(piece.y)

# print(Piece.unmodified["I"][0][1][1])
