from gi.repository import GObject

from models.command import Command


class CommandObject(GObject.Object):

    command_text = GObject.Property(type=str)
    search_tag = GObject.Property(type=str)

    external = GObject.Property(
        type=bool,
        default=False
    )

    keep_open = GObject.Property(
        type=bool,
        default=False
    )

    def __init__(self, command: Command):
        super().__init__()

        self.command_text = command.command
        self.search_tag = command.name
        self.external = command.external
        self.keep_open = command.keep_open

    def get_command(self):
        return Command(
            self.command_text,
            self.external,
            self.keep_open,
            self.search_tag
        )