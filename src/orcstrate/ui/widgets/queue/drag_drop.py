from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject


class QueueDragDrop:

    def __init__(self, list_store):
        self.list_store = list_store

    def setup_drag_and_drop(
        self,
        row,
        list_item
    ):

        drag_source = Gtk.DragSource(
            actions=Gdk.DragAction.MOVE
        )

        drag_source.connect(
            "prepare",
            self.on_drag_prepare,
            list_item
        )

        drag_source.connect(
            "drag-begin",
            self.on_drag_begin,
            row
        )

        row.handle.add_controller(
            drag_source
        )

        drop_target = Gtk.DropTarget.new(
            GObject.TYPE_INT,
            Gdk.DragAction.MOVE
        )

        drop_target.connect(
            "motion",
            self.on_drag_motion,
            list_item
        )

        drop_target.connect(
            "leave",
            self.on_drag_leave,
            list_item
        )

        drop_target.connect(
            "drop",
            self.on_drop,
            list_item
        )

        row.add_controller(drop_target)

    def on_drag_prepare(
        self,
        source,
        x,
        y,
        list_item
    ):
        pos = list_item.get_position()

        return Gdk.ContentProvider.new_for_value(
            pos
        )

    def on_drag_begin(
        self,
        source,
        drag,
        row
    ):
        paintable = Gtk.WidgetPaintable.new(
            row
        )

        source.set_icon(
            paintable,
            0,
            0
        )

    def on_drag_motion(
        self,
        target,
        x,
        y,
        list_item
    ):

        row = list_item.get_child()

        height = row.get_allocated_height()

        if y < height / 2:
            row.add_css_class(
                "drop-indicator-top"
            )

            row.remove_css_class(
                "drop-indicator-bottom"
            )

        else:
            row.add_css_class(
                "drop-indicator-bottom"
            )

            row.remove_css_class(
                "drop-indicator-top"
            )

        return Gdk.DragAction.MOVE

    def on_drag_leave(
        self,
        target,
        list_item
    ):
        row = list_item.get_child()

        row.remove_css_class(
            "drop-indicator-top"
        )

        row.remove_css_class(
            "drop-indicator-bottom"
        )

    def on_drop(
        self,
        target,
        source_pos,
        x,
        y,
        list_item
    ):

        self.on_drag_leave(
            target,
            list_item
        )

        dest_pos = list_item.get_position()

        row = list_item.get_child()

        if y > row.get_allocated_height() / 2:
            dest_pos += 1

        if (
            source_pos == dest_pos
            or
            source_pos == dest_pos - 1
        ):
            return False

        item = self.list_store.get_item(
            source_pos
        )

        insert_idx = (
            dest_pos
            if dest_pos < source_pos
            else dest_pos - 1
        )

        self.list_store.remove(source_pos)

        self.list_store.insert(
            insert_idx,
            item
        )

        return True