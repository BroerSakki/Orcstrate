import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Orcstrate")
        self.set_default_size(600, 400)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box)

        label = Gtk.Label(label="Orcstrate is running 🚀")
        box.pack_start(label, True, True, 0)
