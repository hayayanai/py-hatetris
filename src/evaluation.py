from stable_baselines3 import DQN

from game import Game


def evaluate(model_name: str = "save_weights_seven2", step: int = 4000000, repeat: int = 1000, verbose: int = 2) -> tuple:
    env = Game(save_replay=True)
    model = DQN.load(f"./{model_name}/rl_model_{step}_steps")

    pieces = []
    lines = []
    mx = -1
    max_replay = []
    max_replay_seed = -1

    for i in range(repeat):
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
        if verbose == 2:
            print(f"\r{i+1} / {repeat}", end="")
    if verbose == 2:
        print()

    with open("src/replay.py", mode="w") as f:
        f.writelines("from collections import deque\n\n")
        f.writelines(f"seed = {max_replay_seed}\n")
        f.writelines(f"replay = {str(max_replay)}\n")

    return (sum(lines) / len(lines), mx)


if __name__ == "__main__":
    from sys import argv
    if len(argv) > 1:
        print(evaluate(int(argv[1])))
    else:
        print(evaluate(100_0000, repeat=1000))
        print(evaluate(200_0000, repeat=1000))
        print(evaluate(300_0000, repeat=1000))
        print(evaluate(400_0000, repeat=1000))
