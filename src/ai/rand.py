from random import randint

from piece import Piece

from ai.enemy import EnemyAi


class RandomAi(EnemyAi):
    def __init__(self, initial_seed: int, field: None = None) -> None:
        super().__init__(initial_seed)

    def get_first_piece(self) -> Piece:
        """Random

        Returns: Piece
        """
        # return Piece(randint(0, 1) * 3)
        return Piece(randint(0, 6))
