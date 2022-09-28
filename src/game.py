import time
from typing import Literal

import numpy as np
from gym import Env
from gym.spaces import Box, Dict, Discrete, flatten_space

from actions import ACTIONS
from ai.burgiel import Burgiel
from ai.lovetris import Lovetris
from ai.random import RandomAi
from ai.seven import SevenAi
from piece import Piece
from well import Well

AIs = [Lovetris, RandomAi, Burgiel, SevenAi]
EnemyAI = Lovetris


class Game(Env):
    piece: Piece
    piece_pos_y: int
    # hold: number;
    field: Well
    frame_count: int
    total_piece: int
    total_cleared_line: int
    # rng: int
    # VISIBLE_NEXT: int = 1
    # ACTION_MAP = np.array(["L", "R", "D", "U", "H"])
    ACTION_MAP = np.array(ACTIONS)
    done: bool

    def __init__(self) -> None:
        super().__init__()
        from window import RenderWindow
        self.window: RenderWindow | None = None
        # 状態の範囲を定義
        ACTION_NUM = len(self.ACTION_MAP)
        self.action_space = Discrete(ACTION_NUM)
        OBSERVATION_SPACE = Dict({
            "Column_Height": Box(
                low=np.zeros(Well.WIDTH),
                high=np.full(Well.WIDTH, Well.DEPTH + 1),
                dtype=np.uint8
            ),
            "Field": Box(
                low=np.append(
                    np.zeros(Well.WIDTH * Well.DEPTH - 1), 0),
                high=np.append(
                    np.ones(Well.WIDTH * Well.DEPTH - 1), 1),
                dtype=np.uint8
            ),
            "PieceID": Box(low=0, high=6, dtype=np.uint8)
        })

        self.observation_space = flatten_space(OBSERVATION_SPACE)

        self.frame_count = 0
        self.score = 0.0
        self.total_piece = 0
        self.current_cleard_line = 0
        self.total_cleared_line = 0
        self.field = Well()
        self.enemy = EnemyAI()
        self.piece = self.enemy.get_first_piece()
        self.piece_pos_y = self.piece.y
        self.gameover = False
        self.done = False
        self.reset()

    def reset(self) -> np.ndarray:
        self.frame_count = 0
        self.score = 0.0
        self.total_piece = 0
        self.current_cleard_line = 0
        self.total_cleared_line = 0
        self.field = Well()
        self.enemy = EnemyAI()
        self.piece = self.enemy.get_first_piece()
        self.piece_pos_y = self.piece.y
        self.gameover = False
        self.done = False
        # observation = np.array(
        #     [self.piece.id, self.piece.x, self.piece.y, self.piece.rot, sum(self.field.get_cells_1d())])

        observation = np.append(np.array(self.field.get_column_heights()), np.array(self.field.get_cells_1d()))

        # observation = np.array(self.field.get_cells_1d())
        observation = np.append(observation, self.piece.id)
        return observation

    def step(self, action_index: int) -> tuple[np.ndarray, float, bool, dict]:
        next_frame_count: int = self.frame_count + 1
        og_score = self.score
        self.score = 0.0
        # is_gameover: bool = False

        action_player = self.ACTION_MAP[action_index]
        self._handle_input(action_player)

        # observation = self.field, self.piece
        # observation = np.array(
        #     [self.piece.id, self.piece.x, self.piece.y, self.piece.rot, sum(self.field.get_cells_1d())])

        observation = np.append(np.array(
            self.field.get_column_heights()), np.array(self.field.get_cells_1d()))

        # observation = np.array(self.field.get_cells_1d())
        observation = np.append(observation, self.piece.id)

        self.score = self._calc_score()

        # if (self.total_cleared_line >= 10):
        #     self.score += 1000
        #     self.done = True
        # print(observation, self.score, self.done)

        self.frame_count = next_frame_count
        self.piece.age += 1

        reward = self.score - og_score

        info = {
            # "frame_count": self.frame_count,
            "total_piece": self.total_piece,
            "total_cleared_line": self.total_cleared_line
        }

        return observation, reward, self.done, info

    def _calc_score(self) -> float | int:
        r = 0.0
        # r += (22 - self.piece.y)
        # r += (abs(self.piece.x - 3)) * 2
        # r += np.linalg.norm(np.array([3, 19]) -
        #                     np.array([self.piece.x, self.piece.y]))
        r -= (max(self.field.get_column_heights())) ** 1.8
        r -= (sum(self.field.get_column_heights()))
        # r += (self.piece.rot % 2) * 2
        # r -= self.field.get_holes() ** 2
        # r -= self.field.get_bumpiness()
        # r -= self.field.get_bumpiness() ** 2
        # r -= self.field.get_deviation()
        # r += (self.current_cleard_line) ** 2
        r += (self.total_cleared_line) ** 2
        # r += self.total_piece ** 1.5
        # if (self.piece.y == self.piece_pos_y):
        #     r -= 1
        # print("r", r)
        if (self.gameover):
            self.score -= 100
            self.done = True
        return r

    def _handle_input(self, action: str) -> None:
        pre_x = self.piece.x
        pre_y = self.piece.y
        pre_rot = self.piece.rot
        if len(action) == 1:
            if (action == "D"):
                self.piece.y -= 1
            elif (action == "L"):
                self.piece.x -= 1
            elif (action == "R"):
                self.piece.x += 1
            elif (action == "U"):
                self.piece.rot = (self.piece.rot + 1) % 4
            elif (action == "H"):
                obj_id = id(self.piece)
                while obj_id == id(self.piece):
                    self._handle_input("D")
        else:
            self._handle_input(action[0])
            self._handle_input(action[1:])

        if (not self._is_piece_movable()):  # 動かせないなら元に戻す
            self.piece.x = pre_x
            self.piece.rot = pre_rot
            # self.score -= 2
            if (self.piece.y != pre_y):
                self.piece.y = pre_y
                self._lock_piece()
                # self.score += 10

    def _is_piece_movable(self) -> bool:
        move = True
        for y in range(0, 4):
            for x in range(0, 4):
                if (self.piece.get_char(x, y) == "#"):
                    try:
                        # 頭を抱える。
                        # if (self.field.cellses[y + self.piece.y][x + self.piece.x].landed or x + self.piece.x < 0 or self.piece.y < -1):
                        if (self.field.at(x + self.piece.x, y + self.piece.y).landed):
                            move = False
                    except IndexError:
                        move = False
                        # print("index")
        return move

    def _lock_piece(self) -> None:
        for y in range(0, 4):
            for x in range(0, 4):
                if (self.piece.get_char(x, y) == "#"):
                    try:  # TODO: Refactor
                        self.field.cellses[y + self.piece.y][x
                                                             + self.piece.x].landed = True
                    except IndexError:
                        # print("Error:", y + self.piece.y)
                        # self.gameover = True
                        pass

        self.total_piece += 1
        self.current_cleard_line = self.field.delete_lines()
        self.total_cleared_line += self.current_cleard_line
        self.piece = self.get_next_piece()
        self._check_gameover()

    def get_next_piece(self) -> Piece:
        return self.enemy.get_next_piece()

    def _check_gameover(self) -> None:
        if (self._is_piece_movable()):
            pass
            # return False
        else:
            # print("gameover")
            self.gameover = True
            # return True

    def render(self, mode: Literal["human", "rgb_array", "ansi"] = "human") -> None:
        """描画関数
        mode の引数によって以下の変化がある
        | 引数名 | 内容 | 返り値 |
        | ---- | ---- | ---- |
        | human | 人にとって認識しやすいように可視化, 環境をポップアップ画面に表示 | なし |
        | rgb_array | 返り値の生成処理 | shape=(x, y, 3)のndarray |
        | ansi | 返り値の生成処理 | ansi文字列(str)もしくはStringIO.StringIO |
        """
        if mode == "human":
            from window import RenderWindow
            if self.window is None:
                self.window = RenderWindow(self)
            self.window.render()
            self.window.update_idletasks()
            self.window.update()
            time.sleep(0.2)

        elif mode == "ansi":
            self.field.render_wells()

            print(self.piece)
            print("score", self.score)


if __name__ == "__main__":
    game = Game()
