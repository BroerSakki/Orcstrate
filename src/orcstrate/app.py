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
        
        def update_theme_class(*args):
            # Check if the system prefers dark
            settings = Gtk.Settings.get_default()
            is_dark = settings.get_property("gtk-application-prefer-dark-theme")
            
            # Also check for Libadwaita style system preference
            # (Needed for modern GNOME)
            if is_dark:
                win.add_css_class("dark-mode")
            else:
                win.remove_css_class("dark-mode")
                
        settings = Gtk.Settings.get_default()
        settings.connect("notify::gtk-application-prefer-dark-theme", update_theme_class)
        
        update_theme_class()

        win.present()
    # ---