import time

from stable_baselines3 import DQN

from game import GameEnv

env = GameEnv(seed=1)

model = DQN.load("./save_weights_seven_256_past/rl_model_2000000_steps")

pieces = []
lines = []
for _ in range(10):
    obs = env.reset()
    while True:
        time.sleep(0.1)
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        env.render()
        if dones:
            break

env.close()
