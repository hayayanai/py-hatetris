from random import randint

from Piece import Piece

from ai.enemy import EnemyAi


class RandomAi(EnemyAi):
    def __init__(self) -> None:
        super().__init__()
        pass

    def get_first_piece(self) -> Piece:
        """
        # Return
        Random
        """
        return Piece(randint(0, 6))
