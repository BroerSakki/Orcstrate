import gi
gi.require_version("Gtk", "4.0")
gi.require_version('Vte', '3.91')
from gi.repository import Gtk, Gdk, GLib, Vte
import os

from core.queue_service import QueueService
from ui.widgets.terminal_widget.buttons import TerminalButtonBox

class TerminalWidget(Gtk.Box):

    def __init__(self, queue_service):
        super().__init__(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12
        )

        self.set_hexpand(True)
        self.set_vexpand(True)

        self.queue_service:QueueService = queue_service

        self.terminal = Vte.Terminal(hexpand=True,vexpand=True)

        self.spawn_async_terminal()

        self.build_ui()

    def build_ui(self):
        self.buttons = TerminalButtonBox()

        self.buttons.connect("run-clicked", self.on_play_clicked)

        self.append(self.terminal)
        self.append(self.buttons)

    def spawn_async_terminal(self):
        shell_bin = os.environ.get("SHELL", "/bin/sh")
        argv = [shell_bin]
        working_dir = os.environ.get("HOME", "/")

        self.terminal.spawn_async(
            Vte.PtyFlags.DEFAULT,
            working_dir,
            argv,
            None,
            GLib.SpawnFlags.DEFAULT,
            None, None,
            -1,
            None,
            None,
            None
        )

    def on_play_clicked(self, btn):
        self.queue_service.run_queue(self.terminal)