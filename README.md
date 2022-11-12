# py-hatetris

## Make a virtual environment

```sh
python3 -m venv .venv
source .venv/Scripts/activate
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
docker compose up -d
docker exec -it yanai3.10 /bin/bash
cd src/
clang++ -O3 -Wall -shared -std=c++14 -fPIC `python3.10 -m pybind11 --includes` ai/hatebind.cpp -o hate`python3.10-config --extension-suffix` -I /usr/include/python3.10
```

## Debug hate.cpp

```bash
cd src/
clang++ -std=c++14 -g ai/hate.cpp
gdb a.out
```
