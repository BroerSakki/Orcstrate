import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

class SearchBarWindow(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title("GTK 4 SearchBar Example")
        self.set_default_size(400, 200)

        # 1. Main layout container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(main_box)

        # 2. Setup the SearchEntry and SearchBar
        self.search_entry = Gtk.SearchEntry()
        self.search_bar = Gtk.SearchBar()
        self.search_bar.set_child(self.search_entry)
        self.search_bar.connect_entry(self.search_entry)
        
        # 3. Enable key capture so typing opens the search bar
        self.search_bar.set_key_capture_widget(self)

        # 4. Add SearchBar to the UI (usually at the top)
        main_box.append(self.search_bar)
        
        # Add a placeholder label for content
        label = Gtk.Label(label="Start typing to search...")
        main_box.append(label)

        # 5. Connect signals to handle search logic
        self.search_entry.connect("search-changed", self.on_search_changed)

    def on_search_changed(self, entry):
        text = entry.get_text()
        print(f"Searching for: {text}")

def on_activate(app):
    win = SearchBarWindow(application=app)
    win.present()

app = Gtk.Application(application_id='com.example.SearchBar')
app.connect('activate', on_activate)
app.run(None)