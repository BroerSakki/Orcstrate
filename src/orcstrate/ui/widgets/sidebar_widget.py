import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gio", "2.0")
from gi.repository import Gtk, Gio, GObject, Gdk
from ui.widgets.addbutton_widget import AddBtnWidget
from ui.widgets.deletebtn_widget import DelBtnWidget
from ui.widgets.addqueue_widget import AddQueueWidget
from models.command import Command

class SideBarWidget:
    def __init__(self, root, commands: list[Command]):

        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        sidebar.set_size_request(150, -1)
        sidebar.add_css_class("sidebar") # Optional: style with CSS later
        sidebar.set_margin_end(10)

        AddBtnWidget(root, commands)
        DelBtnWidget(root, commands)
        AddQueueWidget(root, commands)

        sidebar.append(add_btn)
        sidebar.append(self.del_btn)
        sidebar.append(self.add_queue_btn)