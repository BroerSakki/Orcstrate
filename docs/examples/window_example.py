import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Orcstrate")
        
        # Root layout
        # ---
        self.root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_child(self.root)
        # ---

        # Header
        # ---
        header = Gtk.Label(label="Welcome to Orcstrate")
        self.root.append(header)
        # ---

        # Input row
        # ---
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Type something...")

        btn = Gtk.Button(label="Submit")
        btn.connect("clicked", self.on_submit)

        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        row.append(self.entry)
        row.append(btn)

        self.root.append(row)
        # ---

        # Output label
        # ---
        self.output = Gtk.Label(label="Output will appear here")
        self.root.append(self.output)
        # ---

        # Menu button
        # ---
        menu_btn = Gtk.MenuButton(label="Menu")

        popover = Gtk.PopoverMenu()
        menu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        about_btn = Gtk.Button(label="About")
        about_btn.connect("clicked", lambda x: print("About clicked"))

        quit_btn = Gtk.Button(label="Quit")
        quit_btn.connect("clicked", lambda x: app.quit())

        menu_box.append(about_btn)
        menu_box.append(quit_btn)

        popover.set_child(menu_box)
        menu_btn.set_popover(popover)

        self.root.append(menu_btn)
        # ---

    def on_submit(self, widget):
        text = self.entry.get_text()
        self.output.set_text(f"You typed: {text}")

class App(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.orcstrate.app")

    def do_activate(self):
        win = MainWindow(self)
        win.present()

app = App()
app.run()