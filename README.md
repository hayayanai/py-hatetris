# py-hatetris

## Make a virtual environment

### For Ubuntu

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements/dev.txt
pip install "gym~=0.26"

deactivate
```

### For powershell

```ps1
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements/dev.txt
python -m pip install "gym~=0.26"
```

## Build hatetris-cpp

```bash
docker pull nvidia/cuda:11.8.0-runtime-ubuntu22.04
docker compose up -d
docker exec -it yanai3.11 /bin/bash
cd src/
clang++ -O3 -Wall -shared -std=c++20 -fPIC $(python3.11 -m pybind11 --includes) ai/hatebind.cpp -o hate$(python3.11-config --extension-suffix) -I /usr/include/python3.11
```

## Debug hate.cpp

```bash
cd src/
clang++ -std=c++20 -Wall -g3 -O0 -fno-rtti -fsanitize=undefined,address -fno-omit-frame-pointer ai/hate.cpp
apt-get install gdb -y
gdb a.out
```
