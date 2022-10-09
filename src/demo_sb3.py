import time

from stable_baselines3 import DQN

from game import Game

env = Game(seed=1)

model = DQN.load("./save_weights_seven/rl_model_3000000_steps")

pieces = []
lines = []
for _ in range(10):
    obs = env.reset()
    while True:
        time.sleep(0.5)
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        env.render()
        if dones:
            break

env.close()
