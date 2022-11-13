from src.ai.hatetris import HatetrisAi
from src.piece import Mino
from src.well import Well


class Test_HatetrisAi:
    def test_get_next_piece(self):
        field = Well()
        ai = HatetrisAi(field)
        piece = ai.get_next_piece()
        assert piece.id == Mino.S.value
