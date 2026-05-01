import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Gio", "2.0")
from gi.repository import Gtk, Gio, GObject
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

		#ListStore with commands from backend (For example) PS. Switched from ListBox to ListStore, because ListStore has more functionality and only renders item that are visible, making performance imensly better. Meaning we can have 100,000+ commands without lagging
		# ---
		self.list_store = Gio.ListStore(item_type=self.CommandObj)
		for command in commands:
			self.list_store.append(self.CommandObj(command.command, command.name))
		# ---

		# Search Entry (Hashing functionality added)
		# ---
		self.search_entry = Gtk.SearchEntry()
		# ---

		# Set Custom Filter
		# ---
		custom_filter = Gtk.CustomFilter.new(self.filter_func, self.search_entry)
		filter_model = Gtk.FilterListModel(model=self.list_store, filter=custom_filter)
		# ---

		# Set Filter Function on search change
		# ---
		self.search_entry.connect("search-changed", lambda x: custom_filter.changed(Gtk.FilterChange.DIFFERENT))
		# ---
		
		# List Item Factory
		# ---
		self.factory = Gtk.SignalListItemFactory()
		self.factory.connect("setup", self.setup_list_item)
		self.factory.connect("bind", self.bind_list_item)
		# ---

		# Selection And List View
		# ---
		self.selection = Gtk.SingleSelection(model=filter_model)
		self.list_view = Gtk.ListView(model=self.selection, factory=self.factory)
		# ---

		root.append(self.search_entry)

		# Scroll
		# ---
		self.scroll = Gtk.ScrolledWindow()
		self.scroll.set_child(self.list_view)
		root.append(self.scroll)
		# ---

	class CommandObj(GObject.Object):
		def __init__(self,command, name):
			super().__init__()
			self.command = command
			self.search_tag = name.lower() # Should we make this case sensitive or no?

	def setup_list_item(self, factory, list_item):
		label = Gtk.Label()
		list_item.set_child(label)

	def bind_list_item(self, factory, list_item):
		item = list_item.get_item()
		label = list_item.get_child()
		label.set_text(item.command)

	def filter_func(self, item, search_entry):
		query = search_entry.get_text().lower()
		if not query:
			return True
		# Fast comparison using our pre-processed tag
		return query in item.search_tag