# 実験データの分析をする雑なコード

s = ""
# for dic in lis:
#     if dic["sid"] == "0112":
#         s.append(dic)
# for dic in lis:
#     if dic["enemy"] == "hate":
#         s.append(dic)
# for dic in lis4:
#     if (dic["enemy"] == "E_P_seven2"):
#         s += dic["replay_piece"]
# for dic in lis5:
#     if (dic["enemy"] == "E_P_seven2"):
#         s += dic["replay_piece"]
# for dic in lis6:
#     if (dic["enemy"] == "E_P_seven2"):
#         s += dic["replay_piece"]
# pprint.pprint(s)
# t = 0
# for ss in s:
#     print(ss["total_cleared_line"])
#     if ss["total_cleared_line"] > 100:
#         t += 100
#     else:
#         t += ss["total_cleared_line"]
# print(t/10)


def my_round(val, digit=0):
    p = 10 ** digit
    return (val * p * 2 + 1) // 2 / p


p_history = {"S": 0, "Z": 0, "O": 0, "I": 0, "L": 0, "J": 0, "T": 0}

for n in ["S", "Z", "O", "I", "L", "J", "T"]:
    p_history[n] += s.count(n)
print(p_history.values())
print(sum(p_history.values()))
ans = []
for ele in p_history.values():
    f = ele * 100 / sum(p_history.values())
    ans.append(my_round(f, 3))
print(ans)

# for dic in lis:
#     seed = dic["seed"]
#     l = dic["replay"].split("H")
#     nl = []
#     for ele in l:
#         nl.append(ele + "H")
#     # print(nl)
#     replay = deque(nl)

#     game = GameEnv(enemy="E_P_seven2", seed=seed,
#                    replay=replay, save_replay=True)

#     while True:
#         obs, reward, _, info = game.step(action_index=None)
#         if game.done:
#             print(info["replay_piece"])
#             break
