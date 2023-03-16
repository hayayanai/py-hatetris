from matplotlib import pyplot as plt
from stable_baselines3 import DQN
from tqdm.auto import tqdm

from game import GameEnv
import japanize_matplotlib
japanize_matplotlib.japanize()


def evaluate(model_name: str, step: int, repeat: int = 100, save_replay: bool = True) -> tuple:
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


def evaluate_len(model_name: str, step: int, repeat: int = 1000, save_replay: bool = True) -> tuple:
    """evaluate model

    Args:
        model_name (str): saved name
        step (int): valid step
        repeat (int, optional): how many repeat. Defaults to 1000.

    Returns:
        tuple: (sum(lines) / len(lines), max_lines, len)
    """

    env = GameEnv(save_replay=True)
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
    for i in tqdm(range(1, 101)):
        mean_list[i - 1], max_list[i - 1] = evaluate(
            model_name, (total_step // 100) * i, repeat, save_replay=False)
    max_idx = mean_list.index(max(mean_list))
    evaluate(model_name, (total_step // 100) * max_idx, 1000, True)

    with open(f"weights/{model_name}/evaluation1000.txt", mode="w") as f:
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


def graph_average(model_name: str, total_step: int):
    x = range(total_step // 100, total_step + 1, total_step // 100)
    # mean_list, max_list = detail_evaluation(model_name, total_step)
    mean_list = [0.0, 0.0, 0.0, 0.0, 0.001, 0.001, 0.002, 0.002, 0.003, 0.001, 0.005, 0.006, 0.004, 0.019, 0.013, 0.031, 0.035, 0.041, 0.068, 0.1, 0.171, 0.251, 0.321, 0.259, 0.553, 0.614, 1.149, 1.4, 1.198, 2.47, 2.247, 3.716, 1.356, 1.656, 2.516, 1.761, 3.598, 1.189, 0.724, 2.423, 1.827, 0.746, 1.64, 0.259, 0.203, 0.056, 0.025, 0.117, 0.13, 0.045,
                 0.045, 0.115, 0.19, 0.217, 0.202, 0.142, 0.121, 0.13, 0.084, 0.149, 0.278, 0.144, 0.121, 0.184, 0.134, 0.13, 0.21, 0.106, 0.108, 0.083, 0.089, 0.113, 0.111, 0.109, 0.094, 0.106, 0.146, 0.094, 0.09, 0.077, 0.092, 0.113, 0.086, 0.073, 0.052, 0.042, 0.077, 0.058, 0.053, 0.058, 0.041, 0.039, 0.031, 0.049, 0.041, 0.076, 0.07, 0.073, 0.068, 0.076]

    plt.plot(x, mean_list)
    # plt.rcParams['font.family'] = "MS ゴシック"

    plt.xlabel("学習ステップ数")
    plt.ylabel("平均ライン消去数")
    # plt.xlabel("steps")
    # plt.ylabel("score")

    plt.savefig(f"weights/{model_name}/graph_average.pdf", format="pdf")


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Evaluate a Stable Baselines3 model")
    parser.add_argument("name", type=str, help="model name")
    parser.add_argument("step", type=int, help="timesteps")
    parser.add_argument("-r", "--repeat", type=int,
                        help="number of repeat", default=1000)
    parser.add_argument("-v", "--verbose", type=int, default=2)
    args = parser.parse_args()
    # graph_average("P_E_P_E_P_seven", 10000000)
    # print(evaluate(args.name, args.step, repeat=args.repeat, verbose=args.verbose))
    # print(detail_evaluation("save_weights_seven_1024_diff_minus_reward2", 10000000))
    # print(evaluate_len("game_s_seven_nogover",
    #       3200000, save_replay=False, repeat=1000))
    print(evaluate("game_s_seven_nogover", 10000000))
    # print(evaluate("game_seven_row_limit", 9000000, save_replay=False))
# eps2
