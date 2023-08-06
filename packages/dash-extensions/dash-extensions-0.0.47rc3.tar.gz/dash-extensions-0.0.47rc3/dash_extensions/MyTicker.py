# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class MyTicker(Component):
    """A MyTicker component.
A modified version of dcc.Link that adds a few more options. E.g. you can disable scrolling to
the top upon updating the url.

Keyword arguments:
- children (a list of or a singular dash component, string or number; optional): The children of this component
- direction (a value equal to: "toRight", "toLeft"; optional)
- mode (a value equal to: "chain", "await", "smooth"; optional)
- move (boolean; optional)
- offset (a value equal to: PropTypes.number, PropTypes.string; optional)
- speed (number; optional)
- height (a value equal to: PropTypes.number, PropTypes.string; optional)
- id (string; optional): The ID used to identify this component in Dash callbacks
- className (string; optional): The class of the component"""
    @_explicitize_args
    def __init__(self, children=None, direction=Component.UNDEFINED, mode=Component.UNDEFINED, move=Component.UNDEFINED, offset=Component.UNDEFINED, speed=Component.UNDEFINED, height=Component.UNDEFINED, id=Component.UNDEFINED, className=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'direction', 'mode', 'move', 'offset', 'speed', 'height', 'id', 'className']
        self._type = 'MyTicker'
        self._namespace = 'dash_extensions'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'direction', 'mode', 'move', 'offset', 'speed', 'height', 'id', 'className']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(MyTicker, self).__init__(children=children, **args)
