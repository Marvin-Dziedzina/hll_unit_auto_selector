# HLL Unit Auto Selector

This script lets you auto create a locked armor or recon unit in [Hell let Loose](https://store.steampowered.com/app/686810/Hell_Let_Loose/).

Use a template for different resolutions or create your own (Consider contributing it if its a new resolution).

## Running on Windows

Create a virtual enviroment:
```sh
python -m venv venv
```

Activate the enviroment in cmd.exe:
```sh
venv/Scripts/activate.bat
```

OR

Activate the enviroment in PowerShell:
```sh
venv/Scripts/Activate.ps1
```

Install the dependencies:
```sh
pip install -r requirements.txt
```

To run the unit auto selector:
```sh
python hll_unit_auto_selector.py --help
```

## Running on Linux

You need tkinter.

Create a virtual enviroment:
```sh
python -m venv .venv
```

Activate the enviroment:
```sh
source .venv/bin/activate
```

Install the dependencies:
```sh
pip install -r requirements.txt
```

To run the unit auto selector:
```sh
sudo -E $(pwd)/.venv/bin/python ./hll_unit_auto_selector.py --help
```

## Recording

It is recommendet that you use the infantry + button. This is because all other create unit buttons can move but the infantry is always on the same position.