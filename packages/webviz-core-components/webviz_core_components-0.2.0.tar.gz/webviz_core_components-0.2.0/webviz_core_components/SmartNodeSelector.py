# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class SmartNodeSelector(Component):
    """A SmartNodeSelector component.
SmartNodeSelector is a component that allows to create tags by selecting data from a tree structure.
The tree structure can also provide meta data that is displayed as color or icon.

Keyword arguments:
- id (string; required): The ID used to identify this component in Dash callbacks.
- maxNumSelectedNodes (number; default -1): The max number of tags that can be selected.
- delimiter (string; default ":"): The delimiter used to separate input levels.
- numMetaNodes (number; default 0): The number of meta data used. Meta data is not shown as text in the final tag but used
to set properties like border color or icons.
- data (list; required): A JSON object holding all tags.
- label (string; required): A label that will be printed when this component is rendered.
- showSuggestions (boolean; default True): Stating of suggestions should be shown or not.
- selectedNodes (list of strings; optional): Selected nodes - readonly.
- selectedTags (list of strings; optional): Selected tags.
- selectedIds (list of strings; optional): Selected ids.
- placeholder (string; default "Add new tag..."): Placeholder text for input field.
- numSecondsUntilSuggestionsAreShown (number; default 1.5): Number of seconds until suggestions are shown.
- persistence (boolean | string | number; optional): Used to allow user interactions in this component to be persisted when
the component - or the page - is refreshed. If `persisted` is truthy and
hasn't changed from its previous value, a `value` that the user has
changed while using the app will keep that change, as long as
the new `value` also matches what was given originally.
Used in conjunction with `persistence_type`.
- persisted_props (list of a value equal to: 'selectedNodes', 'selectedTags', 'selectedIds's; default ['selectedNodes', 'selectedTags', 'selectedIds']): Properties whose user interactions will persist after refreshing the
component or the page. Since only `value` is allowed this prop can
normally be ignored.
- persistence_type (a value equal to: 'local', 'session', 'memory'; default 'local'): Where persisted user changes will be stored:
memory: only kept in memory, reset on page refresh.
local: window.localStorage, data is kept after the browser quit.
session: window.sessionStorage, data is cleared once the browser quit."""
    @_explicitize_args
    def __init__(self, id=Component.REQUIRED, maxNumSelectedNodes=Component.UNDEFINED, delimiter=Component.UNDEFINED, numMetaNodes=Component.UNDEFINED, data=Component.REQUIRED, label=Component.REQUIRED, showSuggestions=Component.UNDEFINED, selectedNodes=Component.UNDEFINED, selectedTags=Component.UNDEFINED, selectedIds=Component.UNDEFINED, placeholder=Component.UNDEFINED, numSecondsUntilSuggestionsAreShown=Component.UNDEFINED, persistence=Component.UNDEFINED, persisted_props=Component.UNDEFINED, persistence_type=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'maxNumSelectedNodes', 'delimiter', 'numMetaNodes', 'data', 'label', 'showSuggestions', 'selectedNodes', 'selectedTags', 'selectedIds', 'placeholder', 'numSecondsUntilSuggestionsAreShown', 'persistence', 'persisted_props', 'persistence_type']
        self._type = 'SmartNodeSelector'
        self._namespace = 'webviz_core_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'maxNumSelectedNodes', 'delimiter', 'numMetaNodes', 'data', 'label', 'showSuggestions', 'selectedNodes', 'selectedTags', 'selectedIds', 'placeholder', 'numSecondsUntilSuggestionsAreShown', 'persistence', 'persisted_props', 'persistence_type']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['id', 'data', 'label']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(SmartNodeSelector, self).__init__(**args)
