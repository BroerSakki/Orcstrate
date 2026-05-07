import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gio", "2.0")
from gi.repository import Gtk, Gio, GObject, Gdk
from models.command import Command
from ui.queue_widget import QueueWidget

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
	def __init__(self, commands: list[Command], queue_ref):
		# Css
		# ---
		css_provider = Gtk.CssProvider()
		css_provider.load_from_path("src/orcstrate/ui/list_search_widget.css")
		Gtk.StyleContext.add_provider_for_display(
			Gdk.Display.get_default(), 
			css_provider, 
			Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
		)
		# ---

		# Widget Containers
		# ---
		self.main_hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		content_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
		# ---

		#ListStore with commands from backend (For example) PS. Switched from ListBox to ListStore, because ListStore has more functionality and only renders item that are visible, making performance imensly better. Meaning we can have 100,000+ commands without lagging
		# ---
		self.list_store = Gio.ListStore(item_type=self.CommandObj)
		for command in commands:
			self.list_store.append(self.CommandObj(command))
		# ---

		# Search Entry (Hashing functionality added)
		# ---
		self.search_entry = Gtk.SearchEntry()
		self.search_entry.set_halign(Gtk.Align.CENTER)
		self.search_entry.set_max_width_chars(20)
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

		# Scroll
		# Add better css here
		# ---
		self.scroll = Gtk.ScrolledWindow()
		self.scroll.set_propagate_natural_height(True)
		self.scroll.set_hexpand(True)
		self.scroll.set_vexpand(True)
		self.scroll.set_child(self.list_view)
		# ---

		self.queue_ref = queue_ref

		# Sidebar for buttons
		# ---
		sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
		sidebar.set_size_request(150, -1)
		sidebar.add_css_class("sidebar") # Optional: style with CSS later
		sidebar.set_margin_end(10)
		# ---
		# Add Button
		# ---
		add_btn = Gtk.Button(label="Add Command", icon_name="list-add-symbolic")
		add_btn.connect("clicked", self.on_add_clicked)
		# ---
		# Delete Button
		# ---
		self.del_btn = Gtk.Button(label="Delete Selected", icon_name="user-trash-symbolic")
		self.del_btn.add_css_class("destructive-action")
		self.del_btn.connect("clicked", self.on_delete_selected)
		# ---
		# Add To Queue
		# ---
		self.add_queue_btn = Gtk.Button(label="Add To Queue", icon_name="go-next-symbolic")
		self.add_queue_btn.add_css_class("suggested-action")
		self.add_queue_btn.connect("clicked", self.on_add_queue_clicked)
		# ---
		# Add Buttons to sidebar
		# ---
		sidebar.append(add_btn)
		sidebar.append(self.del_btn)
		sidebar.append(self.add_queue_btn)
		# ---

		# Append to root
		# ---
		self.main_hbox.append(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL))
		self.main_hbox.append(self.search_entry)
		content_hbox.append(self.scroll)
		content_hbox.append(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL))
		content_hbox.append(sidebar)
		self.main_hbox.append(content_hbox)
		# ---

	def __call__(self):
		return self.main_hbox

	class CommandObj(GObject.Object):
		# Command Variables
		# ---
		command_text = GObject.Property(type=str)
		search_tag = GObject.Property(type=str)
		external = GObject.Property(type=bool, default=False)
		keep_open = GObject.Property(type=bool, default=False)
		# ---

		def __init__(self,command: Command):
			super().__init__()
			self.command_text = command.command
			self.search_tag = command.name # Should we make this case sensitive or no?
			self.external = command.external
			self.keep_open = command.keep_open

		def get_command(self):
			return Command(self.command_text, self.external, self.keep_open, self.search_tag)

	def on_add_clicked(self, btn):
		"""Appends a new blank command to the store."""
		new_cmdObj = self.CommandObj(Command(""))
		self.list_store.append(new_cmdObj)
		self.search_entry.set_text("") 
		self.selection.set_selected(self.list_store.get_n_items() - 1)

	def on_delete_selected(self, btn):
		"""Remove selected item"""
		selected_item = self.selection.get_selected_item()
		if selected_item:
			found, index = self.list_store.find(selected_item)
			if found:
				self.list_store.remove(index)

	def on_add_queue_clicked(self, btn):
		"""Needs to be added"""
		selected_item = self.selection.get_selected_item()
		if selected_item:
			self.queue_ref.add_command(selected_item.get_command())

	def on_load_clicked(self):
		path = self.file_dialog.open()
		if path:
			self.workspace.load(path)
			self.refresh_ui()

	def on_save_clicked(self):
		self.workspace.save()

	def on_save_as_clicked(self):
		path = self.file_dialog.save()
	
		if path:
			self.workspace.save_as(path)

	def setup_list_item(self, factory, list_item):
		box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
		box.add_css_class("command-row")

		cmd_edit = Gtk.EditableLabel()
		cmd_edit.add_css_class("cmd-field")
		cmd_edit.set_width_chars(30)
		cmd_edit.set_hexpand(True)
		cmd_edit.set_tooltip_text("Edit Command")

		tag_edit = Gtk.EditableLabel()
		tag_edit.add_css_class("tag-field")
		tag_edit.set_width_chars(12)
		tag_edit.set_tooltip_text("Edit Search Tag")

		ext_check = Gtk.CheckButton(label="External")
		ext_check.add_css_class("modern-check")
		keep_check = Gtk.CheckButton(label="Keep Open")
		keep_check.add_css_class("modern-check")

		box.append(cmd_edit)
		box.append(tag_edit)
		box.append(ext_check)
		box.append(keep_check)

		list_item.set_child(box)

	def bind_list_item(self, factory, list_item):
		item = list_item.get_item()
		box = list_item.get_child()

		cmd_edit = box.get_first_child()
		tag_edit = cmd_edit.get_next_sibling()
		ext_check = tag_edit.get_next_sibling()
		keep_check = ext_check.get_next_sibling()

		item.bind_property("command_text", cmd_edit, "text", GObject.BindingFlags.BIDIRECTIONAL | GObject.BindingFlags.SYNC_CREATE)
		item.bind_property("search_tag", tag_edit, "text", GObject.BindingFlags.BIDIRECTIONAL | GObject.BindingFlags.SYNC_CREATE)
		item.bind_property("external", ext_check, "active", GObject.BindingFlags.BIDIRECTIONAL | GObject.BindingFlags.SYNC_CREATE)
		item.bind_property("keep_open", keep_check, "active", GObject.BindingFlags.BIDIRECTIONAL | GObject.BindingFlags.SYNC_CREATE)

	def print_data(self, btn):
		print("\n--- Current Command List Data ---")
		for i in range(self.list_store.get_n_items()):
			obj = self.list_store.get_item(i)
			print(f"[{i}] '{obj.command_text}' (Tag: {obj.search_tag}) | Ext: {obj.external} | Keep: {obj.keep_open}")

	def filter_func(self, item, search_entry):
		query = search_entry.get_text().lower()
		if not query:
			return True
		# Fast comparison using pre-processed tag
		return query in item.search_tag.lower()