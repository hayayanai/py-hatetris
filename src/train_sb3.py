import datetime
import time

from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import CheckpointCallback

from game import Game

TIMESTEPS = 2_000_000

env = Game()
model = DQN("MlpPolicy", env, verbose=1, tensorboard_log="log", device="auto", batch_size=128)

print("start learning")
time_start = time.time()
checkpoint_callback = CheckpointCallback(
    save_freq=TIMESTEPS // 10, save_path="./save_weights_I2/")
model.learn(total_timesteps=TIMESTEPS, callback=checkpoint_callback)
print("finish learning")
time_spent = time.time() - time_start
print(datetime.timedelta(seconds=time_spent))

del model
