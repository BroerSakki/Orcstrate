import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gio", "2.0")
from gi.repository import Gtk, Gio, GObject, Gdk
from models.command import Command

class ListScrollWidget:
    def __init__(self, root, commands: list[Command]):

        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_propagate_natural_height(True)
        self.scroll.set_hexpand(True)
        self.scroll.set_vexpand(True)
        self.scroll.set_child(self.list_view)
