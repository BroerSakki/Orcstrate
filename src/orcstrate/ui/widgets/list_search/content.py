import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from gi.repository import Gio
from ui.widgets.list_search.factory import ListSearchFactory
from ui.widgets.list_search.filtering import SearchFiltering
from ui.widgets.list_search.drag_drop import ListSearchDragDrop


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

        # Selection
        self.selection = Gtk.SingleSelection(
            model=filter_model
        )

        # Drag and drop
        self.drag_handler = ListSearchDragDrop(
            self.model,
            self.selection
        )

        # Factory
        self.factory = ListSearchFactory(
            self.filtering,
            drag_handler=self.drag_handler
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
