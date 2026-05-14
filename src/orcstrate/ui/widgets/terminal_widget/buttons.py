from gi.repository import Gtk, GObject

class TerminalButtonBox(Gtk.Box):
    __gsignals__ = {
    }

    def __init__(self):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL
        )
        self.build_ui()

    def build_ui(self):
        # No buttons needed in this widget
        pass
