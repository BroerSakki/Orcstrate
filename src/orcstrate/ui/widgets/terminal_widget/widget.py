import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk


class TerminalWidget(Gtk.Box):
    """Placeholder terminal - a simple black box for layout preview."""

    def __init__(self):
        super().__init__()

        self.set_hexpand(True)
        self.set_vexpand(True)
        self.set_size_request(-1, 250)

        css = b"""
        .terminal-box {
            background-color: #000000;
            border: 1px solid #333333;
        }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        style_context = self.get_style_context()
        style_context.add_provider(
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        style_context.add_class("terminal-box")