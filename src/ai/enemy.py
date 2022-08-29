from abc import ABCMeta, abstractmethod

from Piece import Piece


class EnemyAi(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_first_piece() -> Piece:
        pass

    # @abstractmethod
    # def get_next_piece() -> Piece:
    #     pass
