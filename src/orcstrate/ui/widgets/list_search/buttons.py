from gi.repository import Gtk, GObject

class ListSearchButtonBox(Gtk.Box):
    __gsignals__ = {
        "add-command-clicked": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "delete-selected-clicked": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "queue-clicked": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "queue-all-clicked": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "edit-clicked": (GObject.SignalFlags.RUN_FIRST, None, ())
    }

    def __init__(self):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL
        )
        self.build_ui()

    def build_ui(self):
        # Create Grid
        # ---
        self.button_grid = Gtk.Grid()
        # ---

        # Set Grid Spacing
        # ---
        self.button_grid.set_row_spacing(6)
        self.button_grid.set_column_spacing(6)
        # ---

        # Create Buttons
        # ---
        self.add_btn = Gtk.Button(
            label="Add Command",
            icon_name="list-add-symbolic"
        )
        self.delete_btn = Gtk.Button(
            label="Delete Selected",
            icon_name="list-remove-symbolic"
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

        # Format Buttons
        # ---
        self.add_btn.set_size_request(-1, 48)
        for btn in [
            self.delete_btn,
            self.queue_btn,
            self.queue_all_btn,
            self.edit_btn
        ]:
            btn.set_size_request(48, 48)
        # ---

        # Attach To Grid
        # ---
        self.button_grid.attach(self.add_btn, 0, 0, 2, 1)
        self.button_grid.attach(self.delete_btn, 0, 1, 1, 1)
        self.button_grid.attach(self.edit_btn, 1, 1, 1, 1)
        self.button_grid.attach(self.queue_btn, 0, 2, 1, 1)
        self.button_grid.attach(self.queue_all_btn, 1, 2, 1, 1)
        # ---

        # Append Grid To Box
        # ---
        self.append(self.button_grid)
        # ---