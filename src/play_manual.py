from pprint import pprint
import json
import datetime
# from gym.spaces import Box

from game_manual import GameEnv

ENEMY = "hate"

game = GameEnv(enemy=ENEMY, save_replay=True)
game.render()

info = {}

sid = input("STUDENT_ID (12k3456): ")
dt = datetime.datetime

info["sid"] = sid
info["datetime"] = dt
info["enemy"] = ENEMY

print("------------ HOW TO CONTROL ------------")
print("1: Left, 2: HardDrop, 3: Right, 4: Rotate(CW)")
print("---------------------------------------------")

while not game.done:
    i = int(input())
    while i < 1 or 4 < i:
        i = int(input())

    obs, reward, _, info = game.step(action_index=i)
    # print("reward:", reward)
    # pprint(obs)
    # pprint(game.field.get_column_heights())
    # print(game.field.get_holes())
    # print(game.field.get_cumulative_wells())
    game.render()

info["replay"] = "".join(list(info["replay"]))

filename = "experiment.json"

with open(filename, "r") as f:
    read_data = json.load(f)

save_data = [read_data, info]

with open(filename, "w") as f:
    json.dump(save_data, f)

print("GAMEOVER")

print("RESULT:")
pprint(info)
