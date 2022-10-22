import datetime
import json
import time
from os import environ

import requests
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import CheckpointCallback

from evaluation import evaluate
from game import Game

# TIMESTEPS = 8_000_000
# BATCH_SIZE = 128
# DEVICE = "cuda"  # ["cpu", "cuda", "auto"]
seed = 20221015

webhook_url = environ.get("WEBHOOK_URL")

if webhook_url is None:
    print("webhook_url is None")
    exit()


def train(model_name: str, batch_size: int = 64, timesteps: int = 8000000, device: str = "cuda"):
    env = Game()
    model = DQN("MlpPolicy", env, verbose=0, tensorboard_log="log", device=device, batch_size=batch_size)

    print("START!")
    time_start = time.time()
    checkpoint_callback = CheckpointCallback(
        save_freq=timesteps // 40, save_path=f"{model_name}/")
    model.learn(total_timesteps=timesteps, callback=checkpoint_callback)
    print("DONE!")

    time_spent = time.time() - time_start

    del model

    print(datetime.timedelta(seconds=time_spent))

    # for i in range(1, 10):
    #     print(evaluate(model_name=model_name, step=i * (timesteps // 10), repeat=1000, verbose=1))

    ave, mx = evaluate(model_name=model_name, step=timesteps, repeat=1000, verbose=1)
    # print(ave, mx)

    payload = {
        "username": "学習終了",
        "content": f"{model_name}\ntotal_timesteps: {timesteps}\nDuration: {datetime.timedelta(seconds=time_spent)}\nAverage: {ave}\nMax: {mx}"
    }

    res = requests.post(webhook_url, {"payload_json": json.dumps(payload)})
    print("res.status_code", res.status_code)


if __name__ == "__main__":
    from multiprocessing import Pool
    args = []
    size = [(64, "cpu"), (128, "cpu"), (256, "cuda"), (512, "cuda")]
    steps = 6000000
    for s in size:
        args.append((f"save_weights_seven_{s[0]}", s[0], steps, s[1]))
    with Pool(4) as p:
        p.starmap(train, args)
