from stable_baselines3 import DQN

from game import GameEnv


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

    env = GameEnv(save_replay=True)
    model = DQN.load(f"./weights/{model_name}/rl_model_{step}_steps")

    pieces = []
    lines = []
    mx = -1
    max_replay = []
    max_replay_seed = -1
    # mx_r_trans = 0
    # mx_c_trans = 0
    # mi_r_trans = 0
    # mi_c_trans = 0
    for i in range(repeat):
        obs = env.reset(regenerate=True)
        while True:
            action, _states = model.predict(obs)
            obs, rewards, dones, info = env.step(action)
            # mx_r_trans = max(mx_r_trans, info["r_trans"])
            # mx_c_trans = max(mx_c_trans, info["c_trans"])
            # mi_r_trans = min(mi_r_trans, info["r_trans"])
            # mi_c_trans = min(mi_c_trans, info["c_trans"])

            if dones:
                if mx < info["total_cleared_line"]:
                    mx = info["total_cleared_line"]
                    max_replay = info["replay"]
                    max_replay_seed = info["seed"]
                pieces.append(info["total_piece"])
                lines.append(info["total_cleared_line"])
                break
        if verbose == 2:
            print(f"\r{i+1} / {repeat}", end="")
    if verbose == 2:
        print()
    # print("rm, cm", mx_r_trans, mx_c_trans)
    # print("rm, cm", mi_r_trans, mi_c_trans)

    with open("src/replay.py", mode="w") as f:
        f.writelines("from collections import deque\n\n")
        f.writelines(f"seed = {max_replay_seed}\n")
        f.writelines(f"replay = {str(max_replay)}\n")

    return (sum(lines) / len(lines), mx)


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Evaluate a Stable Baselines3 model")
    parser.add_argument("name", type=str, help="model name")
    parser.add_argument("step", type=int, help="timesteps")
    parser.add_argument("-r", "--repeat", type=int, help="number of repeat", default=1000)
    parser.add_argument("-v", "--verbose", type=int, default=2)
    args = parser.parse_args()
    print(evaluate(args.name, args.step, repeat=args.repeat, verbose=args.verbose))
