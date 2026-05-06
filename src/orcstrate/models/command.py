import json

class Command:
    def __init__(self, command: str, external: bool = False, keep_open: bool = True, name: str = None):
        self.command = command
        self.external = external
        self.keep_open = keep_open
        self.name = name or command

    def to_dict(self):
        return {
            "command": self.command,
            "external": self.external,
            "keep_open": self.keep_open,
            "name": self.name
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            command=data["command"],
            external=data.get("external", False),
            keep_open=data.get("keep_open", True),
            name=data.get("name")
        )