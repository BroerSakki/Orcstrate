import json
from models.command import Command

def save_commands(commands: list[Command], filename: str):
    with open(filename, "w") as f:
        json.dump([c.to_dict() for c in commands], f, indent=4)

def load_commands(filename: str) -> list[Command]:
    with open(filename, "r") as f:
        data = json.load(f)
    return [Command.from_dict(d) for d in data]