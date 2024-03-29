import numpy as np
from gym import Env
from gym.spaces import Box, Dict, Discrete, flatten_space
from stable_baselines3 import DQN

from game import GameEnv
from well import Well


class EnemyEnvBefore(Env):
    ACTION_MAP = np.array([0, 1, 2, 3, 4, 5, 6])
    PLAYER_MODEL: DQN = DQN.load(
        "./weights/P_E_P_E_P_seven/rl_model_10000000_steps")

    def __init__(self) -> None:
        super().__init__()
        ACTION_NUM = len(EnemyEnv.ACTION_MAP)
        self.action_space = Discrete(ACTION_NUM)
        self.observation_space = self.OBSERVATION_SPACE

        self.player_env: GameEnv = GameEnv()
        self.obs = None
        self.total_lines: int = 0
        self.score: int | float = 0
        self.done: bool = False
        self.reset()

    def reset(self) -> np.ndarray:
        self.obs = self.player_env.reset()
        self.score = 0
        self.total_lines: int = 0
        self.done = False
        return self.get_observation()

    def step(self, action_index: int) -> tuple[np.ndarray, float, bool, dict]:
        # og_score = self.score
        self.player_env.piece.id = action_index
        action, _state = EnemyEnv.PLAYER_MODEL.predict(self.obs)
        self.obs, rewards, dones, info = self.player_env.step(action)
        # self.score = -1 * rewards + int(dones) * 500 - self.player_env.frame_count * 10
        self.score = -1 * rewards
        self.done = dones
        r = self.score

        info = {
            "frame_count": self.player_env.frame_count,
            "total_piece": self.player_env.total_piece,
            "total_cleared_line": self.player_env.total_cleared_line,
            "seed": self.player_env.seed,
            "replay": self.player_env.replay,
        }
        return self.get_observation(), r, self.done, info

    @property
    def OBSERVATION_SPACE(self):
        OBS_SPACE = Dict({
            # "Column_Height_Diff_Minus": Box(
            #     low=np.full(Well.WIDTH - 1, -1 * (Well.DEPTH + 1)),
            #     high=np.full(Well.WIDTH - 1, Well.DEPTH + 1),
            #     dtype=np.int8
            # ),
            "Column_Height_Diff_Limit": Box(
                low=np.full(Well.WIDTH - 1, -3),
                high=np.full(Well.WIDTH - 1, 3),
                dtype=np.int8
            ),
        })
        return flatten_space(OBS_SPACE)

    def get_observation(self) -> np.ndarray:
        return np.array(self.player_env.field.get_heights_diff_limit())

    def render(self, mode="human") -> None:
        if (mode == "human"):
            self.player_env.render()


class EnemyEnv(Env):
    ACTION_MAP = np.array([0, 1, 2, 3, 4, 5, 6])
    PLAYER_MODEL: DQN = DQN.load(
        "./weights/Pseven/rl_model_1000000_steps")

    def __init__(self) -> None:
        super().__init__()
        ACTION_NUM = len(EnemyEnv.ACTION_MAP)
        self.action_space = Discrete(ACTION_NUM)
        self.observation_space = self.OBSERVATION_SPACE

        self.player_env: GameEnv = GameEnv()
        self.obs = None
        self.total_lines: int = 0
        self.score: int | float = 0
        self.done: bool = False
        self.reset()

    def reset(self) -> np.ndarray:
        self.obs = self.player_env.reset()
        self.score = 0
        self.total_lines: int = 0
        self.done = False
        return self.get_observation()

    def step(self, action_index: int) -> tuple[np.ndarray, float, bool, dict]:
        # og_score = self.score
        self.player_env.piece.id = action_index
        action, _state = EnemyEnv.PLAYER_MODEL.predict(self.obs)
        self.obs, rewards, dones, info = self.player_env.step(action)
        # self.score = -1 * rewards + int(dones) * 500 - self.player_env.frame_count * 10
        self.score = -1 * rewards
        self.done = dones
        r = self.score

        info = {
            "frame_count": self.player_env.frame_count,
            "total_piece": self.player_env.total_piece,
            "total_cleared_line": self.player_env.total_cleared_line,
            "seed": self.player_env.seed,
            "replay": self.player_env.replay,
        }
        return self.get_observation(), r, self.done, info

    @property
    def OBSERVATION_SPACE(self):
        OBS_SPACE = Dict({
            # "Column_Height_Diff_Minus": Box(
            #     low=np.full(Well.WIDTH - 1, -1 * (Well.DEPTH + 1)),
            #     high=np.full(Well.WIDTH - 1, Well.DEPTH + 1),
            #     dtype=np.int8
            # ),
            "Column_Height_Diff_Limit": Box(
                low=np.full(Well.WIDTH - 1, -3),
                high=np.full(Well.WIDTH - 1, 3),
                dtype=np.int8
            ),
            "Row_Cleared": Box(low=0, high=4, dtype=np.uint8),
        })
        return flatten_space(OBS_SPACE)

    def get_observation(self) -> np.ndarray:
        observation = np.array(self.player_env.field.get_heights_diff_limit())
        observation = np.append(
            observation, self.player_env.current_cleard_line)
        return observation

    def render(self, mode="human") -> None:
        if (mode == "human"):
            self.player_env.render()
