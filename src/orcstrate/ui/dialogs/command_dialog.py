import gi

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk

from models.command import Command


class CommandDialog(Gtk.Dialog):
    def __init__(
        self,
        parent,
        command=None
    ):

        super().__init__(
            title="Edit Command",
            transient_for=parent,
            modal=True
        )

        self.set_default_size(500, 300)

        self.command = command

        self.build_ui()

        if command:
            self.load_command(command)

    def build_ui(self):

        content = self.get_content_area()

        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12
        )

        box.set_margin_top(12)
        box.set_margin_bottom(12)
        box.set_margin_start(12)
        box.set_margin_end(12)

        content.append(box)

        # Name
        # ---
        self.name_entry = Gtk.Entry()
        self.name_entry.set_placeholder_text(
            "Command Name"
        )

        box.append(Gtk.Label(
            label="Name",
            xalign=0
        ))

        box.append(self.name_entry)
        # ---

        # Command
        # ---
        self.command_entry = Gtk.Entry()
        self.command_entry.set_placeholder_text(
            "Command"
        )

        box.append(Gtk.Label(
            label="Command",
            xalign=0
        ))

        box.append(self.command_entry)
        # ---

        # Checkboxes
        # ---
        self.external_check = Gtk.CheckButton(
            label="Run externally"
        )

        self.keep_open_check = Gtk.CheckButton(
            label="Keep terminal open"
        )

        box.append(self.external_check)
        box.append(self.keep_open_check)
        # ---

        # Buttons
        # ---
        self.add_button(
            "Cancel",
            Gtk.ResponseType.CANCEL
        )

        self.add_button(
            "Save",
            Gtk.ResponseType.OK
        )
        # ---

    def load_command(self, command):
        self.name_entry.set_text(command.name)

        self.command_entry.set_text(
            command.command
        )
        self.external_check.set_active(
            command.external
        )
        self.keep_open_check.set_active(
            command.keep_open
        )

    def get_command(self):

        return Command(
            command=self.command_entry.get_text(),
            external=self.external_check.get_active(),
            keep_open=self.keep_open_check.get_active(),
            name=self.name_entry.get_text()
        )