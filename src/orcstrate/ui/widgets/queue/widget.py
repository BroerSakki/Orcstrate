import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk
from gi.repository import Gio

from models.command_object import (
    CommandObject
)

from models.command import Command

from core.runner import (
    CommandRunner
)

from core.queue_service import (
    QueueService
)

from ui.widgets.queue.factory import (
    QueueFactory
)

from ui.widgets.queue.drag_drop import (
    QueueDragDrop
)


class QueueWidget(Gtk.Box):

    def __init__(self, queue_service):

        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
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

        scroll = Gtk.ScrolledWindow(
            hexpand=True,
            vexpand=True
        )

        scroll.set_child(self.list_view)

        self.append(scroll)

        button_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8
        )

        self.append(button_box)

        play_btn = Gtk.Button(
            label="Play Queue",
            icon_name="media-playback-start-symbolic"
        )

        play_btn.add_css_class(
            "suggested-action"
        )

        play_btn.connect(
            "clicked",
            self.on_play_clicked
        )

        button_box.append(play_btn)

        delete_btn = Gtk.Button(
            label="Remove",
            icon_name="user-trash-symbolic"
        )

        delete_btn.add_css_class(
            "destructive-action"
        )

        delete_btn.connect(
            "clicked",
            self.on_delete_selected
        )

        button_box.append(delete_btn)

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