import pprint
import sys
from typing import Literal
import gym
from gym import spaces
import numpy as np

from Piece import Piece
from Well import Well


class Game(gym.Env):
    piece: Piece
    piece_pos_y: int
    # hold: number;
    field: Well
    frame_count: int
    total_piece: int
    # rng: int
    VISIBLE_NEXT: int = 1
    ACTION_MAP = np.array(["L", "R", "D", "U"])
    done: bool

    def __init__(self) -> None:
        super().__init__()

        # 状態の範囲を定義
        ACTION_NUM = len(self.ACTION_MAP)
        self.action_space = spaces.Discrete(ACTION_NUM)

        # LOW = np.array([np.float32(0)])
        # HIGH = np.array([np.float32(ACTION_NUM - 1)])
        # self.observation_space = gym.spaces.Box(
        #     low=LOW, high=HIGH)
        self.observation_space = spaces.Box(
            low=np.array([-2, 0, 0]), high=np.array([Well.wellWidth - 1, 19, 23 * Well.wellWidth - 1]))
        # self.observation_space = spaces.Tuple(
        #     (spaces.Discrete(2**(10*23)), spaces.Discrete(10*20)))
        # self.observation_space = spaces.Box
        # size = 10*20
        # -int(-np.log(2**(4*8)*4*4*9*5)/np.log(2))
        # self.observation_space.shape = np.zeros(size, dtype=int)

        # spaces.Discrete((2**(4*8))*4*4*9*5) # 4x8 board [filled or not], 4*9 active-shape locations, 4 rotation positions, 5 shape types

        # #(np.zeros(2**(4*8)), np.zeros(4*9), np.zeros(4), np.zeros(5))
        self.frame_count = 0
        self.score = 0.0
        self.total_piece = 0
        self.field = Well()
        self.piece = Piece(0)
        self.piece_pos_y = self.piece.y
        self.gameover = False
        self.done = False

        self.reset()

    def step(self, action_index: int) -> tuple[dict, float, bool, dict]:
        next_frame_count: int = self.frame_count + 1
        og_score = self.score
        self.score = 0.0
        # is_gameover: bool = False

        action_player = self.ACTION_MAP[action_index]
        self._handle_input(action_player)

        # observation = self.field, self.piece
        observation = np.array(
            [self.piece.x, self.piece.y, sum(self.field.getcells1D())])

        # observation = np.array([np.arctan2(self.piece.x, self.piece.y)])

        self.score = self._calc_score()

        if (self.total_piece >= 10):
            self.score += 1000
            self.done = True
            # print(observation, self.score, self.done)
        # if (self.piece.age > 50):
        #     self.gameover = True

        if (self.gameover):
            self.score -= 1000
            self.done = True

        self.frame_count = next_frame_count
        self.piece.age += 1

        reward = self.score - og_score

        return observation, reward, self.done, {}

    def _calc_score(self) -> float:
        r = 0.0
        r += (22 - self.piece.y)
        r += (abs(self.piece.x - 3))
        # r += np.linalg.norm(np.array([3, 19]) -
        #                     np.array([self.piece.x, self.piece.y]))
        r += (self.total_piece * 10)
        # r -= self.piece.age
        # if (self.piece.y == self.piece_pos_y):
        #     r -= 1
        # print("r", r)
        return r

    def _handle_input(self, action: str) -> None:
        pre_x = self.piece.x
        pre_y = self.piece.y
        if (action == "D"):
            self.piece.y -= 1
        elif (action == "L"):
            self.piece.x -= 1
        elif (action == "R"):
            self.piece.x += 1
        elif (action == "U"):
            self.piece.y -= 1
            # self.score -= 1
            pass

        if (not self._is_piece_movable()):  # 動かせないなら元に戻す
            self.piece.x = pre_x
            self.score -= 1
            if (self.piece.y != pre_y):
                self.piece.y = pre_y
                self._lock_piece()
                self.score += 10

    def _is_piece_movable(self) -> bool:
        # wellDepth = 20
        # wellWidth = 10
        move = True
        for y in range(0, 4):
            for x in range(0, 4):
                if (self.piece.unmodified[self.piece.name][1][y][x] == "#"):
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
                if (self.piece.unmodified[self.piece.name][1][y][x] == "#"):
                    try:  # TODO: Refactor
                        self.field.cellses[y + self.piece.y][x +
                                                             self.piece.x].landed = True
                    except IndexError:
                        # print("Error:", y + self.piece.y)
                        # self.gameover = True
                        pass

        self.total_piece += 1
        self.piece = self.get_next_piece()
        self._check_gameover()

    def get_next_piece(self) -> Piece:
        return Piece(0)

    def _check_gameover(self) -> None:
        if (self._is_piece_movable()):
            pass
            # return False
        else:
            # print("gameover")
            self.gameover = True
            # return True

    def reset(self) -> np.ndarray:
        self.frame_count = 0
        self.score = 0.0
        self.total_piece = 0
        self.field = Well()
        self.piece = Piece(0)
        self.piece_pos_y = self.piece.y
        self.gameover = False
        self.done = False
        observation = np.array(
            [self.piece.x, self.piece.y, sum(self.field.getcells1D())])

        # observation = np.array([np.arctan2(self.piece.x, self.piece.y)])
        return observation

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
            self.field.renderWells()
            print(self.piece, self.frame_count)
            print("total_piece", self.total_piece)
            print("score", self.score)

            pass


# if __name__ == "__main__":
#     game = Game()

#     game.field.cellses[0][3].landed = True
#     game.field.cellses[0][4].landed = True
#     game.field.cellses[0][5].landed = True

#     while True:
#         game.field.renderWells()
#         obs, reward, _, _ = game.step(action_index=int(input()))
#         print(game.piece)
