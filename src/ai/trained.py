import numpy as np
from stable_baselines3 import DQN

from enemy_env import EnemyEnv
from piece import Piece
from well import Well


class TrainedAi():
    ENEMY_MODEL: DQN = DQN.load(
        "./weights/enemy_1024/rl_model_5000000_steps")

    def __init__(self, field: Well) -> None:
        self.enemy_env: EnemyEnv = EnemyEnv()
        self.field: Well = field

    def get_first_piece(self) -> Piece:
        self.enemy_env.obs = np.array(self.field.get_heights_diff_minus())
        action, _state = TrainedAi.ENEMY_MODEL.predict(self.enemy_env.obs)
        return Piece(int(action))

    def get_next_piece(self) -> Piece:
        self.enemy_env.obs = np.array(self.field.get_heights_diff_minus())
        action, _state = TrainedAi.ENEMY_MODEL.predict(self.enemy_env.obs)
        return Piece(int(action))
