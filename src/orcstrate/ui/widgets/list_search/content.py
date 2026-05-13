import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from gi.repository import Gio
from ui.widgets.list_search.factory import ListSearchFactory
from ui.widgets.list_search.filtering import SearchFiltering


class ListSearchContentBox(Gtk.Box):
    def __init__(self, model):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL
        )

        self.model = model
        self.build_ui()

    def build_ui(self):
        # Search entry
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_hexpand(True)
        self.search_entry.set_margin_bottom(12)

        search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        search_box.append(self.search_entry)
        self.append(search_box)

        # Filtering
        self.filtering = SearchFiltering(
            self.model,
            self.search_entry
        )

        filter_model = Gtk.FilterListModel(
            model=self.model,
            filter=self.filtering.get_filter()
        )

        # Factory
        self.factory = ListSearchFactory(
            self.filtering
        )

        # Selection
        self.selection = Gtk.SingleSelection(
            model=filter_model
        )

        # List view
        self.list_view = Gtk.ListView(
            model=self.selection,
            factory=self.factory.get_factory()
        )

        # Scroll
        scroll = Gtk.ScrolledWindow(
            hexpand=True,
            vexpand=True
        )

        scroll.set_child(self.list_view)
        self.append(scroll)