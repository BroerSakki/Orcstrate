import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gio", "2.0")
from gi.repository import Gtk, Gio, GObject, Gdk
from models.command import Command

class DelBtnWidget:
    def __init__(self, root, commands: list[Command]):

        self.del_btn = Gtk.Button(label="Delete Selected", icon_name="user-trash-symbolic")
        self.del_btn.add_css_class("destructive-action")
        self.del_btn.connect("clicked", self.on_delete_selected)