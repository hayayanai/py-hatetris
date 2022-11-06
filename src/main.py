from enum import Enum
from pprint import pprint
from random import randint
from time import sleep

from gym.spaces import Box

from actions import ACTIONS
from game import GameEnv


class Mode(Enum):
    MANUAL = 0
    RANDOM = 1
    REPLAY = 2


mode = Mode.REPLAY

if (mode == Mode.REPLAY):
    from replay import replay, seed
    game = GameEnv(seed=seed, replay=replay)
else:
    game = GameEnv(seed=1)

# print(game.action_space)
# print(game.observation_space)
# print(game.observation_space.sample())
space = game.observation_space
if isinstance(space, Box):
    # print('    最小値: ', space.low)
    # print('    最大値: ', space.high)
    pass

while not game.done:

    if mode == Mode.MANUAL:
        obs, reward, _, info = game.step(action_index=int(input()))
        # print("reward:", reward)
        # pprint(info)
        # pprint(obs)
        # pprint(game.field.get_column_heights())
        # print(game.field.get_holes())
        # print(game.field.get_cumulative_wells())
        game.render()

    elif mode == Mode.RANDOM:
        obs, reward, _, info = game.step(action_index=randint(0, len(ACTIONS) - 1))
        print("reward:", reward)
        # pprint(info)
        game.render()
        sleep(0.1)
        print("obs:", obs)
        print("age", game.piece.age)

    elif mode == Mode.REPLAY:
        obs, reward, _, info = game.step(action_index=None)
        sleep(0.1)
        game.render()
