# py-hatetris

HATETRIS (HardDrop only) impl in Python>=3.10 and C++

- [py-hatetris](#py-hatetris)
  - [Make a virtual environment](#make-a-virtual-environment)
    - [For Ubuntu](#for-ubuntu)
    - [For powershell](#for-powershell)
    - [For Docker](#for-docker)
  - [Train](#train)
    - [Setup HatetrisAI](#setup-hatetrisai)
    - [Enable Discord WebHook notification](#enable-discord-webhook-notification)
  - [Logging on Tensorboard](#logging-on-tensorboard)
  - [EnemyAI vs Human](#enemyai-vs-human)
  - [Evaluation PlayerAI vs EnemyAI](#evaluation-playerai-vs-enemyai)
  - [Play demo](#play-demo)
  - [Play replay](#play-replay)

## Make a virtual environment

- Dependency bug: https://github.com/openai/gym/issues/3176
- pip freeze -> 

### For Ubuntu

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -U setuptools==65.5.0
pip install -r requirements/dev.txt
pip install --force-reinstall "gym~=0.26"

deactivate # exit
```

### For powershell

```ps1
.\.venv\Scripts\Activate.ps1
python -m pip install -U setuptools==65.5.0
python -m pip install -r requirements/dev.txt
python -m pip install --force-reinstall "gym~=0.26"
```

### For Docker

- On WSL2
```bash
docker pull nvidia/cuda:11.8.0-runtime-ubuntu22.04
docker compose build
docker compose up -d
docker exec -it py-hatetris /bin/bash
```

```bash
python3.11 -m pip install -r requirements/common.txt
python3.11 -m pip install --force-reinstall "gym~=0.26"
export PYTHONPATH=./
python3.11 src/~~~.py
```

## Train

- Train P(seven)
  - `python3.11 src/train_sb3.py Pseven 10000000 auto`
  - The weights are saved in `weights/Pseven/*`
- Adjust EnemyEnv for Train EP(seven)
  - See `src/enemy_env.py` -> line:81
- Train EP(seven)
  - `python3.11 src/train_enemy_sb3.py EPseven 10000000 auto`
- Adjust TrainedAi for Train PEP(seven)
  - See `src/ai/trained.py` -> line:11
- Train PEP(seven)
  - `python3.11 src/train_player_sb3.py PEPseven 10000000 auto`

### Setup HatetrisAI

- Build hatetris-cpp

```bash
docker exec -it py-hatetris /bin/bash
cd src/
clang++ -O3 -Wall -shared -std=c++20 -fPIC $(python3.11 -m pybind11 --includes) ai/hatebind.cpp -o hate$(python3.11-config --extension-suffix) -I /usr/include/python3.11
```

- Debug hate.cpp

```bash
docker exec -it py-hatetris /bin/bash
cd src/
clang++ -std=c++20 -Wall -g3 -O0 -fno-rtti -fsanitize=undefined,address -fno-omit-frame-pointer ai/hate.cpp
gdb a.out
```

### Enable Discord WebHook notification

```sh
cat << '_EOF' > .env
PYTHONPATH=./
WEBHOOK_URL="https://discord.com/api/webhooks/012345/foobar"
_EOF
```

## Logging on Tensorboard

```sh
tensorboard --port 6006 --logdir log/
```

## EnemyAI vs Human

```pwsh
docker exec -it py-hatetris python3.11 src/play_manual.py
```

- The data will be saved as experiment.json in root dir
- Adjust `src/play_manual.py` and `src/game_manual.py` to change EnemyAI

## Evaluation PlayerAI vs EnemyAI

- Use `src/evaluation*.py`
- The args and methods are trash
- Call `evaluate_len` to print pieces ratio

## Play demo

- Adjust Env in `src/demo_sb3.py`
- `python3.11 src/demo_sb3.py`

## Play replay

- Copy `weights/Pseven/replay.py` to `src/replay.py`
- Adjust Env in `src/play_replay.py`
- `python3.11 src/play_replay.py`
