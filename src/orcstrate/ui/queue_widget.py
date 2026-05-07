import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Gio", "2.0")
from gi.repository import Gtk, Gio, GObject, Gdk
from models.command import Command

class QueueWidget:
	# Constructor
	# ---
	def __init__(self, root):

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
		main_hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		# ---

		#ListStore with commands from backend (For example) PS. Switched from ListBox to ListStore, because ListStore has more functionality and only renders item that are visible, making performance imensly better. Meaning we can have 100,000+ commands without lagging
		# ---
		self.list_store = Gio.ListStore(item_type=self.CommandObj)
		for i in range(10):
			self.list_store.append(self.CommandObj(Command(f"Item {i+1}")))
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

		# Append to root
		# ---
		main_hbox.append(self.scroll)

		root.append(main_hbox)
		# ---

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
			self.search_tag = command.name.lower() # Should we make this case sensitive or no?
			self.external = command.external
			self.keep_open = command.keep_open

	def setup_list_item(self, factory, list_item):
		box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		box.add_css_class("row-container")

		handle = Gtk.Image.new_from_icon_name("open-menu-symbolic")
		handle.add_css_class("drag-handle")
		box.append(handle)

		label = Gtk.Label(xalign=0, hexpand=True)
		box.append(label)

		list_item.set_child(box)

		# DRAG SOURCE (Attached ONLY to the handle)
		drag_source = Gtk.DragSource(actions=Gdk.DragAction.MOVE)
		drag_source.connect("prepare", self.on_drag_prepare, list_item)
		drag_source.connect("drag-begin", self.on_drag_begin, box) # Snapshot the whole row
		handle.add_controller(drag_source)

		# DROP TARGET (Attached to the whole BOX for better hit area)
		drop_target = Gtk.DropTarget.new(GObject.TYPE_UINT, Gdk.DragAction.MOVE)
		drop_target.connect("enter", self.on_drag_enter)
		drop_target.connect("motion", self.on_drag_motion, list_item)
		drop_target.connect("leave", self.on_drag_leave, list_item)
		drop_target.connect("drop", self.on_drop, list_item)
		box.add_controller(drop_target)

	def bind_list_item(self, factory, list_item):
		item = list_item.get_item()
		box = list_item.get_child()
		label = box.get_last_child()
		label.set_label(item.command_text)

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