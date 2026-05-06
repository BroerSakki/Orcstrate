import gi
import sys
gi.require_version("Gtk", "4.0")
gi.require_version("Gio", "2.0")
from gi.repository import Gtk, Gio
from ui.window import MainWindow
from models.command import Command

def is_dark_mode():
    """Detects dark mode on Linux and Windows (MSYS2)."""
    # 1. Check Windows (MSYS2)
    if sys.platform == "win32":
        try:
            import winreg
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            keypath = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'
            with winreg.OpenKey(registry, keypath) as reg_key:
                # 0 = Dark, 1 = Light
                value, _ = winreg.QueryValueEx(reg_key, 'AppsUseLightTheme')
                return value == 0
        except Exception:
            return False

    # 2. Check Linux
    try:
        # Check modern color-scheme setting
        interface_settings = Gio.Settings.new("org.gnome.desktop.interface")
        scheme = interface_settings.get_string("color-scheme")
        if scheme == "prefer-dark":
            return True
    except Exception:
        pass
    
    # Check legacy GTK setting
    gtk_settings = Gtk.Settings.get_default()
    return gtk_settings.get_property("gtk-application-prefer-dark-theme")

def update_theme_class(window):
    """Applies the .dark-mode CSS class based on OS detection."""
    if is_dark_mode():
        window.add_css_class("dark-mode")
        Gtk.Settings.get_default().set_property("gtk-application-prefer-dark-theme", True)
    else:
        window.remove_css_class("dark-mode")
        Gtk.Settings.get_default().set_property("gtk-application-prefer-dark-theme", False)

class App(Gtk.Application):
    # Constructor
    # ---
    def __init__(self, commands: list[Command]=[]):
        super().__init__(application_id="com.orcstrate.app")
        self.commands = commands
    # ---

    # App runner
    # ---
    def do_activate(self):
        win = MainWindow(self, self.commands)
        
        update_theme_class(win)

        win.present()
    # ---