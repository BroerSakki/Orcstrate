from gi.repository import Gtk, GObject


class ListSearchSidebar(Gtk.Box):
    __gsignals__ = {
        "add-command-clicked": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "delete-selected-clicked": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "queue-clicked": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "queue-all-clicked": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "edit-clicked": (GObject.SignalFlags.RUN_FIRST, None, ())
    }

    def __init__(self):

        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=8
        )

        self.set_size_request(180, -1)
        self.add_css_class("sidebar")
        self.build_ui()

    def build_ui(self):
        # Create buttons
        # ---
        self.add_btn = Gtk.Button(
            label="Add Command",
            icon_name="list-add-symbolic"
        )
        self.delete_btn = Gtk.Button(
            label="Delete Selected",
            icon_name="user-trash-symbolic"
        )
        self.queue_btn = Gtk.Button(
            label="Add To Queue",
            icon_name="mail-reply-rtl-symbolic"
        )
        self.queue_all_btn = Gtk.Button(
            label="Add All To Queue",
            icon_name="mail-reply-all-symbolic-rtl"
        )
        self.edit_btn = Gtk.Button(
            label="Edit",
            icon_name="edit-symbolic"
        )
        # ---        

        # Emit signals
        # ---
        self.add_btn.connect("clicked", lambda _: self.emit("add-command-clicked"))
        self.delete_btn.connect("clicked", lambda _: self.emit("delete-selected-clicked"))
        self.queue_btn.connect("clicked", lambda _: self.emit("queue-clicked"))
        self.queue_all_btn.connect("clicked", lambda _: self.emit("queue-all-clicked"))
        self.edit_btn.connect("clicked", lambda _: self.emit("edit-clicked"))
        # ---

        # Add CSS
        # ---
        self.delete_btn.add_css_class(
            "destructive-action"
        )
        self.queue_btn.add_css_class(
            "suggested-action"
        )
        # ---

        # Append buttons
        # ---
        self.append(self.add_btn)
        self.append(self.delete_btn)
        self.append(self.queue_btn)
        self.append(self.queue_all_btn)
        self.append(self.edit_btn)
        # ---