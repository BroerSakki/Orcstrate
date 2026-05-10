from gi.repository import Gtk

from ui.widgets.queue.row import QueueRow


class QueueFactory:

    def __init__(self, drag_handler):

        self.drag_handler = drag_handler

        self.factory = Gtk.SignalListItemFactory()

        self.factory.connect(
            "setup",
            self.setup
        )

        self.factory.connect(
            "bind",
            self.bind
        )

    def get_factory(self):
        return self.factory

    def setup(self, factory, list_item):

        row = QueueRow()

        list_item.set_child(row)

        self.drag_handler.setup_drag_and_drop(
            row,
            list_item
        )

    def bind(self, factory, list_item):

        item = list_item.get_item()
        row = list_item.get_child()

        row.command_label.set_label(
            item.command_text
        )

        row.tag_label.set_label(
            item.search_tag
        )

        row.external_check.set_active(
            item.external
        )

        row.keep_open_check.set_active(
            item.keep_open
        )