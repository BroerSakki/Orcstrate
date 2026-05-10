from core.storage import (
    load_commands,
    save_commands
)


class Workspace:
    # Constructor
    # ---
    def __init__(self, command_service):

        self.command_service = command_service

        self.filepath = None
    # ---

    # Load
    # ---
    def load(self, filepath):

        commands = load_commands(filepath)

        self.command_service.load(
            commands
        )

        self.filepath = filepath
    # ---

    # Save
    # ---
    def save(self):

        if not self.filepath:
            raise ValueError(
                "No file path set"
            )

        save_commands(
            self.command_service.get_commands(),
            self.filepath
        )
    # ---

    # Save as
    # ---
    def save_as(self, filepath):

        self.filepath = filepath

        self.save()
    # ---