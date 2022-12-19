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
dt_now = datetime.datetime.now()

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
info["sid"] = sid
info["datetime"] = dt_now.strftime("%Y/%m/%d %H:%M:%S")
info["enemy"] = ENEMY

filename = "experiment.json"

with open(filename, "r") as f:
    data = json.load(f)

data.append(info)

with open(filename, "w") as f:
    json.dump(data, f)
print("SAVED DATA")


print("GAMEOVER")

print("RESULT:")
pprint(info)
