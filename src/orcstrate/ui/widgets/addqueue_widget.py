import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gio", "2.0")
from gi.repository import Gtk, Gio, GObject, Gdk
from models.command import Command

class AddQueueWidget:
    def __init__(self, root, commands: list[Command]):

        self.add_queue_btn = Gtk.Button(label="Add To Queue", icon_name="go-next-symbolic")
        self.add_queue_btn.add_css_class("suggested-action")
        self.add_queue_btn.connect("clicked", self.on_add_queue_clicked)