import time

from stable_baselines3 import DQN

from game import GameEnv

env = GameEnv()

model = DQN.load("./save_weights_hate_1024_diff_minus/rl_model_650000_steps")

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
