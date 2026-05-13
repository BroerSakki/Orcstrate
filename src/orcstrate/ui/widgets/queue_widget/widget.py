import gi
import time
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from gi.repository import Gio
from models.command_object import CommandObject
from models.command import Command
from core.runner import CommandRunner
from core.queue_service import QueueService
from ui.widgets.queue_widget.factory import QueueFactory
from ui.widgets.queue_widget.buttons import QueueButtonBox
from ui.widgets.queue_widget.drag_drop import QueueDragDrop


class QueueWidget(Gtk.Box):
    def __init__(self, queue_service):

        super().__init__(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12
        )

        self.queue_service:QueueService = queue_service

        self.set_hexpand(True)
        self.set_vexpand(True)

        self.set_margin_top(12)
        self.set_margin_bottom(12)
        self.set_margin_start(12)
        self.set_margin_end(12)

        self.drag_handler = QueueDragDrop(
            self.queue_service.get_model()
        )

        self.factory = QueueFactory(
            self.drag_handler
        )

        self.selection = Gtk.SingleSelection(
            model=self.queue_service.get_model()
        )

        self.list_view = Gtk.ListView(
            model=self.selection,
            factory=self.factory.get_factory()
        )

        self.build_ui()

    def build_ui(self):
        # Create Content
        # ---
        scroll = Gtk.ScrolledWindow(
            hexpand=True,
            vexpand=True
        )
        scroll.set_child(self.list_view)
        self.buttons = QueueButtonBox()
        # ---

        # Connect Buttons
        # ---
        self.buttons.connect("run-clicked", self.on_play_clicked)
        self.buttons.connect("delete-clicked", self.on_delete_selected)
        # ---

        # Append Content
        # ---
        self.append(scroll)
        self.append(self.buttons)
        # ---

    def on_delete_selected(self, btn):
        selected:CommandObject = (
            self.selection.get_selected_item()
        )
        if not selected:
            return
        print(f"\n[QUEUE] Removing command: {selected.get_command().command}")
        self.queue_service.remove(selected)

    def on_play_clicked(self, btn):
        self.queue_service.run_queue()