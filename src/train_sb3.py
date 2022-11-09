import datetime
import json
import time
from os import getenv

import requests
from dotenv import load_dotenv
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import CheckpointCallback
from torch.cuda import is_available

from evaluation import evaluate
from game import GameEnv

load_dotenv(override=True)

print("torch.cuda.is_available():", is_available())

# TIMESTEPS = 8_000_000
# BATCH_SIZE = 128
# DEVICE = "cuda"  # ["cpu", "cuda", "auto"]
seed = 20221015

NOTIFICATION = True
webhook_url = getenv("WEBHOOK_URL")

if webhook_url is None and NOTIFICATION:
    print("webhook_url is None")
    exit()


def train(model_name: str, batch_size: int, timesteps: int, device: str = "cuda"):
    env = GameEnv()
    model = DQN("MlpPolicy", env, verbose=1, tensorboard_log="log", device=device, batch_size=batch_size)

    print("START!")
    print(model_name, batch_size, timesteps, device)
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
    print(model_name, ave, mx)

    payload = {
        "username": "学習終了",
        "content": f"{model_name}\ntotal_timesteps: {timesteps}\nDuration: {datetime.timedelta(seconds=time_spent)}\nAverage: {ave}\nMax: {mx}"
    }
    if NOTIFICATION and webhook_url is not None:
        res = requests.post(webhook_url, {"payload_json": json.dumps(payload)})
        print("res.status_code", res.status_code)


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Train with Stable Baselines3")
    parser.add_argument("name", type=str, help="model name")
    parser.add_argument("batch_size", type=int, help="batch size")
    parser.add_argument("step", type=int, help="timesteps")
    parser.add_argument("device", type=str, help="cpu | cuda | auto", default="cuda")
    args = parser.parse_args()
    train(args.name, batch_size=args.batch_size, timesteps=args.step, device=args.device)
