# Orcstrate

A lightweight GTK-based tool for managing and executing command queues on Linux.

## Features (planned)
- Sequential and parallel command execution
- Profile saving/loading
- Multi-terminal support

## Requirements
- Python 3
- GTK 4 (PyGObject)

## Setup
### Linux
```bash
git clone https://github.com/BroerSakki/Orcstrate.git
cd Orcstrate
./scripts/setup.sh
```

### Windows
1. Install [MSYS2](https://www.msys2.org/) (Follow [this](https://www.gtk.org/docs/installations/windows) tutorial for more detailed steps)
2. Run these commands in the MSYS2 shell (The UCRT64 one)
```
-pacman -Syu
pacman -S mingw-w64-ucrt-x86_64-gtk4
pacman -S mingw-w64-ucrt-x86_64-python-gobject
pacman -S mingw-w64-ucrt-x86_64-xfce4-terminal
```
3. If needed add "C:\msys64\mingw64\bin" to PATH in the Windows System Environment Variables

## Running

### Linux
```bash
PYTHONPATH=src python3 src/orcstrate/main.py
```

### Windows
1. In the MSYS2 shell (The UCRT64 one), cd into the Orcstrate folder and run this command
```
python3 src/orcstrate/main.py
```