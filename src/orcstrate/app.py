import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from ui.window import MainWindow
from models.command import Command

class App(Gtk.Application):
    # Constructor
    # ---
    def __init__(self, commands: list[Command]):
        super().__init__(application_id="com.orcstrate.app")
        self.commands = commands
    # ---

    # App runner
    # ---
    def do_activate(self):
        win = MainWindow(self, self.commands)
        win.present()
    # ---