import time
from collections import deque
from random import randint
from typing import Literal

import numpy as np
from gym import Env
from gym.spaces import Box, Dict, Discrete, flatten_space

from actions import ACTIONS
from ai.burgiel import Burgiel
# from ai.hatetris import HatetrisAi
from ai.lovetris import Lovetris
from ai.rand import RandomAi
from ai.seven import SevenAi
# from ai.trained import TrainedAi  # Avoid circular import
from piece import Piece
# from watch import watch
from well import Well

AIs = [Lovetris, RandomAi, Burgiel, SevenAi]
EnemyAI = SevenAi


class GameEnv(Env):
    piece: Piece
    piece_pos_y: int
    # hold: number;
    field: Well
    frame_count: int
    total_piece: int
    total_cleared_line: int
    landing_height: int
    # rng: int
    # VISIBLE_NEXT: int = 1
    ACTION_MAP = np.array(ACTIONS)
    done: bool
    replay: deque[str] | None
    seed: int

    def __init__(
        self,
        replay: deque[str] | None = None,
        seed: int | None = None,
        save_replay: bool = False
    ) -> None:

        super().__init__()
        self.save_replay: bool = save_replay
        from window import RenderWindow
        self.window: RenderWindow | None = None
        ACTION_NUM = len(self.ACTION_MAP)
        self.action_space = Discrete(ACTION_NUM)
        self.observation_space = self.OBSERVATION_SPACE

        if replay is None:
            self.replay = deque()
        else:
            self.replay = replay

        regenerate: bool
        if seed is None:
            self.seed = randint(0, 2**32 - 1)
            self.replay = deque()
            regenerate = True
        else:
            self.seed = seed
            regenerate = False

        self.frame_count = 0
        self.score = 0.0
        self.total_piece = 0
        self.current_cleard_line = 0
        self.total_cleared_line = 0
        self.landing_height = 0
        self.field = Well()
        self.enemy = EnemyAI(initial_seed=self.seed, field=self.field)
        self.piece = self.enemy.get_first_piece()
        self.piece_pos_y = self.piece.y
        self.gameover = False
        self.done = False
        self.reset(regenerate)

    def reset(self, regenerate: bool = True) -> np.ndarray:
        self.frame_count = 0
        self.score = 0.0
        self.total_piece = 0
        self.current_cleard_line = 0
        self.total_cleared_line = 0
        self.landing_height = 0
        self.field = Well()
        if regenerate:
            self.seed = randint(0, 2**32 - 1)
            self.replay = deque()
        self.enemy = EnemyAI(initial_seed=self.seed, field=self.field)
        self.piece = self.enemy.get_first_piece()
        self.piece_pos_y = self.piece.y
        self.gameover = False
        self.done = False

        return self._get_observation()

    # def seed(self, seed: int):
    #     self.seed = seed
    #     np.random.seed = seed

    def step(self, action_index: int | None) -> tuple[np.ndarray, float, bool, dict]:
        next_frame_count: int = self.frame_count + 1
        og_score = self.score
        # og_piece = self.piece
        # self.score = 0.0
        # is_gameover: bool = False

        action_player = self.ACTION_MAP[action_index]
        if action_index is None:  # Play replay
            self._handle_input(self.replay.popleft(), save=False)
        else:
            if self.save_replay:
                self.replay.append(action_player)
            self._handle_input(action_player)

        observation = self._get_observation()

        self.score = self._calc_score()

        self.frame_count = next_frame_count
        # self.piece.age += 1
        if self.gameover:
            self.score -= 500
            self.done = True
        reward = self.score - og_score
        # reward = self.score

        # if self.gameover:
        #     reward -= 500
        #     self.done = True

        info = {
            # "frame_count": self.frame_count,
            # "c_trans": self.field.get_column_transitions(),
            # "r_trans": self.field.get_row_transitions(),
            "total_piece": self.total_piece,
            "total_cleared_line": self.total_cleared_line,
            "seed": self.seed,
            "replay": self.replay
        }

        return observation, reward, self.done, info

    @property
    def OBSERVATION_SPACE(self):
        OBS_SPACE = Dict({
            # "Aggregate_Height": Box(low=0, high=7 * Well.DEPTH + 3 * 18, dtype=np.uint8),
            # "Bumpiness": Box(low=0, high=(Well.WIDTH - 1) * Well.DEPTH, dtype=np.uint8),
            # "Column_Height": Box(
            #     low=np.zeros(Well.WIDTH),
            #     high=np.full(Well.WIDTH, Well.DEPTH + 1),
            #     dtype=np.uint8
            # ),
            # "Column_Height_Diff": Box(
            #     low=np.zeros(Well.WIDTH - 1),
            #     high=np.full(Well.WIDTH - 1, Well.DEPTH + 1),
            #     dtype=np.uint8
            # ),
            "Column_Height_Diff_Minus": Box(
                low=np.full(Well.WIDTH - 1, -1 * (Well.DEPTH + 1)),
                high=np.full(Well.WIDTH - 1, Well.DEPTH + 1),
                dtype=np.int8
            ),
            # "max_height": Box(low=0, high=20, dtype=np.uint8),
            # "max_height_diff": Box(
            #     low=np.full(Well.WIDTH, -1 * (Well.DEPTH)),
            #     high=np.zeros(Well.WIDTH),
            #     dtype=np.int8
            # ),
            # "max_height_diff_limit": Box(
            #     low=np.full(Well.WIDTH, -3),
            #     high=np.zeros(Well.WIDTH),
            #     dtype=np.int8
            # ),
            # "Column_Height_Diff_Limit": Box(
            #     low=np.full(Well.WIDTH - 1, -3),
            #     high=np.full(Well.WIDTH - 1, 3),
            #     dtype=np.int8
            # ),
            # "Column_Transitions": Box(low=0, high=180, dtype=np.uint8),
            # "Cumulative_Wells": Box(low=0, high=Well.WIDTH * Well.DEPTH, dtype=np.uint8),
            # "Field": Box(
            #     low=np.append(
            #         np.zeros(Well.WIDTH * Well.DEPTH - 1), 0),
            #     high=np.append(
            #         np.ones(Well.WIDTH * Well.DEPTH - 1), 1),
            #     dtype=np.uint8
            # ),
            # "Holes": Box(low=0, high=(Well.WIDTH - 1) * Well.DEPTH, dtype=np.uint8),
            # "Landing_Height": Box(low=0, high=20, dtype=np.uint8),
            # "PieceID1": Box(low=0, high=6, dtype=np.uint8),
            "PieceID2": Discrete(7),
            # "Row_Cleared": Box(low=0, high=4, dtype=np.uint8),
            # "Row_Transitions": Box(low=0, high=180, dtype=np.uint8),

        })
        return flatten_space(OBS_SPACE)

    # @watch
    def _get_observation(self) -> np.ndarray:

        # observation = np.array(self.field.get_column_heights())
        observation = np.array(self.field.get_heights_diff_minus())
        # observation = np.array(self.field.get_max_height())
        # observation = np.append(
        #     observation, self.field.get_max_height_diff())
        # observation = np.array(self.field.get_heights_diff_limit())
        # # observation = np.append(np.array(self.field.get_column_heights()), np.array(self.field.get_cells_1d()))
        # observation = np.array(sum(self.field.get_column_heights()))
        # observation = np.append(observation, np.array(self.field.get_bumpiness()))
        # # observation = np.append(observation, np.array(self.field.get_column_heights()))
        # observation = np.append(observation, self.field.get_column_transitions())
        # observation = np.append(observation, self.field.get_cumulative_wells())
        # # observation = np.append(observation, np.array(self.field.get_cells_1d()))
        # observation = np.append(observation, self.field.get_holes())
        lis = [0] * 7
        lis[self.piece.id] = 1
        # observation = np.append(observation, self.piece.id)
        observation = np.append(observation, np.array(lis))

        # observation = np.append(observation, self.landing_height)
        # observation = np.append(observation, self.current_cleard_line)
        # observation = np.append(observation, self.field.get_row_transitions())

        # return get_possible_state()
        return observation

    def _calc_score(self) -> float | int:
        r = 0
        # # if self.current_cleard_line == 1:
        # #     r += 40
        # # elif self.current_cleard_line == 2:
        # #     r += 100
        # # elif self.current_cleard_line == 3:
        # #     r += 300
        # # elif self.current_cleard_line == 4:
        # #     r += 1200
        # # r += (22 - self.piece.y)
        # # r += (abs(self.piece.x - 3)) * 2
        # # r += np.linalg.norm(np.array([3, 16]) -
        # #                     np.array([self.piece.x, self.piece.y]))
        # r -= (max(self.field.get_column_heights()))
        # # r -= (sum(self.field.get_column_heights()))
        # # r += (self.piece.rot % 2) * 2
        # # r -= self.field.get_holes() * 7
        # r -= self.field.get_holes()
        # r -= self.field.get_bumpiness()
        # # r -= self.field.get_bumpiness() ** 2
        # r -= self.field.get_deviation()
        r += self.current_cleard_line ** 2 * 3
        r += (self.total_cleared_line ** 1.5) * 100
        # # r += self.total_piece
        # # if (self.piece.y == self.piece_pos_y):
        # #     r -= 1
        # # print("r", r)
        # # if self.total_cleared_line > 100:
        # #     self.score += 10000
        # #     self.done = True

        r += -5 * self.field.get_average_height() - 16 * self.field.get_holes() - \
            self.field.get_bumpiness_2d()
        return r

    def _handle_input(self, action: str, save=True) -> None:
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
                    self._handle_input("D", save=False)
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

    # @lru_cache(maxsize=None)
    def _is_piece_movable(self) -> bool:
        move = True
        for y in range(4):
            for x in range(4):
                if self.piece.get_char(x, y) == "#":
                    try:
                        # 頭を抱える。
                        # if (self.field.cellses[y + self.piece.y][x + self.piece.x].landed or x + self.piece.x < 0 or self.piece.y < -1):
                        if (self.field.at(x + self.piece.x, 3 - y + self.piece.y).landed):
                            move = False
                    except IndexError:
                        move = False
                        # print("index")
        return move

    def _lock_piece(self) -> None:
        mx = 0
        for y in range(4):
            for x in range(4):
                if self.piece.get_char(x, y) == "#":
                    try:  # TODO: Refactor
                        self.field.cellses[3 - y + self.piece.y][x +
                                                                 self.piece.x].landed = True
                        if mx < 3 - y + self.piece.y:
                            mx = 3 - y + self.piece.y
                    except IndexError:
                        # print("Error:", y + self.piece.y)
                        # self.gameover = True
                        pass
        self.landing_height = mx
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
            time.sleep(0.01)

        elif mode == "ansi":
            self.field.render_wells()

            print(self.piece)
            print("score", self.score)


if __name__ == "__main__":
    game = GameEnv()
