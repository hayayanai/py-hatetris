from matplotlib import pyplot as plt
from stable_baselines3 import DQN
from tqdm.auto import tqdm

from enemy_env import EnemyEnv


def evaluate(model_name: str, step: int, repeat: int = 1000, verbose: int = 2) -> tuple:
    """evaluate model

    Args:
        model_name (str): saved name
        step (int): valid step
        repeat (int, optional): how many repeat. Defaults to 1000.
        verbose (int, optional): 2 shows progress. Defaults to 2.

    Returns:
        tuple: (sum(lines) / len(lines), max_lines)
    """

    env = EnemyEnv()
    model = DQN.load(f"./weights/{model_name}/rl_model_{step}_steps")

    pieces = []
    lines = []
    mx = -1
    max_replay = []
    max_replay_seed = -1

    for i in tqdm(range(repeat), leave=False):
        obs = env.reset(regenerate=True)
        while True:
            action, _states = model.predict(obs)
            obs, rewards, dones, info = env.step(action)

            if dones:
                if mx < info["total_cleared_line"]:
                    mx = info["total_cleared_line"]
                    max_replay = info["replay"]
                    max_replay_seed = info["seed"]
                pieces.append(info["total_piece"])
                lines.append(info["total_cleared_line"])
                break

    with open("src/replay.py", mode="w") as f:
        f.writelines("from collections import deque\n\n")
        f.writelines(f"seed = {max_replay_seed}\n")
        f.writelines(f"replay = {str(max_replay)}\n")

    return (sum(lines) / len(lines), mx)


def detail_evaluation(model_name: str, total_step: int, repeat: int = 5) -> tuple[list, list]:
    mean_list = [0] * 100
    max_list = [0] * 100
    for i in tqdm(range(1, 100)):
        mean_list[i], max_list[i] = evaluate(model_name, (total_step // 100) * i, repeat, verbose=0)

    with open(f"weights/{model_name}/evaluation.txt", mode="w") as f:
        f.writelines(f"mean: {mean_list}\n")
        f.writelines(f"max: {max_list}\n")
    return mean_list, max_list


def graph(model_name: str, total_step: int):
    x = range(total_step // 100, total_step + 1, total_step // 100)
    mean_list, max_list = detail_evaluation(model_name, total_step)
    plt.subplot(2, 1, 1)
    plt.plot(x, mean_list)
    plt.ylabel("lines")

    plt.subplot(2, 1, 2)
    plt.plot(x, max_list)
    plt.xlabel("steps")
    plt.ylabel("lines")

    plt.savefig(f"weights/{model_name}/graph.png", format="png")


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Evaluate a Stable Baselines3 model")
    parser.add_argument("name", type=str, help="model name")
    parser.add_argument("step", type=int, help="timesteps")
    parser.add_argument("-r", "--repeat", type=int, help="number of repeat", default=1000)
    parser.add_argument("-v", "--verbose", type=int, default=2)
    args = parser.parse_args()
    print(evaluate(args.name, args.step, repeat=args.repeat, verbose=args.verbose))
