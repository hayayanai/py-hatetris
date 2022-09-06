from random import randint

from Piece import Piece

from ai.enemy import EnemyAi
from collections import deque


class SevenAi(EnemyAi):
    def __init__(self) -> None:
        super().__init__()
        self.pieces: deque[Piece] = deque()
        self.rng: int = self._rng()
        self._generate()
        self.piece = self.pieces.popleft()

    def _rng(self):
        return randint(0, 2**31)

    def _generate(self):
        while len(self.pieces) < 12:
            bag: list[int] = [0, 1, 2, 3, 4, 5, 6]

            for i in range(0, 7)[::-1]:  # フィッシャーイェーツ
                # this.rng = this.rng_next();
                j = i + (self._rng() % (7 - i))
                if (j < 0):
                    j *= -1

                new_value = bag[j]
                old_value = bag[i]
                bag[i] = new_value
                bag[j] = old_value

            for i in range(0, 7):
                self.pieces.append(Piece(bag[i]))

    def get_first_piece(self) -> Piece:
        return self.piece

    def get_next_piece(self) -> Piece:
        self.piece = self.pieces.popleft()
        self._generate()
        return self.piece
