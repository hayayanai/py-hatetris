from piece import Mino, Piece

from ai.enemy import EnemyAi


class Lovetris(EnemyAi):
    def __init__(self, initial_seed: None = None, field: None = None) -> None:
        super().__init__()

    def get_first_piece(self) -> Piece:
        return Piece(Mino.I)
