from matplotlib import pyplot as plt
from stable_baselines3 import DQN
from tqdm.auto import tqdm

from game import GameEnv


def evaluate(model_name: str, step: int, repeat: int = 1000, save_replay: bool = True) -> tuple:
    """evaluate model

    Args:
        model_name (str): saved name
        step (int): valid step
        repeat (int, optional): how many repeat. Defaults to 1000.

    Returns:
        tuple: (sum(lines) / len(lines), max_lines)
    """

    env = GameEnv(save_replay=True)
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

    if save_replay:
        with open("src/replay.py", mode="w") as f:
            f.writelines("from collections import deque\n\n")
            f.writelines(f"seed = {max_replay_seed}\n")
            f.writelines(f"replay = {str(max_replay)}\n")

        with open(f"./weights/{model_name}/replay.py", mode="w") as f:
            f.writelines(f"# step: {step}\n\n")
            f.writelines("from collections import deque\n\n")
            f.writelines(f"seed = {max_replay_seed}\n")
            f.writelines(f"replay = {str(max_replay)}\n")

        print(f"step: {step}")
        print((sum(lines) / len(lines), mx))

    return (sum(lines) / len(lines), mx)


def detail_evaluation(model_name: str, total_step: int, repeat: int = 400) -> tuple[list, list]:
    mean_list = [0] * 100
    max_list = [0] * 100
    for i in tqdm(range(1, 101)):
        mean_list[i - 1], max_list[i - 1] = evaluate(
            model_name, (total_step // 100) * i, repeat, save_replay=False)
    max_idx = mean_list.index(max(mean_list))
    evaluate(model_name, (total_step // 100) * max_idx, 1000, True)

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
    parser.add_argument("-r", "--repeat", type=int,
                        help="number of repeat", default=1000)
    parser.add_argument("-v", "--verbose", type=int, default=2)
    args = parser.parse_args()
    # print(evaluate(args.name, args.step, repeat=args.repeat, verbose=args.verbose))
    # print(detail_evaluation("save_weights_seven_1024_diff_minus_reward2", 10000000))
    graph("seven_1024_alpha0.001", 10000000)
    # graph("mh_diff", 10000000)
    # graph("mh_diff_limit", 10000000)
