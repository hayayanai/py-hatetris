from matplotlib import pyplot as plt
from stable_baselines3 import DQN
from tqdm.auto import tqdm

from player_env import PlayerEnv


def evaluate(model_name: str, step: int, repeat: int = 1000, save_replay: bool = True) -> tuple:
    """evaluate model

    Args:
        model_name (str): saved name
        step (int): valid step
        repeat (int, optional): how many repeat. Defaults to 1000.

    Returns:
        tuple: (sum(lines) / len(lines), max_lines)
    """

    env = PlayerEnv(save_replay=True)
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


def evaluate_len(model_name: str, step: int, repeat: int = 100, save_replay: bool = True) -> tuple:
    """evaluate model

    Args:
        model_name (str): saved name
        step (int): valid step
        repeat (int, optional): how many repeat. Defaults to 1000.

    Returns:
        tuple: (sum(lines) / len(lines), max_lines, len)
    """

    env = PlayerEnv(save_replay=True)
    model = DQN.load(f"./weights/{model_name}/rl_model_{step}_steps")

    pieces = []
    lines = []
    mx = -1
    max_replay = []
    max_replay_seed = -1
    t_length = 0
    p_history = {"S": 0, "Z": 0, "O": 0, "I": 0, "L": 0, "J": 0, "T": 0}

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
                t_length += info["frame_count"]
                for n in ["S", "Z", "O", "I", "L", "J", "T"]:
                    p_history[n] += info["replay_piece"].count(n)
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

    return (sum(lines) / len(lines), mx, t_length / repeat, p_history)


def detail_evaluation(model_name: str, total_step: int, repeat: int = 1000) -> tuple[list, list]:
    mean_list = [0] * 100
    max_list = [0] * 100
    for i in tqdm(range(1, 100)):
        mean_list[i], max_list[i] = evaluate(
            model_name, (total_step // 100) * i, repeat, save_replay=False)
    max_idx = max_list.index(max(max_list))
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
    # graph("P_E_P_seven", 10000000)
    print(evaluate_len("P_E_P_hatetris", 10000000))
