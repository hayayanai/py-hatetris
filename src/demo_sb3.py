import time

from stable_baselines3 import DQN

from game import GameEnv

env = GameEnv(seed=1)

model = DQN.load("./save_weights_burgiel_256/rl_model_1050000_steps")

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
