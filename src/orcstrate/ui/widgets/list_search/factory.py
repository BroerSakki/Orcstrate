from gi.repository import Gtk
from gi.repository import GObject

from ui.widgets.list_search.row import (
    CommandRow
)


class ListSearchFactory:

    def __init__(
        self,
        filtering,
        drag_handler=None
    ):

        self.filtering = filtering
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

    def setup(
        self,
        factory,
        list_item
    ):

        row = CommandRow()

        list_item.set_child(row)

        if self.drag_handler:
            self.drag_handler.setup_drag_and_drop(
                row,
                list_item
            )

    def bind(
        self,
        factory,
        list_item
    ):

        item = list_item.get_item()

        row = list_item.get_child()

        item.bind_property(
            "command_text",
            row.command_edit,
            "label",

            GObject.BindingFlags.BIDIRECTIONAL
            |
            GObject.BindingFlags.SYNC_CREATE
        )
                
        item.bind_property(
            "search_tag",
            row.tag_edit,
            "label",

            GObject.BindingFlags.BIDIRECTIONAL
            |
            GObject.BindingFlags.SYNC_CREATE
        )

        item.bind_property(
            "external",
            row.external_check,
            "active",

            GObject.BindingFlags.BIDIRECTIONAL
            |
            GObject.BindingFlags.SYNC_CREATE
        )

        item.bind_property(
            "keep_open",
            row.keep_open_check,
            "active",

            GObject.BindingFlags.BIDIRECTIONAL
            |
            GObject.BindingFlags.SYNC_CREATE
        )

    def on_tag_editing_toggled(
        self,
        label,
        pspec,
        item
    ):

        if label.get_editing():
            return

        new_tag = (
            label.get_text()
            .strip()
            .lower()
        )

        old_tag = (
            item.search_tag.lower()
            if item.search_tag
            else ""
        )

        if new_tag == old_tag:
            return

        self.filtering.update_tag(
            item,
            old_tag,
            new_tag
        )

        item.search_tag = new_tag

        self.filtering.trigger_filter()