from gi.repository import Gio

from models.command_object import (
    CommandObject
)

from core.runner import (
    CommandRunner
)


class QueueService:

    def __init__(self):

        self.list_store = Gio.ListStore(
            item_type=CommandObject
        )

    def get_model(self):
        return self.list_store

    def add(self, command):

        self.list_store.append(
            CommandObject(command)
        )

    def remove(self, item):

        found, index = self.list_store.find(
            item
        )

        if found:
            self.list_store.remove(index)

    def get_commands(self):

        return [
            self.list_store.get_item(i)
            .get_command()

            for i in range(
                self.list_store.get_n_items()
            )
        ]

    def run_queue(self):

        runner = CommandRunner()

        runner.load_commands(
            self.get_commands()
        )

        runner.run_queue()