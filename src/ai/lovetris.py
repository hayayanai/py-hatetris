from Piece import Piece

from ai.enemy import EnemyAi


class Lovetris(EnemyAi):
    def __init__(self) -> None:
        super().__init__()
        pass

    def get_first_piece(self) -> Piece:
        """
        # Return
        Always `I` Piece
        """
        return Piece(3)
