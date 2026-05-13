from gi.repository import Gtk


class QueueRow(Gtk.Box):

    def __init__(self):
        super().__init__(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8
        )

        self.add_css_class("row-container")

        self.set_margin_top(4)
        self.set_margin_bottom(4)
        self.set_margin_start(8)
        self.set_margin_end(8)

        self.command_label = Gtk.Label(
            xalign=0,
            hexpand=True
        )

        self.command_label.set_width_chars(15)

        self.append(self.command_label)

        self.tag_label = Gtk.Label(
            xalign=0
        )

        self.tag_label.set_width_chars(10)

        self.append(self.tag_label)

        self.external_check = Gtk.CheckButton(
            label="External"
        )

        self.external_check.set_sensitive(False)

        self.append(self.external_check)

        self.keep_open_check = Gtk.CheckButton(
            label="Keep Open"
        )

        self.keep_open_check.set_sensitive(False)

        self.append(self.keep_open_check)