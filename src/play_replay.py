# from pprint import pprint
from time import sleep

from gym.spaces import Box

from game import GameEnv


from replay import replay, seed
game = GameEnv(seed=seed, replay=replay)

print(game.action_space)
print(game.observation_space)
print(game.observation_space.sample())
space = game.observation_space
if isinstance(space, Box):
    # print('    最小値: ', space.low)
    # print('    最大値: ', space.high)
    pass

while not game.done:

    obs, reward, _, info = game.step(action_index=None)
    sleep(0.01)
    game.render()
