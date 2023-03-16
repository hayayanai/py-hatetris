from pprint import pprint
import json
import datetime
# from gym.spaces import Box
import readchar

from game_manual import GameEnv

ENEMY = ""

info = {}

enemy = input("SELECT ENEMY (s || eps || hate): ")
if enemy == "s":
    ENEMY = "seven"
elif enemy == "eps":
    ENEMY = "E_P_seven2"
elif enemy == "hate":
    ENEMY = "hate"

game = GameEnv(enemy=ENEMY, save_replay=True)

sid = input("STUDENT_ID (12k3456): ")
dt_now = datetime.datetime.now()
skill_level = input("プレイ時間 (0: ~2 hours, 1: 2~10 hours, 2: 10~hours): ")

game.render()

print("------------ HOW TO CONTROL ------------")
print("1: Left, 2: HardDrop, 3: Right, 4: Rotate(CW)")
print("---------------------------------------------")

for i in range(10):
    print(f"GAME {i} / 10")
    game.reset()
    game.render()
    while not game.done:
        i = readchar.readkey()
        while i not in ["1", "2", "3", "4"]:
            i = readchar.readkey()
        i = int(i)
        obs, reward, _, info = game.step(action_index=i)
        # print("reward:", reward)
        # pprint(obs)
        # pprint(game.field.get_column_heights())
        # print(game.field.get_holes())
        # print(game.field.get_cumulative_wells())
        game.render()

    info["replay"] = "".join(list(info["replay"]))
    info["replay_piece"] = "".join(list(info["replay_piece"]))
    info["sid"] = sid
    info["skill"] = skill_level
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
