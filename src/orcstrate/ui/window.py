import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from ui.list_search_widget import ListSearchWidget
from models.command import Command

class MainWindow(Gtk.ApplicationWindow):
    # Constructor
    # ---
    def __init__(self, app, commands: list[Command]):
        super().__init__(application=app, title="Orcstrate")

        # Root layout
        # ---
        self.root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_child(self.root)
        # ---
        
        # List Search Widget
        # ---
        """
        The commands passed here should come from a file storing entered commands
        For now we can just not pass any initial commands, meaning entered commands reset when the app closes.
        
        It's not an essential feature, so can add later on if we get time
        """
        ListSearchWidget(self.root, commands)
        # ---
    # ---