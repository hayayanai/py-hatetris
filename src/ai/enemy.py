from abc import ABCMeta, abstractmethod

from piece import Piece
from well import Well


class EnemyAi(metaclass=ABCMeta):
    def __init__(self, initial_seed: int | None = None, field: Well | None = None) -> None:
        self.rng = initial_seed
        self.field = field
        pass

    @abstractmethod
    def get_first_piece(self) -> Piece:
        pass

    def get_next_piece(self) -> Piece:
        return self.get_first_piece()
