# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Select(Component):
    """A Select component.
Select is a dash wrapper for the html select tag.

Keyword arguments:
- id (string; required): The ID used to identify this compnent in Dash callbacks
- size (number; default 4): The number of visible options
- options (dict; optional): An array of options {label: [string|number], value: [string|number]},
an optional disabled field can be used for each option. options has the following type: list of dicts containing keys 'label', 'value'.
Those keys have the following types:
  - label (string | number; required): The dropdown's label
  - value (string | number; required): The value of the dropdown. This value
corresponds to the items specified in the
`value` property.
- value (string | number | list of strings; optional): The value of the input. If `multi` is false
then value is just a string that corresponds to the values
provided in the `options` property. If `multi` is true, then
multiple values can be selected at once, and `value` is an
array of items with values corresponding to those in the
`options` prop.
- multi (boolean; default True): If true, the user can select multiple values
- className (string; default ""): Appends a class to the select tag
- style (dict; optional): Appends styles to the select tag
- parent_className (string; default ""): Appends a class to the wrapping div
- parent_style (dict; optional): Appends inline styles to the wrapping div
- persistence (boolean | string | number; optional): Used to allow user interactions in this component to be persisted when
the component - or the page - is refreshed. If `persisted` is truthy and
hasn't changed from its previous value, a `value` that the user has
changed while using the app will keep that change, as long as
the new `value` also matches what was given originally.
Used in conjunction with `persistence_type`.
- persisted_props (list of a value equal to: "value"s; default ["value"]): Properties whose user interactions will persist after refreshing the
component or the page. Since only `value` is allowed this prop can
normally be ignored.
- persistence_type (a value equal to: "local", "session", "memory"; default "local"): Where persisted user changes will be stored:
memory: only kept in memory, reset on page refresh.
local: window.localStorage, data is kept after the browser quit.
session: window.sessionStorage, data is cleared once the browser quit."""
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, size=Component.UNDEFINED, options=Component.UNDEFINED, value=Component.UNDEFINED, multi=Component.UNDEFINED, className=Component.UNDEFINED, style=Component.UNDEFINED, parent_className=Component.UNDEFINED, parent_style=Component.UNDEFINED, persistence=Component.UNDEFINED, persisted_props=Component.UNDEFINED, persistence_type=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'size', 'options', 'value', 'multi', 'className', 'style', 'parent_className', 'parent_style', 'persistence', 'persisted_props', 'persistence_type']
        self._type = 'Select'
        self._namespace = 'webviz_core_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'size', 'options', 'value', 'multi', 'className', 'style', 'parent_className', 'parent_style', 'persistence', 'persisted_props', 'persistence_type']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Select, self).__init__(**args)
