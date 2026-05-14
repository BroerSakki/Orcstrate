import gi
gi.require_version("Gtk", "4.0")
gi.require_version('Vte', '3.91')
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Vte
import os

from core.queue_service import (
	QueueService
)

class TerminalWidget(Gtk.Box):
	def __init__(self, queue_service):
		super().__init__(
			orientation=Gtk.Orientation.VERTICAL,
			spacing=12
		)

		self.queue_service:QueueService = queue_service

		self.terminal = Vte.Terminal()
		self.terminal.set_height_request(100)

		shell_bin = os.environ.get("SHELL", "/bin/sh")
		argv = [shell_bin]
		working_dir = os.environ.get("HOME", "/")

		self.terminal.spawn_async(
			Vte.PtyFlags.DEFAULT,
			working_dir,
			argv,
			None,
			GLib.SpawnFlags.DEFAULT,
			None, None,
			-1,
			None,
			None,
			None
		)

		self.build_ui()

	def build_ui(self):
		box = Gtk.Box(
			orientation=Gtk.Orientation.HORIZONTAL,
			spacing=8
		)

		box.append(self.terminal)

		play_btn = Gtk.Button(
			label="Play Queue",
			icon_name="media-playback-start-symbolic"
		)

		play_btn.add_css_class(
			"suggested-action"
		)

		play_btn.connect(
			"clicked",
			self.on_play_clicked
		)

		box.append(play_btn)

		self.append(box)

	def on_play_clicked(self, btn):
		self.queue_service.run_queue(self.terminal)
		#self.run_internal("echo Test")