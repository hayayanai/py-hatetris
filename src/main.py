from random import randint
from time import sleep
from Game import Game
from gym.spaces import Box

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
        obs, reward, _, _ = game.step(action_index=int(input()))
        print("reward:", reward)
        game.render()
    else:
        obs, reward, _, _ = game.step(action_index=randint(0, 3))
        print("reward:", reward)
        game.render()
        sleep(0.5)
    # print("obs:", obs)
    # print("age", game.piece.age)
