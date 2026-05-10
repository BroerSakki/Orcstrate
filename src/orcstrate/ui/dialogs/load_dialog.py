import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk


class LoadDialog:

    def __init__(
        self,
        parent,
        on_load
    ):

        self.parent = parent

        self.on_load = on_load

        self.dialog = Gtk.FileDialog()

    def show(self):

        self.dialog.open(
            self.parent,
            None,
            self.on_response
        )

    def on_response(
        self,
        dialog,
        result
    ):

        try:

            file = dialog.open_finish(result)

            path = file.get_path()

            self.on_load(path)

        except Exception as e:

            print(f"[ERROR] {e}")