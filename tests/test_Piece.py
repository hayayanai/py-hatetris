from src.Piece import Piece


class Test_Piece:

    def test_unmodified(self):
        assert Piece.unmodified["I"][0][1][1] == "#"

    def test_get_char(self):
        piece = Piece(0)
        assert piece.get_char(1, 0) == "."
