import time

from stable_baselines3 import DQN

# from player_env import PlayerEnv as GameEnv
from game import GameEnv as GameEnv

env = GameEnv()

model = DQN.load("./weights/Pseven/rl_model_10000000_steps")

pieces = []
lines = []
for _ in range(10):
    obs = env.reset()
    while True:
        time.sleep(0.2)
        action, _states = model.predict(obs)  # _states is None
        obs, rewards, dones, info = env.step(action)
        env.render()
        if dones:
            break

env.close()
