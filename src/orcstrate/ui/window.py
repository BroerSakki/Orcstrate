import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

class MainWindow(Gtk.ApplicationWindow):
    # Constructor
    # ---
    def __init__(self, app):
        super().__init__(application=app, title="Orcstrate")

        # Root layout
        # ---
        self.root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_child(self.root)
        # ---
    # ---