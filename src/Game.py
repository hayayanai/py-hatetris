from dataclasses import dataclass
import pprint
from typing import Literal
import gym
from gym import spaces
import numpy as np

from Piece import Piece


@dataclass
class Cell:
    landed: bool
    live: bool


class Well:
    cellses: list[list[Cell]]
    wellDepth: int
    wellWidth: int

    def __init__(self) -> None:
        self.cellses: list[list[Cell]] = []

        self.wellDepth = 20
        self.wellWidth = 10
        for y in range(0, self.wellDepth):
            cells = []
            for x in range(0, self.wellWidth):
                # landed = (well is not None) and (well[y] & (1 << x)) != 0

                # live: bool
                # if (piece is None):
                #     live = False
                # else:
                #     orientation: Orientation = rotationSystem.rotations[piece.id][piece.o]
                #     y2 = y - piece.y - orientation.yMin
                #     x2 = x - piece.x - orientation.xMin
                #     live = (y2 >= 0 and y2 < orientation.yDim and x2 >= 0 and x2 <
                #             orientation.xDim and (orientation.rows[y2] & (1 << x2)) != 0)

                cells.append(Cell(landed=False, live=False))
            self.cellses.append(cells)

    def renderWells(self):
        for y in range(0, self.wellDepth):
            for x in range(0, self.wellWidth):
                if (self.cellses[y][x].landed):
                    print("■", end="")
                else:
                    print("□", end="")
            print()


class Game(gym.Env):
    piece: Piece
    piece_pos_y: int
    # hold: number;
    field: Well
    frame_count: int
    # rng: int
    VISIBLE_NEXT: int = 1
    ACTION_MAP = np.array(["L", "R", "D", "U"])
    done: bool

    def __init__(self) -> None:
        super().__init__()
        self.frame_count = 0
        self.score = 0.0

        # 状態の範囲を定義
        ACTION_NUM = len(self.ACTION_MAP)
        self.action_space = spaces.Discrete(ACTION_NUM)

        # LOW = np.array([np.float32(0)])
        # HIGH = np.array([np.float32(ACTION_NUM - 1)])
        # self.observation_space = gym.spaces.Box(
        #     low=LOW, high=HIGH)
        self.observation_space = spaces.Box(
            low=np.array([0, 0]), high=np.array([10-1, 20-1]))
        # self.observation_space = spaces.Tuple(
        #     spaces.Discrete(10), spaces.Discrete(20))
        # self.observation_space = spaces.Box
        size = 10*20
        # -int(-np.log(2**(4*8)*4*4*9*5)/np.log(2))
        # self.observation_space.shape = np.zeros(size, dtype=int)

        # spaces.Discrete((2**(4*8))*4*4*9*5) # 4x8 board [filled or not], 4*9 active-shape locations, 4 rotation positions, 5 shape types

        # #(np.zeros(2**(4*8)), np.zeros(4*9), np.zeros(4), np.zeros(5))
        self.field = Well()

        self.piece = Piece()
        self.piece_pos_y = self.piece.y

        # self.field.renderWells()
        self.done = False

        self.reset()

    def step(self, action_index: int) -> tuple[dict, float, bool, dict]:
        next_frame_count: int = self.frame_count + 1
        og_score = self.score
        self.score: float = 0.0
        # is_gameover: bool = False

        action_player = self.ACTION_MAP[action_index]
        self.piece.handle_input(action_player)

        # observation = self.field, self.piece
        observation = np.array([self.piece.x, self.piece.y])

        # observation = np.array([np.arctan2(self.piece.x, self.piece.y)])

        self.score = self._calc_score()

        if (self.piece.y <= 1):
            self.score += 10000
            self.done = True
            # print(observation, self.score, self.done)
        if (self.frame_count > 900):
            self.done = True
            self.score -= 1000

        self.frame_count = next_frame_count

        reward = self.score - og_score

        return observation, reward, self.done, {}

    def _calc_score(self) -> float:
        r = 0.0
        r -= self.piece.y * 10
        r += self.frame_count * -1
        # if (self.piece.y == self.piece_pos_y):
        #     r -= 1
        return r

    def reset(self):
        self.frame_count = 0
        self.score = 0.0
        self.field = Well()
        self.piece = Piece(0)
        self.piece_pos_y = self.piece.y
        self.done = False
        observation = np.array([self.piece.x, self.piece.y])

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
            # self.field.renderWells()
            print(self.piece, self.frame_count)

            pass


# game = Game()
# print(game.render())
