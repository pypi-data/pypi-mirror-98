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

    def create_handler(self, component_id: str, container=None, item=None, **kwargs):
        if component_id in ("shape", "rectangle", "circle", "interval"):
            return ShapeHandler(item)
        return None

    def get_resource(self, resource_id: str, container=None, item=None) -> typing.Optional[Declarative.UIDescription]:
        u = Declarative.DeclarativeUI()
        if resource_id == "shape":
            if item.type == "rectangle":
                width_row = u.create_row(u.create_label(text="Width:"), u.create_label(text="@binding(shape.width)"), spacing=8)
                height_row = u.create_row(u.create_label(text="Height:"), u.create_label(text="@binding(shape.height)"), spacing=8)
                return u.define_component(u.create_group(u.create_column(width_row, height_row, spacing=8), title="@binding(shape.label)"))
            elif item.type == "circle":
                radius_row = u.create_row(u.create_label(text="Radius:"), u.create_label(text="@binding(shape.radius)"), spacing=8)
                return u.define_component(u.create_group(u.create_column(radius_row, spacing=8), title="@binding(shape.label)"))
            elif item.type == "interval":
                left_row = u.create_row(u.create_label(text="Left:"), u.create_label(text="@binding(shape.left)"), spacing=8)
                right_row = u.create_row(u.create_label(text="Right:"), u.create_label(text="@binding(shape.right)"), spacing=8)
                return u.define_component(u.create_group(u.create_column(left_row, right_row, spacing=8), title="@binding(shape.label)"))
        return None


def construct_ui(ui: Declarative.DeclarativeUI):
    shape_components = ui.create_column(items="shapes_model.items", item_component_id="shape", spacing=8)
    return ui.create_column(shape_components, spacing=8, margin=12)
