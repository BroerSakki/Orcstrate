from gi.repository import Gtk, GObject

class QueueButtonBox(Gtk.Box):
    __gsignals__ = {
        "delete-clicked": (GObject.SignalFlags.RUN_FIRST, None, ()),
        "run-clicked": (GObject.SignalFlags.RUN_FIRST, None, ())
    }

    def __init__(self):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL
        )
        self.build_ui()

    def build_ui(self):
        # Create Buttons
        # ---
        self.run_btn = Gtk.Button(
            label="Run Queue",
            icon_name="media-playback-start-symbolic"
        )

        self.delete_btn = Gtk.Button(
            label="Delete Selected",
            icon_name="list-remove-symbolic"
        )
        # ---

        # Emit signals
        # ---
        self.delete_btn.connect("clicked", lambda _: self.emit("delete-clicked"))
        # ---

        # Add CSS
        # ---
        self.run_btn.add_css_class(
            "suggested-action"
        )
        self.delete_btn.add_css_class(
            "destructive-action"
        )
        # ---

        # Format Buttons
        # ---
        self.delete_btn.set_size_request(102, 48)
        # ---

        # Append To Box
        # ---
        self.append(self.delete_btn)
        # ---
