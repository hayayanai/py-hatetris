# import type {CoreState
#              import EnemyAi} from '../components/Game/Game.jsx'
# /*
# This is an implementation of the algorithm proposed by Heidi Burgiel in her 1997 paper
# "How To Lose At Tetris"
# <https: // citeseerx.ist.psu.edu/viewdoc/download?doi = 10.1.1.55.8562 & rep = rep1 & type = pdf > .

# """
#     The Tetris game consisting of only Z-tetrominoes alternating orientation will always end
#     before 70,000 tetrominoes have been played.
#   """

# Here "Z-tetromino" is a generic term for S and Z pieces, where a "left-handed Z-tetromino" is a
# Z piece and a "right-handed Z tetromino" is an S piece.

# Burgiel's paper proves that this AI eventually defeats the player before 70, 000 pieces have been
# played(i.e. before 28, 000 lines have been made), regardless of what actions the player takes
# and despite the fact that the AI pays no attention to the current state of the well when deciding
# which piece to send next.
# */

from piece import Piece

from ai.enemy import EnemyAi


class Burgiel(EnemyAi):
    def __init__(self) -> None:
        super().__init__()
        self.current_piece: int = 4

    def get_first_piece(self) -> Piece:
        return Piece(4)

    def get_next_piece(self) -> Piece:
        return Piece(6 if self.current_piece == 4 else 6)
