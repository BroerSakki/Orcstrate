import gi
gi.require_version("Gtk", "4.0")
gi.require_version('Vte', '3.91')
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Vte
import os

class TerminalWidget(Gtk.Box):
	def __init__(self):
		box = Gtk.Box(
			orientation=Gtk.Orientation.HORIZONTAL,
			spacing=8
		)

		terminal = Vte.Terminal()
		terminal.spawn_async(
			Vte.PtyFlags.DEFAULT,
			os.environ['HOME'],
			["/bin/bash"],
			[],
			GLib.SpawnFlags.DO_NOT_REAP_CHILD,
			None, None, -1, None, None
		)

		box.append(terminal)

		self.append(box)