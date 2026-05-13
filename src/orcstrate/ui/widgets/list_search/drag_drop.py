from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject


class ListSearchDragDrop:

    def __init__(self, source_model, selection_model):
        self.source_model = source_model
        self.selection_model = selection_model

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

        # Resolve the destination position in the filter/selection model
        dest_pos = list_item.get_position()

        row = list_item.get_child()

        if y > row.get_allocated_height() / 2:
            dest_pos += 1

        # Get the actual item at the source position
        item = self.selection_model.get_item(source_pos)

        if item is None:
            return False

        # Find the item's position in the source model
        found, source_source_pos = self.source_model.find(item)

        if not found:
            return False

        # Find the item at the destination position in the filter/selection model
        # If dest_pos is beyond the filtered model, insert at the end
        if dest_pos < self.selection_model.get_n_items():
            dest_item = self.selection_model.get_item(dest_pos)

            if dest_item is not None:
                found, dest_source_pos = self.source_model.find(dest_item)

                if not found:
                    return False
            else:
                # Append to end of source model
                self.source_model.remove(source_source_pos)
                self.source_model.append(item)
                return True
        else:
            # Append to end of source model
            self.source_model.remove(source_source_pos)
            self.source_model.append(item)
            return True

        # Adjust insert index if the source was before the destination
        if source_source_pos < dest_source_pos:
            insert_idx = dest_source_pos - 1
        else:
            insert_idx = dest_source_pos

        # Guard against out-of-bounds
        if insert_idx < 0:
            insert_idx = 0

        self.source_model.remove(source_source_pos)
        self.source_model.insert(insert_idx, item)

        return True