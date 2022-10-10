from stable_baselines3 import DQN

from game import Game

env = Game(save_replay=True)
model = DQN.load("./save_weights_seven/rl_model_3000000_steps")
REPEAT = 100

pieces = []
lines = []
mx = -1
max_replay = []
max_replay_seed = -1

for _ in range(REPEAT):
    obs = env.reset(regenerate=True)
    while True:
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        if dones:
            if mx < info["total_cleared_line"]:
                mx = info["total_cleared_line"]
                max_replay = info["replay"]
                max_replay_seed = info["seed"]
            break

print(mx)
with open("src/replay.py", mode="w") as f:
    f.writelines("from collections import deque\n\n")
    f.writelines(f"seed = {max_replay_seed}\n")
    f.writelines(f"replay = {str(max_replay)}\n")

env.close()
