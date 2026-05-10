import gi
gi.require_version("Gtk", "4.0")

from gi.repository import Gtk
from gi.repository import Gio

from models.command import Command

from models.command_object import (
    CommandObject
)

from ui.widgets.list_search.factory import (
    ListSearchFactory
)

from ui.widgets.list_search.filtering import (
    SearchFiltering
)

from ui.widgets.list_search.sidebar import (
    ListSearchSidebar
)

from ui.dialogs.command_dialog import (
    CommandDialog
)


class ListSearchWidget(Gtk.Box):

    def __init__(
        self,
        command_service,
        queue_service
    ):

        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12
        )

        self.command_service = command_service
        self.queue_service = queue_service

        self.set_hexpand(True)
        self.set_vexpand(True)

        self.set_margin_top(12)
        self.set_margin_bottom(12)
        self.set_margin_start(12)
        self.set_margin_end(12)

        self.model = self.command_service.get_model()

        self.build_ui()

    def build_ui(self):

        # Search entry
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_hexpand(True)

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

        # Sidebar
        # ---
        self.sidebar = ListSearchSidebar()
        self.sidebar.set_size_request(180, -1)
        self.sidebar.add_css_class("sidebar")

        self.sidebar.connect(
            "add-command-clicked",
            self.on_add_clicked
        )
        self.sidebar.connect(
            "delete-selected-clicked",
            self.on_delete_selected)
        self.sidebar.connect(
            "queue-clicked",
            self.on_add_queue_clicked
        )
        self.sidebar.connect(
            "edit-clicked",
            self.on_edit_clicked
        )
        # ---

        # Main content
        # ---
        content_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12
        )

        content_box.append(scroll)

        content_box.append(self.sidebar)

        self.append(content_box)
        # ---

    # Event handlers
    # ---
    def on_add_clicked(self, btn):

        dialog = CommandDialog(
            self.get_root()
        )

        dialog.connect(
            "response",
            self.on_add_dialog_response
        )

        dialog.present()

    def on_delete_selected(self, btn):
        selected:CommandObject = (
            self.selection.get_selected_item()
        )
        if not selected:
            return

        print(f"\n[LIST] Removing command: {selected.get_command().command}")
        self.command_service.remove(selected)

    def on_add_queue_clicked(self, btn):
        selected = (
            self.selection.get_selected_item()
        )
        if not selected:
            return

        print(f"\n[QUEUE] Adding command: {selected.get_command().command}")
        self.queue_service.add(
            selected.get_command()
        )

    def on_edit_clicked(self, btn):

        selected = (
            self.selection.get_selected_item()
        )

        if not selected:
            return

        dialog = CommandDialog(
            self.get_root(),
            selected.get_command()
        )

        dialog.connect(
            "response",
            self.on_edit_dialog_response,
            selected
        )

        dialog.present()

    def on_add_dialog_response(
        self,
        dialog,
        response
    ):

        if response == Gtk.ResponseType.OK:

            command = dialog.get_command()

            self.command_service.add(
                command
            )

        dialog.destroy()

    def on_edit_dialog_response(
        self,
        dialog,
        response,
        selected
    ):

        if response == Gtk.ResponseType.OK:

            updated = dialog.get_command()

            selected.command_text = updated.command
            selected.search_tag = updated.name
            selected.external = updated.external
            selected.keep_open = updated.keep_open

        dialog.destroy()
    # ---