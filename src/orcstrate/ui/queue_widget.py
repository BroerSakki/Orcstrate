import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gio", "2.0")
from gi.repository import Gtk, Gio, GObject, Gdk
from models.command import Command
from core.runner import CommandRunner

class QueueWidget:
	# Constructor
	# ---
	def __init__(self):

		# Create a CSS provider and add it to the display
		style_provider = Gtk.CssProvider()
		style_provider.load_from_data(b"""
			.drag-handle { margin-right: 10px; cursor: grab; opacity: 0.5; }
			.drag-handle:hover { opacity: 1.0; }
			.drop-indicator-top { border-top: 3px solid #3584e4; }
			.drop-indicator-bottom { border-bottom: 3px solid #3584e4; }
			.row-container { padding: 8px; border-bottom: 1px solid alpha(@border_color, 0.5); }
		""")
		Gtk.StyleContext.add_provider_for_display(
			Gdk.Display.get_default(),
			style_provider,
			Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
		)

		# Widget Containers
		# ---
		self.main_hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		# ---

		#ListStore with commands from backend (For example) PS. Switched from ListBox to ListStore, because ListStore has more functionality and only renders item that are visible, making performance imensly better. Meaning we can have 100,000+ commands without lagging
		# ---
		self.list_store = Gio.ListStore(item_type=self.CommandObj)
		self.list_store.append(self.CommandObj(Command(f"Add More Items")))
		# ---

		# List Item Factory
		# ---
		self.factory = Gtk.SignalListItemFactory()
		self.factory.connect("setup", self.setup_list_item)
		self.factory.connect("bind", self.bind_list_item)
		# ---
		# Selection And List View
		# ---
		self.selection = Gtk.SingleSelection(model=self.list_store)
		self.list_view = Gtk.ListView(model=self.selection, factory=self.factory)
		# ---

		# Scroll
		# Add better css here
		# ---
		self.scroll = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
		self.scroll.set_child(self.list_view)
		# ---

		# Widget Containers
		# ---
		self.btn_hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		# ---

		# Add To Queue
		# ---
		self.play_btn = Gtk.Button(label="Play Queue", icon_name="go-next-symbolic")
		self.play_btn.add_css_class("suggested-action")
		self.play_btn.connect("clicked", self.on_play_clicked)
		# ---

		# Remove From Queue
		# ---
		self.delete_btn = Gtk.Button(label="Remove Command", icon_name="user-trash-symbolic")
		self.delete_btn.add_css_class("destructive-action")
		self.delete_btn.connect("clicked", self.on_delete_selected)
		# ---

		# Append to root
		# ---
		self.main_hbox.append(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL))
		self.main_hbox.append(self.scroll)
		self.btn_hbox.append(self.play_btn)
		self.btn_hbox.append(self.delete_btn)
		self.main_hbox.append(self.btn_hbox)
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

	def on_play_clicked(self, btn):
		all_items = [self.list_store.get_item(i).get_command() for i in range(self.list_store.get_n_items())]
		runner = CommandRunner()
		runner.load_commands(all_items)
		runner.run_queue()

	def on_delete_selected(self, btn):
		selected_item = self.selection.get_selected_item()
		if selected_item:
			found, index = self.list_store.find(selected_item)
			if found:
				self.list_store.remove(index)

	def setup_list_item(self, factory, list_item):
		box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		box.add_css_class("row-container")

		handle = Gtk.Image.new_from_icon_name("open-menu-symbolic")
		handle.add_css_class("drag-handle")
		box.append(handle)

		label = Gtk.Label(xalign=0, hexpand=True)
		label.add_css_class("cmd-field")
		label.set_width_chars(30)
		box.append(label)

		name = Gtk.Label(xalign=0, hexpand=True)
		name.add_css_class("tag-field")
		name.set_width_chars(12)
		box.append(name)

		ext_check = Gtk.CheckButton(label="External")
		ext_check.add_css_class("modern-check")
		ext_check.set_sensitive(False)
		box.append(ext_check)
		keep_check = Gtk.CheckButton(label="Keep Open")
		keep_check.add_css_class("modern-check")
		keep_check.set_sensitive(False)
		box.append(keep_check)

		list_item.set_child(box)

		# DRAG SOURCE (Attached ONLY to the handle)
		drag_source = Gtk.DragSource(actions=Gdk.DragAction.MOVE)
		drag_source.connect("prepare", self.on_drag_prepare, list_item)
		drag_source.connect("drag-begin", self.on_drag_begin, box) # Snapshot the whole row
		handle.add_controller(drag_source)

		# DROP TARGET (Attached to the whole BOX for better hit area)
		drop_target = Gtk.DropTarget.new(GObject.TYPE_INT, Gdk.DragAction.MOVE)
		drop_target.connect("enter", self.on_drag_enter)
		drop_target.connect("motion", self.on_drag_motion, list_item)
		drop_target.connect("leave", self.on_drag_leave, list_item)
		drop_target.connect("drop", self.on_drop, list_item)
		box.add_controller(drop_target)

	def bind_list_item(self, factory, list_item):
		item = list_item.get_item()
		box = list_item.get_child()

		handle = box.get_first_child()
		label = handle.get_next_sibling()
		name = label.get_next_sibling()
		ext_check = name.get_next_sibling()
		keep_check = ext_check.get_next_sibling()

		label.set_label(item.command_text)
		name.set_label(item.search_tag)
		ext_check.set_active(item.external)
		keep_check.set_active(item.keep_open)

	def on_drag_enter(self, target, x, y):
		return Gdk.DragAction.MOVE

	def on_drag_motion(self, target, x, y, list_item):
		label = list_item.get_child()
		height = label.get_allocated_height()
	
		# Decide whether to show the indicator at the top or bottom half of the row
		if y < height / 2:
			label.add_css_class("drop-indicator-top")
			label.remove_css_class("drop-indicator-bottom")
		else:
			label.add_css_class("drop-indicator-bottom")
			label.remove_css_class("drop-indicator-top")
		return Gdk.DragAction.MOVE

	def on_drag_leave(self, target, list_item):
		label = list_item.get_child()
		label.remove_css_class("drop-indicator-top")
		label.remove_css_class("drop-indicator-bottom")

	def on_drag_prepare(self, source, x, y, list_item):
		# Implement finding which item is dragged if necessary
		pos = list_item.get_position()
		return Gdk.ContentProvider.new_for_value(pos)
	
	def on_drag_begin(self, source, drag, widget):
		# Create a preview icon from the actual widget
		paintable = Gtk.WidgetPaintable.new(widget)
		source.set_icon(paintable, 0, 0)

	def on_drop(self, target, source_pos, x, y, list_item):
		self.on_drag_leave(target, list_item) # Clean up styles
		dest_pos = list_item.get_position()

		cmd = list_item.get_child()
		if y > cmd.get_allocated_height() / 2:
			dest_pos += 1

		if source_pos == dest_pos or source_pos == dest_pos - 1:
			return False
		
		item = self.list_store.get_item(source_pos)

		# Adjust for removal shifting indices
		insert_idx = dest_pos if dest_pos < source_pos else dest_pos - 1

		self.list_store.remove(source_pos)
		self.list_store.insert(insert_idx, item)
		return True

	def add_command(self, command):
		self.list_store.append(self.CommandObj(command))