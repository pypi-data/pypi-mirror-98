import typing
from nion.ui import Declarative
from nion.utils import ListModel
from nion.utils import Model


class Shape:
    def __init__(self):
        self.type = "shape"
        self.label = "Shape"

class Rectangle(Shape):
    def __init__(self):
        super().__init__()
        self.type = "rectangle"
        self.label = "Rectangle"
        self.width = 100
        self.height = 90


class Circle(Shape):
    def __init__(self):
        super().__init__()
        self.type = "circle"
        self.label = "Circle"
        self.radius = 45


class Interval(Shape):
    def __init__(self):
        super().__init__()
        self.type = "interval"
        self.label = "Interval"
        self.left = 55
        self.right = 70


class ShapeHandler:

    def __init__(self, shape: Shape):
        self.shape = shape


class Handler:

    def __init__(self):
        # define our list of shapes, one from each class
        self.shapes_model = ListModel.ListModel(items=[Rectangle(), Circle(), Interval()])

        # define the shape index model
        self.shape_index_model = Model.PropertyModel(0)

        # define the shape page model
        self.shape_page = Model.PropertyModel()

        def shape_index_changed(p: str = None) -> None:
            self.shape_page.value = self.shapes_model.items[self.shape_index_model.value].type

        shape_index_changed()

        # track changes to shape index and update shape page.
        self.__shape_index_changed = self.shape_index_model.property_changed_event.listen(shape_index_changed)

    def close(self):
        self.__shape_index_changed.close()
        self.__shape_index_changed = None

    def create_handler(self, component_id: str, container=None, item=None, **kwargs):
        if component_id in ("shape", "rectangle", "circle", "interval"):
            item = self.shapes_model.items[self.shape_index_model.value]
            return ShapeHandler(item)
        return None

    def get_resource(self, resource_id: str, container=None, item=None) -> typing.Optional[Declarative.UIDescription]:
        u = Declarative.DeclarativeUI()
        if resource_id == "rectangle":
            width_row = u.create_row(u.create_label(text="Width:"), u.create_label(text="@binding(shape.width)"), spacing=8)
            height_row = u.create_row(u.create_label(text="Height:"), u.create_label(text="@binding(shape.height)"), spacing=8)
            return u.define_component(u.create_group(u.create_column(width_row, height_row, spacing=8), title="@binding(shape.label)"))
        elif resource_id == "circle":
            radius_row = u.create_row(u.create_label(text="Radius:"), u.create_label(text="@binding(shape.radius)"), spacing=8)
            return u.define_component(u.create_group(u.create_column(radius_row, spacing=8), title="@binding(shape.label)"))
        elif resource_id == "interval":
            left_row = u.create_row(u.create_label(text="Left:"), u.create_label(text="@binding(shape.left)"), spacing=8)
            right_row = u.create_row(u.create_label(text="Right:"), u.create_label(text="@binding(shape.right)"), spacing=8)
            return u.define_component(u.create_group(u.create_column(left_row, right_row, spacing=8), title="@binding(shape.label)"))
        return None


def construct_ui(ui: Declarative.DeclarativeUI):
    shape_choice = ui.create_combo_box(items=["Rectangle", "Circle", "Interval"], current_index="@binding(shape_index_model.value)")
    shape_component = ui.create_component_instance("@binding(shape_page.value)")
    return ui.create_column(shape_choice, shape_component, spacing=8, margin=12)
