from .utils import encode_attr
from .control import Control

class SearchBox(Control):
    def __init__(self, id=None, value=None, placeholder=None, underlined=None,
            icon=None, icon_color=None, data=None, on_change=None, onsearch=None,
            onclear=None, onescape=None, onchange=None,
            width=None, height=None, padding=None, margin=None,
            visible=None, disabled=None):

        Control.__init__(self, id=id,
            width=width, height=height, padding=padding, margin=margin,
            visible=visible, disabled=disabled)

        self.value = value
        self.placeholder = placeholder
        self.underlined = underlined
        self.icon = icon
        self.icon_color = icon_color
        self.data = data
        self.on_change = on_change
        self.onsearch = onsearch
        self.onclear = onclear
        self.onescape = onescape
        self.onchange = onchange

    def _getControlName(self):
        return "searchbox"

# onsearch
    @property
    def onsearch(self):
        return None

    @onsearch.setter
    def onsearch(self, handler):
        self._add_event_handler("search", handler)

# onclear
    @property
    def onclear(self):
        return None

    @onclear.setter
    def onclear(self, handler):
        self._add_event_handler("clear", handler)

# onescape
    @property
    def onescape(self):
        return None

    @onescape.setter
    def onescape(self, handler):
        self._add_event_handler("escape", handler)

# onchange
    @property
    def onchange(self):
        return None

    @onchange.setter
    def onchange(self, handler):
        self._add_event_handler("change", handler)

# value
    @property
    def value(self):
        return self._get_attr("value")

    @value.setter
    def value(self, value):
        self._set_attr("value", value)

# placeholder
    @property
    def placeholder(self):
        return self._get_attr("placeholder")

    @placeholder.setter
    def placeholder(self, value):
        self._set_attr("placeholder", value)

# underlined
    @property
    def underlined(self):
        return self._get_attr("underlined")

    @underlined.setter
    def underlined(self, value):
        assert value == None or isinstance(value, bool), "value must be a boolean"
        self._set_attr("underlined", value)

# icon
    @property
    def icon(self):
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value):
        self._set_attr("icon", value)

# icon_color
    @property
    def icon_color(self):
        return self._get_attr("iconColor")

    @icon_color.setter
    def icon_color(self, value):
        self._set_attr("iconColor", value)

# data
    @property
    def data(self):
        return self._get_attr("data")

    @data.setter
    def data(self, value):
        self._set_attr("data", value)

# on_change
    @property
    def on_change(self):
        return self._get_attr("onChange")

    @on_change.setter
    def on_change(self, value):
        assert value == None or isinstance(value, bool), "value must be a boolean"
        self._set_attr("onChange", value)

