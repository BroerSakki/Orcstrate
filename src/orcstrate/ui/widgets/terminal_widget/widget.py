import gi
gi.require_version("Gtk", "4.0")
gi.require_version('Vte', '3.91')
from gi.repository import Gtk, Gdk, GLib, Vte
import os

from core.queue_service import QueueService


class TerminalWidget(Gtk.Box):

    def __init__(self, queue_service):
        super().__init__(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12
        )

        self.set_hexpand(True)
        self.set_vexpand(False)

        self.queue_service:QueueService = queue_service

        self.terminal = Vte.Terminal(hexpand=True, vexpand=False)
        self.terminal.set_size_request(-1, 100)

        self.spawn_async_terminal()

        self.build_ui()

    def build_ui(self):
        self.append(self.terminal)

    def get_terminal(self):
        return self.terminal

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