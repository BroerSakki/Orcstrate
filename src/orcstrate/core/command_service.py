from gi.repository import Gio
from models.command import Command
from models.command_object import CommandObject


class CommandService:

    def __init__(self, commands: list[Command]):
        self._commands = commands
        self._model = Gio.ListStore(
            item_type=CommandObject
        )
        self._build_model()

    def _build_model(self):
        for cmd in self._commands:
            self._model.append(
                CommandObject(cmd)
            )

    # PUBLIC API
    # ---
    def get_model(self):
        """GTK widgets use THIS"""
        return self._model

    def get_commands(self):
        """Backend / saving / execution"""
        return [
            self._model.get_item(i).get_command()
            for i in range(self._model.get_n_items())
        ]

    def add(self, command: Command):
        obj = CommandObject(command)
        self._model.append(obj)
        self._commands.append(command)

    def remove(self, obj: CommandObject):
        found, index = self._model.find(obj)
        if found:
            self._model.remove(index)

    def load(self, commands):
    
        self._model.remove_all()
    
        self._commands = commands
    
        for cmd in commands:
        
            self._model.append(
                CommandObject(cmd)
            )
    
    def update(self):
        """Optional hook if you later add persistence"""
        pass

    def build_model(self):

        model = Gio.ListStore(CommandObject)

        for cmd in self.commands:
            model.append(CommandObject(cmd))

        return model
    # ---