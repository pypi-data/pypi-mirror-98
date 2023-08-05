from .utils import encode_attr
from .control import Control
from .alignment import Alignment

class Stack(Control):

    def __init__(self, controls=[], id=None, horizontal=None, vertical_fill=None, horizontal_align=None,
            vertical_align=None, gap=None, wrap=None,
            width=None, height=None, padding=None, margin=None,
            visible=None, disabled=None):
        Control.__init__(self, id=id,
            width=width, height=height, padding=padding, margin=margin,
            visible=visible, disabled=disabled)

        self.horizontal = horizontal
        self.vertical_fill = vertical_fill
        self.horizontal_align = horizontal_align
        self.vertical_align = vertical_align
        self.gap = gap
        self.wrap = wrap

        self._controls = []
        if controls and len(controls) > 0:
            for control in controls:
                self.add_control(control)

    def _getControlName(self):
        return "stack"

    def add_control(self, control):
        if not isinstance(control, Control):
            raise Exception("Stack can hold controls only")

        self._controls.append(control)

# gap
    @property
    def gap(self):
        return self._get_attr("gap")

    @gap.setter
    def gap(self, value):
        self._set_attr("gap", value)

# wrap
    @property
    def wrap(self):
        return self._get_attr("wrap")

    @wrap.setter
    def wrap(self, value):
        assert value == None or isinstance(value, bool), "wrap must be a bool"
        self._set_attr("wrap", value)

# horizontal
    @property
    def horizontal(self):
        return self._get_attr("horizontal")

    @horizontal.setter
    def horizontal(self, value):
        assert value == None or isinstance(value, bool), "horizontal must be a bool"
        self._set_attr("horizontal", value)

# vertical_fill
    @property
    def vertical_fill(self):
        return self._get_attr("verticalFill")

    @vertical_fill.setter
    def vertical_fill(self, value):
        assert value == None or isinstance(value, bool), "verticalFill must be a bool"
        self._set_attr("verticalFill", value)

# horizontal_align
    @property
    def horizontal_align(self):
        return self._get_attr("horizontalAlign")

    @horizontal_align.setter
    def horizontal_align(self, value):
        assert value == None or isinstance(value, Alignment), "horizontalAlign must be an Alignment"
        self._set_attr("horizontalAlign", value)

# vertical_align
    @property
    def vertical_align(self):
        return self._get_attr("verticalAlign")

    @vertical_align.setter
    def vertical_align(self, value):
        assert value == None or isinstance(value, Alignment), "verticalAlign must be an Alignment"
        self._set_attr("verticalAlign", value)

    def _getChildren(self):
        return self._controls