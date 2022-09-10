import gym.spaces
from keras.layers import Dense, Flatten
from keras.models import Sequential
from keras.optimizers import adam_v2
from rl.agents.dqn import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import BoltzmannQPolicy

from Game import Game

env = Game()
NB_STEPS = 5000000

env = Game()
window_length = 1
print(gym.spaces.flatten_space((env.observation_space)).shape)
input_shape = (1,) + gym.spaces.flatten_space((env.observation_space)).shape
print(input_shape)
nb_actions = env.action_space.n

model = Sequential()
model.add(Flatten(input_shape=input_shape))
model.add(Dense(units=2**8, activation="relu"))
model.add(Dense(units=2**6, activation="relu"))
model.add(Dense(units=2**4, activation="relu"))
model.add(Dense(units=nb_actions, activation="linear"))
model.load_weights("./moving_random_3")
memory = SequentialMemory(limit=50000, window_length=window_length)
policy = BoltzmannQPolicy()
agent = DQNAgent(model=model, nb_actions=nb_actions, memory=memory,
                 nb_steps_warmup=10, target_model_update=1e-2, policy=policy, enable_double_dqn=True, enable_dueling_network=True)
agent.compile(adam_v2.Adam())
agent.test(env, nb_episodes=100, visualize=True)
