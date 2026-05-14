from gi.repository import Gtk, GObject

class TerminalButtonBox(Gtk.Box):
    __gsignals__ = {
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
        # ---

        # Emit signals
        # ---
        self.run_btn.connect("clicked", lambda _: self.emit("run-clicked"))
        # ---

        # Add CSS
        # ---
        self.run_btn.add_css_class(
            "suggested-action"
        )
        # ---

        # Format Buttons
        # ---
        self.run_btn.set_size_request(102, 48)
        self.run_btn.set_margin_bottom(6)
        # ---

        # Append To Box
        # ---
        self.append(self.run_btn)
        # ---