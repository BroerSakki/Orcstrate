from models.command import Command
from core.storage import load_commands, save_commands

class Workspace:
    def __init__(self):
        self.commands: list[Command] = []
        self.filepath: str | None = None

    def load(self, filepath: str):
        self.commands = load_commands(filepath)
        self.filepath = filepath

    def save(self):
        if not self.filepath:
            raise ValueError("No file path set")

        save_commands(self.commands, self.filepath)

    def save_as(self, filepath: str):
        self.filepath = filepath
        self.save()