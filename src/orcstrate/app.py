import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from ui.window import MainWindow

class App(Gtk.Application):
    # Constructor
    # ---
    def __init__(self):
        super().__init__(application_id="com.orcstrate.app")
    # ---

    # App runner
    # ---
    def do_activate(self):
        win = MainWindow(self)
        win.present()
    # ---