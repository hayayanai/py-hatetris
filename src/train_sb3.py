import datetime
import json
import time
from os import environ

import requests
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import CheckpointCallback

from evaluation import evaluate
from game import Game

TIMESTEPS = 4_000_000
BATCH_SIZE = 256
DEVICE = "cuda"  # ["cpu", "cuda", "auto"]

env = Game()
model = DQN("MlpPolicy", env, verbose=1, tensorboard_log="log", device=DEVICE, batch_size=BATCH_SIZE)

print("START!")
time_start = time.time()
checkpoint_callback = CheckpointCallback(
    save_freq=TIMESTEPS // 40, save_path="./save_weights_seven2/")
model.learn(total_timesteps=TIMESTEPS, callback=checkpoint_callback)
print("DONE!")

time_spent = time.time() - time_start

del model

print(datetime.timedelta(seconds=time_spent))

WEBHOOK_URL = environ.get("WEBHOOK_URL")

ave, mx = evaluate()

payload = {
    "username": "学習終了",
    "content": f"total_timesteps: {TIMESTEPS}\nDuration: {datetime.timedelta(seconds=time_spent)}\nAverage: {ave}\nMax: {mx}"
}

res = requests.post(WEBHOOK_URL, {"payload_json": json.dumps(payload)})
print("res.status_code", res.status_code)
