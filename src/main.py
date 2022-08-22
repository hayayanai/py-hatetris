from random import randint
from Game import Game


game = Game()
print(game.action_space)

while not game.done:
    # obs, reward, _, _ = game.step(action_index=int(input()))
    obs, reward, _, _ = game.step(action_index=randint(0, 3))

    # print(game.observation_space)
    # print("obs:", obs)
    print("reward:", reward)
    # print(game.frame_count)
    game.render()
