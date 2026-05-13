from gi.repository import Gtk
from ui.widgets.list_search.widget import ListSearchWidget
from ui.widgets.queue.widget import QueueWidget
from ui.dialogs.save_dialog import SaveDialog
from ui.dialogs.load_dialog import LoadDialog


class MainWindow(Gtk.ApplicationWindow):

    def __init__(self, app, command_service, queue_service, workspace):
        super().__init__(application=app)
        self.workspace = workspace
        self.set_title("Orcstrate")
        self.set_default_size(1700, 800)

        root = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12
        )
        header = Gtk.HeaderBar()
        self.set_titlebar(header)

        save_btn = Gtk.Button(icon_name="document-save-symbolic")
        save_as_btn = Gtk.Button(icon_name="document-save-as-symbolic")
        load_btn = Gtk.Button(icon_name="document-open-symbolic")

        save_btn.connect(
            "clicked",
            self.on_save_clicked
        )
        save_as_btn.connect(
            "clicked",
            self.on_save_as_clicked
        )
        load_btn.connect(
            "clicked",
            self.on_load_clicked
        )

        header.pack_start(load_btn)
        header.pack_start(save_btn)
        header.pack_start(save_as_btn)
        
        self.set_margin_top(16)
        self.set_margin_bottom(16)
        self.set_margin_start(16)
        self.set_margin_end(16)

        self.set_child(root)

        queue_widget = QueueWidget(queue_service=queue_service)

        list_widget = ListSearchWidget(
            command_service,
            queue_service
        )

        root.append(list_widget)
        root.append(queue_widget)

    # Event handlers
    # ---
    def on_save_clicked(self, btn):
    
        # Existing file?
        if self.workspace.filepath:
        
            self.workspace.save()
            print("[INFO] Workspace saved")
            return
        dialog = SaveDialog(
            self,
            self.save_workspace
        )
        dialog.show()
    def on_load_clicked(self, btn):
    
        dialog = LoadDialog(
            self,
            self.load_workspace
        )
        dialog.show()

    def on_save_as_clicked(self, btn):
        dialog = SaveDialog(
            self,
            self.save_workspace
        )

        dialog.show()

    def on_save_dialog_response(
        self,
        dialog,
        result
    ):
        try:
        
            file = dialog.save_finish(result)
            path = file.get_path()
            if not path.endswith(".orc"):
            
                path += ".orc"
            self.workspace.save_as(path)
            print(
                f"[INFO] Saved workspace: {path}"
            )
        except Exception as e:
        
            print(f"[ERROR] {e}")

    def on_load_dialog_response(
        self,
        dialog,
        result
    ):
    
        try:
        
            file = dialog.open_finish(result)
    
            path = file.get_path()
    
            self.workspace.load(path)
    
            print(
                f"[INFO] Loaded workspace: {path}"
            )
    
        except Exception as e:
        
            print(f"[ERROR] {e}")
        # ---
        
    # Callbacks
    # ---
    def save_workspace(self, path):
    
        self.workspace.save_as(path)
    
        print(
            f"[INFO] Saved workspace: {path}"
        )
    def load_workspace(self, path):
    
        self.workspace.load(path)
        print(
            f"[INFO] Loaded workspace: {path}"
        )
    # ---