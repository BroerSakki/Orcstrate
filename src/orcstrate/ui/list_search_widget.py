import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from models.command import Command

"""
This acts as an example and tutorial for developing future widgets

window.py will hold all widgets together. So one thing we can do is have different layouts for the app.
So for instance we want a version of the app that only shows the currently playing queue, we can only use that essential widget.

Each widget should be preferrably only be called by its class name with arguments (So it looks cleaner), so in other words use __init__ as function that builds entire widget.
Always include a root parameter in __init__, because this is essential to be able to add to main window (As shown below with the root.append())
If variables from backend is required, add it as a parameter in the __init__ function (As shown with commands below)

As Izak mentioned, when building a widget, don't add single line stuff (Like only a SearchBar or something). That can just be added to window.py directly

Remember to HAVE FUN :)
"""

class ListSearchWidget:
	# Constructor
	# ---
	def __init__(self, root, commands: list[Command]):
		# Search Entry (Actual search functionality still needs to be implemented)
		# ---
		search_entry = Gtk.SearchEntry()
		root.append(search_entry)
		# ---

		# ListBox with commands from backend (For example)
		# ---
		list_box = Gtk.ListBox()

		for command in commands:
			row = Gtk.ListBoxRow()
			label = Gtk.Label(label=f"Item {command.name}")
			row.set_child(label)
			list_box.append(row)

		root.append(list_box)
		# ---
	# ---