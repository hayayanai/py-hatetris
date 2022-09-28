import sys
import time

from stable_baselines3 import DQN

from game import Game

env = Game()
if len(sys.argv) > 1:
    args = sys.argv
    model = DQN.load(f"./save_weights_I/rl_model_{args[1]}_steps")
else:
    model = DQN.load(
        "./save_weights_I2/rl_model_2000000_steps")

# 10回試行する
for i in range(10):
    obs = env.reset()
    for j in range(2000):
        time.sleep(0.001)
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        env.render()
        if dones:
            break
env.close()
