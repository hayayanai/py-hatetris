from keras.layers import Dense, Flatten
from keras.models import Sequential
from keras.optimizers import adam_v2
from matplotlib import pyplot as plt
from rl.agents.dqn import DQNAgent
from rl.memory import SequentialMemory
from rl.policy import BoltzmannQPolicy

from Game import Game

env = Game()
window_length = 1
print(env.observation_space.shape)
input_shape = (1,) + env.observation_space.shape
nb_actions = env.action_space.n
model = Sequential()

# 基本は以下のようにSequentialは使わずに定義
# c = input_ = Input(input_shape)
# c = Flatten()(c)
# c = Dense(16, activation='relu')(c)
# c = Dense(16, activation='relu')(c)
# c = Dense(16, activation='relu')(c)
# c = Dense(nb_actions, activation='linear')(c)
# model = Model(input_, c)

model.add(Flatten(input_shape=input_shape))
model.add(Dense(units=256, activation="relu"))
model.add(Dense(units=64, activation="relu"))
model.add(Dense(units=16, activation="relu"))
model.add(Dense(units=nb_actions, activation="linear"))
# 経験値を蓄積するためのメモリ
# 学習を安定させるために使用
memory = SequentialMemory(limit=50000, window_length=window_length)
# 行動ポリシー
# BoltzmannQPolicyを使用
# EpsGreedyQPolicyと比較して、こちらの方が収束が早かったので採用
policy = BoltzmannQPolicy()
# DQN エージェントの作成
agent = DQNAgent(model=model, nb_actions=nb_actions, memory=memory,
                 nb_steps_warmup=10, target_model_update=1e-2, policy=policy)
# DQNAgentのコンパイル
# 最適化はAdam,評価関数はMAEを使用
agent.compile(adam_v2.Adam())
# 学習を開始
# 100000ステップ実行

history = agent.fit(env, nb_steps=100000, visualize=False, verbose=1)
# 学習した重みをファイルに保存
agent.save_weights("moving_test.hdf5", overwrite=True)

print(history.history)
print(history.history.keys())

plt.subplot(2, 1, 1)
plt.plot(history.history["nb_episode_steps"])
plt.ylabel("step")

plt.subplot(2, 1, 2)
plt.plot(history.history["episode_reward"])
plt.xlabel("episode")
plt.ylabel("reward")

plt.show()

i = input()

agent.test(env, nb_episodes=1, visualize=True)
