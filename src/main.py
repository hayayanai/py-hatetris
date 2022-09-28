from pprint import pprint
from random import randint
from time import sleep

from gym.spaces import Box

from game import Game
from actions import ACTIONS
manual = False

game = Game()
print(game.action_space)
print(game.observation_space)
print(game.observation_space.sample())
space = game.observation_space
if isinstance(space, Box):
    print('    最小値: ', space.low)
    print('    最大値: ', space.high)

while not game.done:
    if manual:
        obs, reward, _, info = game.step(action_index=int(input()))
        print("reward:", reward)
        pprint(info)
        pprint(game.field.get_column_heights())
        print(game.field.get_holes())
        print(game.field.get_bumpiness())

        game.render()
    else:
        obs, reward, _, info = game.step(action_index=randint(0, len(ACTIONS) - 1))
        print("reward:", reward)
        pprint(info)
        game.render()
        sleep(0.02)
    # print("obs:", obs)
    # print("age", game.piece.age)
