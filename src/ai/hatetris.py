from copy import deepcopy

from actions import ACTIONS
from piece import Mino, Piece
from well import Well

from ai.enemy import EnemyAi

from hate import Hate

class HatetrisAi(EnemyAi):
    # 'SZOILJT'
    # ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
    WORST_PIECES = [4, 6, 3, 0, 2, 1, 5]

    def __init__(self, field: Well, initial_seed: None = None) -> None:
        super().__init__(field=field)
        self.hate = Hate(field.get_cells_2d())
        self.piece = self.get_first_piece()

    def get_first_piece(self) -> Piece:
        return Piece(Mino.S)

    from watch import watch
    @watch
    def get_next_piece(self) -> Piece:
        # next_piece = self._get_hatetris()
        # return self._get_hatetris()
        # next_piece_id =
        # return Piece(self.hate.get_next_piece())

    def _get_hatetris(self) -> Piece:
        ratings = {}
        for pid in range(7):
            ratings[pid] = 25

        for pid in range(7):
            for action in ACTIONS:
                if not action.endswith("H"):
                    continue
                future_field = deepcopy(self.field)
                # ブロックを置く
                future_field = self._put_block(future_field, action, pid)
                # 最良（盤面の高さが低い）置き方をスコアとする。
                rating = self._evaluate(future_field)
                if ratings[pid] > rating:  # 小さかったら辞書を更新
                    ratings[pid] = rating

        # 辞書の値を探索して、最大なpidを返す。
        pids = []
        mx_v = -1
        for k, v in ratings.items():
            if v > mx_v:
                mx_v = v
                pids = [k]
            elif v == mx_v:
                pids.append(k)
        for p in HatetrisAi.WORST_PIECES:
            for pid in pids:
                if p == pid:
                    return Piece(p)

    def _put_block(self, field: Well, action: str, piece_id: int) -> Well:
        """Put Block

        Args:
            field (Well): field
            action (str): action
            piece_id (int): 0~6

        Returns:
            Well: field (same address)
        """
        piece = Piece(piece_id)
        field = self._handle_input(field, action, piece)
        return field

    def _evaluate(self, field: Well) -> int:
        return max(field.get_column_heights())

    def _handle_input(self, field: Well, action: str, piece: Piece) -> Well:
        pre_x = piece.x
        pre_y = piece.y
        pre_rot = piece.rot
        if len(action) == 1:
            if (action == "D"):
                piece.y -= 1
            elif (action == "L"):
                piece.x -= 1
            elif (action == "R"):
                piece.x += 1
            elif (action == "U"):
                piece.rot = (piece.rot + 1) % 4
            elif (action == "H"):
                while piece.id != -1:
                    self._handle_input(field=field, action="D", piece=piece)

            if not self._is_piece_movable(piece, field) and (piece.id != -1):  # 動かせないなら元に戻す
                piece.x = pre_x
                piece.rot = pre_rot
                if (piece.y != pre_y):
                    piece.y = pre_y
                    field = self._lock_piece(piece, field)
        else:
            self._handle_input(field=field, action=action[0], piece=piece)
            self._handle_input(field=field, action=action[1:], piece=piece)

        return field

    def _is_piece_movable(self, piece: Piece, field: Well) -> bool:
        for y in range(4):
            for x in range(4):
                if piece.get_char(x, y) == "#":
                    try:
                        if (field.at(x + piece.x, 3 - y + piece.y).landed):
                            return False
                    except IndexError:
                        return False
        return True

    def _lock_piece(self, piece: Piece, field: Well) -> Well:
        for y in range(4):
            for x in range(4):
                if piece.get_char(x, y) == "#":
                    try:  # TODO: Refactor
                        field.cellses[3 - y + piece.y][x +
                                                       piece.x].landed = True
                    except IndexError:
                        pass
        _ = field.delete_lines()
        piece.id = -1
        return field


if __name__ == "__main__":
    field = Well()
    ai = HatetrisAi(field)
    print(ai.get_next_piece())
    board_blueprint = [
        "          ",
        "          ",
        "          ",
        "          ",
        "          ",
        "          ",
        "          ",
        "          ",
        "          ",
        "          ",
        "   ##     ",
        "   ##    #",
        "   ##    #",
        "   ###   #",
        "# ##### ##",
        "# ### # ##",
        "# ########",
        "# ####### ",
        "#### #####",
        " ####   ##",
        " #########",
        " #########",
        " #########",
    ]
    lis = [[None] * Well.WIDTH for _ in range(Well.DEPTH)]
    board_blueprint.reverse()
    for y in range(len(board_blueprint)):
        for x in range(Well.WIDTH):
            lis[y][x] = 1 if board_blueprint[y][x] == "#" else 0
    h = Hate(lis)
    # p = Blocks()
    # print(h.getFirstPiece())
    # print(h.getNextPiece())
    # h.print()
    # print(p.print_piece())
