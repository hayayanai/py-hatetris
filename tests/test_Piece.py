from src.Piece import Piece


class Test_Piece:

    def test_UNMODIFIED(self):
        assert Piece.UNMODIFIED["I"][0][1][1] == "#"

    def test_get_char(self):
        piece = Piece(0)
        assert piece.get_char(1, 0) == "."
