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

        # Initialize a dictionary used for hashing
        # Python uses the SipHash algorithm to generate hash values.
        # - It randomly generates a secret key each time a python process is started, which means better prevention against DoS attacks.
        # - The output is a 64-bit output
        # Python handles collisions using open addressing with a pseudo-random probing sequence
        # - When a collision is met, probe for a new slot using this algorithm (j = (5*j) + 1 + perturb (perturb is bits from the original hash))
        # - This pseudo-random probing helps avoid clustering
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

        # Check if item has a search tag
        tag = (
            item.search_tag.lower()
            if item.search_tag
            else ""
        )

        if not tag:
            return

        # Add search tag to hashmap, if not already
        if tag not in self.command_map:
            self.command_map[tag] = []

        # The hashmap element is an array incase multiple commands have the same tag
        self.command_map[tag].append(item)

    def remove_item(self, item):

        # Check if item has a search tag
        tag = (
            item.search_tag.lower()
            if item.search_tag
            else ""
        )

        # Check if tag exists
        if tag not in self.command_map:
            return

        # Remove item from tag array
        if item in self.command_map[tag]:
            self.command_map[tag].remove(item)

        # Remove entire tag if tag doesn't hold any items
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

        # Firstly check if old tag exists
        if old_tag in self.command_map:

            # Remove item from tag
            if item in self.command_map[old_tag]:
                self.command_map[old_tag].remove(item)

            # Remove entire tag if tag doesn't hold any items
            if not self.command_map[old_tag]:
                del self.command_map[old_tag]

        # Check if item needs to be added to tag
        if new_tag:

            # Create tag if not exists
            if new_tag not in self.command_map:
                self.command_map[new_tag] = []

            # Add item to tag
            self.command_map[new_tag].append(item)

    def on_search_changed(self, entry):

        if self.search_timeout_id:
            GObject.source_remove(
                self.search_timeout_id
            )

        # Add a 300ms delay to search, to not constantly try to search
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

        # If search is empty don't try to search
        if not query:
            return True

        # Try to get search from hashmap
        matches = self.command_map.get(query)

        # If found show all items under that tag name
        if matches is not None:
            return item in matches

        # If nothing is found in hashmap use slower search as fallback
        return query in item.search_tag.lower()