from gi.repository import Gtk


class CommandRow(Gtk.Box):

    def __init__(self):

        super().__init__(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=8
        )

        self.set_margin_top(4)
        self.set_margin_bottom(4)
        self.set_margin_start(8)
        self.set_margin_end(8)

        self.add_css_class("command-row")

        # Drag handle
        self.handle = Gtk.Image.new_from_icon_name(
            "open-menu-symbolic"
        )

        self.handle.add_css_class("drag-handle")

        self.append(self.handle)

        # Command text
        self.command_edit = Gtk.Label()

        self.command_edit.set_hexpand(True)

        self.command_edit.set_width_chars(15)

        self.command_edit.add_css_class(
            "cmd-field"
        )

        self.command_edit.set_tooltip_text(
            "Command"
        )

        self.append(self.command_edit)

        # Search tag
        self.tag_edit = Gtk.Label()

        self.tag_edit.set_width_chars(10)

        self.tag_edit.add_css_class(
            "tag-field"
        )

        self.tag_edit.set_tooltip_text(
            "Search Tag"
        )

        self.append(self.tag_edit)

        # External checkbox
        self.external_check = Gtk.CheckButton(
            label="External"
        )

        self.external_check.add_css_class(
            "modern-check"
        )

        self.append(self.external_check)

        # Keep open checkbox
        self.keep_open_check = Gtk.CheckButton(
            label="Keep Open"
        )

        self.keep_open_check.add_css_class(
            "modern-check"
        )

        self.append(self.keep_open_check)