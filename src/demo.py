from keras.models import Sequential
from keras.layers import Dense, Flatten
from Game import Game
from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory
from keras.optimizers import adam_v2

env = Game()
window_length = 1
input_shape = (window_length,) + env.observation_space.shape
nb_actions = env.action_space.n
model = Sequential()
model.add(Flatten(input_shape=input_shape))
model.add(Dense(units=16, activation="relu"))
model.add(Dense(units=16, activation="relu"))
model.add(Dense(units=16, activation="relu"))
model.add(Dense(units=nb_actions, activation="linear"))
model.load_weights("./moving_test.hdf5")
memory = SequentialMemory(limit=50000, window_length=window_length)
policy = BoltzmannQPolicy()
agent = DQNAgent(model=model, nb_actions=nb_actions, memory=memory,
                 nb_steps_warmup=10, target_model_update=1e-2, policy=policy)
agent.compile(adam_v2.Adam())
agent.test(env, nb_episodes=1, visualize=True)
