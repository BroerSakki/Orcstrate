from gi.repository import Gtk
from gi.repository import GObject


class SearchFiltering:

    def __init__(
        self,
        list_store,
        search_entry
    ):

        self.list_store = list_store
        self.search_entry = search_entry

        self.command_map = {}

        self.search_timeout_id = None

        self.custom_filter = Gtk.CustomFilter.new(
            self.filter_func,
            self.search_entry
        )

        self.search_entry.connect(
            "search-changed",
            self.on_search_changed
        )

    def get_filter(self):
        return self.custom_filter

    def add_item(self, item):

        tag = (
            item.search_tag.lower()
            if item.search_tag
            else ""
        )

        if not tag:
            return

        if tag not in self.command_map:
            self.command_map[tag] = []

        self.command_map[tag].append(item)

    def remove_item(self, item):

        tag = (
            item.search_tag.lower()
            if item.search_tag
            else ""
        )

        if tag not in self.command_map:
            return

        if item in self.command_map[tag]:
            self.command_map[tag].remove(item)

        if not self.command_map[tag]:
            del self.command_map[tag]

    def update_tag(
        self,
        item,
        old_tag,
        new_tag
    ):

        old_tag = old_tag.lower()
        new_tag = new_tag.lower()

        if old_tag in self.command_map:

            if item in self.command_map[old_tag]:
                self.command_map[old_tag].remove(item)

            if not self.command_map[old_tag]:
                del self.command_map[old_tag]

        if new_tag:

            if new_tag not in self.command_map:
                self.command_map[new_tag] = []

            self.command_map[new_tag].append(item)

    def on_search_changed(self, entry):

        if self.search_timeout_id:
            GObject.source_remove(
                self.search_timeout_id
            )

        self.search_timeout_id = (
            GObject.timeout_add(
                300,
                self.trigger_filter
            )
        )

    def trigger_filter(self):

        self.custom_filter.changed(
            Gtk.FilterChange.DIFFERENT
        )

        self.search_timeout_id = None

        return False

    def filter_func(
        self,
        item,
        search_entry
    ):

        query = (
            search_entry
            .get_text()
            .strip()
            .lower()
        )

        if not query:
            return True

        matches = self.command_map.get(query)

        if matches is not None:
            return item in matches

        return query in item.search_tag.lower()