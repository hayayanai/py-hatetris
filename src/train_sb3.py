import datetime
import json
from os import environ
import time

import requests
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import CheckpointCallback

from game import Game

TIMESTEPS = 3_000_000
BATCH_SIZE = 256
DEVICE = "cpu"  # ["cpu", "cuda", "auto"]

env = Game()
model = DQN("MlpPolicy", env, verbose=1, tensorboard_log="log", device=DEVICE, batch_size=BATCH_SIZE)

print("start learning")
time_start = time.time()
checkpoint_callback = CheckpointCallback(
    save_freq=TIMESTEPS // 40, save_path="./save_weights_seven/")
model.learn(total_timesteps=TIMESTEPS, callback=checkpoint_callback)
print("finish learning")
time_spent = time.time() - time_start
print(datetime.timedelta(seconds=time_spent))

WEBHOOK_URL = environ.get("WEBHOOK_URL")

payload = {
    "username": "学習終了",
    "content": f"total_timesteps: {TIMESTEPS}\nDuration: {datetime.timedelta(seconds=time_spent)}"
}

res = requests.post(WEBHOOK_URL, {"payload_json": json.dumps(payload)})
print("res.status_code", res.status_code)

del model
