import datetime
import json
import time
from os import environ

import requests
from keras.layers import Dense, Flatten
from keras.models import Sequential
from keras.optimizers import adam_v2
from matplotlib import pyplot as plt
from rl.agents.dqn import DQNAgent
# from rl.agents.sarsa import SARSAAgent
from rl.memory import SequentialMemory
from rl.policy import BoltzmannQPolicy

from game import Game

NB_STEPS = 800000

DEVICE = "cpu"  # ["cpu", "gpu_limited", "gpu_unlimited"]

if (DEVICE == "cpu"):
    environ["CUDA_VISIBLE_DEVICES"] = "-1"
elif (DEVICE == "gpu_limited"):
    environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"
elif (DEVICE == "gpu_unlimited"):
    pass


env = Game()
window_length = 1
# print(flatten_space((env.observation_space)).shape)
input_shape = (1,) + (env.observation_space.shape)
# print(input_shape)

# input_shape = (1,) + env.observation_space.shape
nb_actions = env.action_space.n

model = Sequential()
model.add(Flatten(input_shape=input_shape))
model.add(Dense(units=2**6, activation="relu"))
model.add(Dense(units=2**6, activation="relu"))
model.add(Dense(units=2**6, activation="relu"))
model.add(Dense(units=nb_actions, activation="linear"))
# 経験値を蓄積するためのメモリ
# 学習を安定させるために使用
memory = SequentialMemory(limit=50000, window_length=window_length)

# 行動ポリシー
# BoltzmannQPolicyを使用
# EpsGreedyQPolicyと比較して、こちらの方が収束が早かったので採用
policy = BoltzmannQPolicy()

# DQN エージェントの作成
# agent = SARSAAgent(model=model, nb_actions=nb_actions, nb_steps_warmup=10)
agent = DQNAgent(model=model, nb_actions=nb_actions, memory=memory,
                 nb_steps_warmup=10, target_model_update=1e-2, policy=policy, enable_double_dqn=True, batch_size=32)
# DQNAgentのコンパイル
# 最適化はAdam,評価関数はMAEを使用
agent.compile(adam_v2.Adam())

# 学習を開始
time_start = time.time()

history = agent.fit(env, nb_steps=NB_STEPS, visualize=False, verbose=1)
# 学習した重みをファイルに保存
agent.save_weights("moving_I.hdf5", overwrite=True)
# model.save("model_IO")

time_spent = time.time() - time_start
print(datetime.timedelta(seconds=time_spent))

# print(history.history)
# print(history.history.keys())

plt.subplot(2, 1, 1)
plt.plot(history.history["nb_steps"], history.history["nb_episode_steps"])
plt.ylabel("step")

plt.subplot(2, 1, 2)
plt.plot(history.history["nb_steps"], history.history["episode_reward"])
plt.xlabel("episode")
plt.ylabel("reward")

plt.savefig("graph.png", format="png")

WEBHOOK_URL = "https://discord.com/api/webhooks/1015490794603425803/0YIP0jDBiObdMIzvT6NEeYuxekeIAWCj1_ljths_I-l9Ttr2-XVXRNIj5zwAZFTglzi3"

payload = {
    "username": "学習終了",
    "content": f"nb_steps: {NB_STEPS}\nDuration: {datetime.timedelta(seconds=time_spent)}"
}

res = requests.post(WEBHOOK_URL, {"payload_json": json.dumps(
    payload)}, files={"graph.png": open("graph.png", "rb")})
print("res.status_code", res.status_code)
# print(json.dumps(json.loads(res.content), indent=4, ensure_ascii=False))

plt.show()

agent.test(env, nb_episodes=10, visualize=True)
