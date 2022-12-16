# from pprint import pprint
from random import randint
from time import sleep

from gym.spaces import Box

from actions import ACTIONS
from game import GameEnv


game = GameEnv(seed=1)

print(game.action_space)
print(game.observation_space)
print(game.observation_space.sample())
space = game.observation_space
if isinstance(space, Box):
    # print('    最小値: ', space.low)
    # print('    最大値: ', space.high)
    pass

while not game.done:
    obs, reward, _, info = game.step(
        action_index=randint(0, len(ACTIONS) - 1))
    print("reward:", reward)
    # pprint(info)
    game.render()
    sleep(0.1)
    print("obs:", obs)
    print("age", game.piece.age)
