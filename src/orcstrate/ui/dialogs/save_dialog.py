import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, Gio


class SaveDialog:

    def __init__(
        self,
        parent,
        on_save
    ):
        self.parent = parent

        self.on_save = on_save

        self.dialog = Gtk.FileDialog()

        filter = Gtk.FileFilter()

        filter.set_name("Orcstrate Files")

        filter.add_pattern("*.orc")

        store = Gio.ListStore.new(Gtk.FileFilter)

        store.append(filter)

        self.dialog.set_filters(store)

    def show(self):

        self.dialog.save(
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

            file = dialog.save_finish(result)

            path = file.get_path()

            if not path.endswith(".orc"):

                path += ".orc"

            self.on_save(path)

        except Exception as e:

            print(f"[ERROR] {e}")