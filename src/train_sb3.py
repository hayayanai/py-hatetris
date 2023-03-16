import datetime
import time
from shutil import copy2

from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.logger import configure
# from torch import compile
from torch.cuda import is_available

from evaluation import detail_evaluation
from game import GameEnv
from notification import send_webhook

print("torch.cuda.is_available():", is_available())

# TIMESTEPS = 8_000_000
# BATCH_SIZE = 128
# DEVICE = "cuda"  # ["cpu", "cuda", "auto"]
seed = 20221015


def train(
    model_name: str,
    batch_size: int,
    timesteps: int,
    exp_fraction: float = 0.3,
    alpha: float = 0.001,
    device: str = "cuda",
    notification: bool = True
) -> None:

    env = GameEnv()
    logger = configure(f"log/{model_name}",
                       ["stdout", "csv", "json", "tensorboard"])
    model = DQN("MlpPolicy", env, verbose=1,
                device=device, batch_size=batch_size, exploration_fraction=exp_fraction, learning_rate=alpha)
    model.set_logger(logger)

    print("START!")
    print(model_name, batch_size, timesteps, device)
    time_start = time.time()
    checkpoint_callback = CheckpointCallback(
        save_freq=timesteps // 100, save_path=f"weights/{model_name}/")
    # model = compile(model)
    model.learn(total_timesteps=timesteps, callback=checkpoint_callback)
    print("DONE!")

    with open(f"weights/{model_name}/config.txt", mode="w") as f:
        f.writelines(
            f"{model_name} {batch_size} {timesteps} {exp_fraction} {device}\n")

    copy2("src/game.py", f"weights/{model_name}/")
    copy2("src/actions.py", f"weights/{model_name}/")

    time_spent = time.time() - time_start

    del model

    print(datetime.timedelta(seconds=time_spent))

    ave, mx = detail_evaluation(model_name, timesteps)
    print(model_name, max(ave), max(mx))

    payload = {
        "username": "学習終了",
        "content": f"{model_name}\ntotal_timesteps: {timesteps}\nDuration: {datetime.timedelta(seconds=time_spent)}\nAverage: {max(ave)}\nMax: {max(mx)}"
    }
    if notification:
        send_webhook(payload)


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Train with Stable Baselines3")
    parser.add_argument("name", type=str, help="model name")
    parser.add_argument("-bs", "--batch_size", type=int,
                        help="batch size", default=1024)
    parser.add_argument("step", type=int, help="timesteps")
    parser.add_argument("-ef", "--exploration_fraction",
                        type=float, default=0.3)
    parser.add_argument("--alpha", type=float,
                        help="leaning_rate", default=0.001)
    parser.add_argument("device", type=str,
                        help="cpu | cuda | auto", default="cuda")
    parser.add_argument("-n", "--notification", type=bool, default=True)
    args = parser.parse_args()

    train(args.name, batch_size=args.batch_size, timesteps=args.step, exp_fraction=args.exploration_fraction, alpha=args.alpha,
          device=args.device, notification=args.notification)
