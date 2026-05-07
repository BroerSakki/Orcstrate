import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gio", "2.0")
from gi.repository import Gtk, Gio, GObject, Gdk
from models.command import Command

class AddBtnWidget:
    def __init__(self, root, commands: list[Command]):
        # Add Button
        add_btn = Gtk.Button(label="Add Command", icon_name="list-add-symbolic")
        add_btn.connect("clicked", self.on_add_clicked)

        
        