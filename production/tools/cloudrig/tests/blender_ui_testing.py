"""Add-on agnostic helpers for running Panel, Menu, Operator and UIList UI code in background-mode Blender tests.

Nothing in here may depend on a specific add-on: callers pass in the module prefix
their add-on is registered under (eg. "bl_ext.user_default.my_addon").
"""

import inspect
import traceback
from types import FunctionType, MethodType

import bpy
from bpy.types import Menu, Operator, Panel, UIList

UI_BASE_CLASSES = (Panel, Menu, Operator)
UIClass = type[Panel] | type[Menu] | type[Operator]

# Values of Blender's UILST_FLT_ITEM and UILST_FLT_ITEM_NEVER_SHOW (DNA_screen_types.h).
# Their RNA defaults are 0, since the real values come from C getters.
UILST_FLT_ITEM = 1 << 30
UILST_FLT_ITEM_NEVER_SHOW = 1 << 16

_FUNCTIONS = None
_PROPERTY_TYPES = None

_TYPE_DEFAULTS = {
    'BOOLEAN': False,
    'INT': 0,
    'FLOAT': 0.0,
    'STRING': "",
    'ENUM': "",
}


def _uilayout_rna():
    """Return ({function name: (input param names, output types)}, {property name: type}) of UILayout."""
    # Cached: bl_rna is static for the process, no need to walk it more than once.
    global _FUNCTIONS, _PROPERTY_TYPES
    if _FUNCTIONS is None:
        bl_rna = bpy.types.UILayout.bl_rna
        _FUNCTIONS = {
            f.identifier: (
                [p.identifier for p in f.parameters if not p.is_output],
                [p.type for p in f.parameters if p.is_output],
            )
            for f in bl_rna.functions
        }
        _PROPERTY_TYPES = {p.identifier: p.type for p in bl_rna.properties}
    return _FUNCTIONS, _PROPERTY_TYPES


def _rna_default(prop):
    if prop.type == 'POINTER':
        return None
    if prop.type == 'COLLECTION':
        return []
    if prop.type == 'ENUM' and prop.is_enum_flag:
        return set(prop.default_flag)
    if getattr(prop, 'is_array', False):
        return tuple(prop.default_array)
    return prop.default


class MockUILayout:
    """Stand-in for a real UILayout so draw() functions can run without a Blender UI.

    Methods and properties are discovered from UILayout.bl_rna, so this tracks
    whatever UILayout API the installed Blender actually has. Every call is
    recorded into `self.calls` as (name, args, kwargs), shared with any
    sub-layout returned by row()/column()/box()/etc., so a test can assert on
    the whole draw() call tree from the top-level instance alone.

    template_list() also filters and draws the UIList's items, like Blender does during that call.
    """

    def __init__(self, calls=None):
        self.calls = calls if calls is not None else []

    def __getattr__(self, name):
        functions, properties = _uilayout_rna()
        if name in functions:
            def method(*args, **kwargs):
                self.calls.append((name, args, kwargs))
                param_names, out_types = functions[name]
                if name == 'template_list':
                    _draw_template_list(self, param_names, args, kwargs)
                if not out_types:
                    return None
                values = [
                    MockUILayout(self.calls) if t == 'POINTER' else _TYPE_DEFAULTS.get(t)
                    for t in out_types
                ]
                return values[0] if len(values) == 1 else tuple(values)
            return method
        if name in properties:
            return _TYPE_DEFAULTS.get(properties[name])
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if name == 'calls':
            object.__setattr__(self, name, value)
            return
        self.calls.append(('__setattr__', (name, value), {}))
        object.__setattr__(self, name, value)


class _UIProxyMeta(type):
    """Forwards class-level attribute access on a proxy's class to the real UI class,
    so eg. `type(self).cache = ...` in UI code affects the real class, like in Blender."""

    def __getattr__(cls, name):
        if name == '_ui_cls':
            raise AttributeError(name)
        return getattr(cls._ui_cls, name)

    def __setattr__(cls, name, value):
        setattr(cls._ui_cls, name, value)


class UIProxy(metaclass=_UIProxyMeta):
    """Stands in for a Panel, Menu, Operator or UIList instance: a mock `layout`, with
    everything else (bl_label, helper methods, etc.) resolved from the real UI class.

    For Operators, their properties resolve to the last-used (or default) values, the
    same ones a redo panel or invoke_props_dialog() would draw.
    For UILists, their properties (filter_name, etc.) resolve to their RNA defaults.
    """

    def __new__(cls, ui_cls: UIClass | type[UIList], context):
        # A class per proxy, so that type(self) can stand in for ui_cls.
        proxy_cls = _UIProxyMeta(ui_cls.__name__, (cls,), {'_ui_cls': ui_cls})
        return object.__new__(proxy_cls)

    def __init__(self, ui_cls: UIClass | type[UIList], context):
        self.layout = MockUILayout()
        self._op_props = None
        self._rna_defaults = {}
        if issubclass(ui_cls, Operator):
            self._op_props = context.window_manager.operator_properties_last(ui_cls.bl_idname)
        elif issubclass(ui_cls, UIList):
            self._rna_defaults = {
                prop.identifier: _rna_default(prop)
                for prop in ui_cls.bl_rna.properties
                if prop.identifier != 'rna_type' and not prop.identifier.startswith('bl_')
            }
            self._rna_defaults['bitflag_filter_item'] = UILST_FLT_ITEM
            self._rna_defaults['bitflag_item_never_show'] = UILST_FLT_ITEM_NEVER_SHOW

    @property
    def __class__(self):
        # Lets isinstance() and zero-argument super() treat the proxy as an instance of the real class.
        return self._ui_cls

    def __getattr__(self, name):
        if self._op_props is not None:
            if name == "properties":
                return self._op_props
            if name in self._op_props.bl_rna.properties:
                return getattr(self._op_props, name)
        if name in self._rna_defaults:
            return self._rna_defaults[name]
        attr = getattr(self._ui_cls, name)
        # Staticmethods also come back as plain functions from the class, but must not be bound.
        is_static = isinstance(inspect.getattr_static(self._ui_cls, name), staticmethod)
        if isinstance(attr, FunctionType) and not is_static:
            return MethodType(attr, self)
        return attr


def _positional_arg_count(func, available: int) -> int:
    """How many of `available` positional args (excluding self) func accepts."""
    params = list(inspect.signature(func).parameters.values())[1:]
    if any(p.kind == p.VAR_POSITIONAL for p in params):
        return available
    positional = sum(p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD) for p in params)
    return min(available, positional)


def _draw_template_list(layout: MockUILayout, param_names: list[str], args, kwargs):
    """Do what Blender does during a template_list() call: filter the items,
    then draw the filter options and every visible item."""
    params = dict(zip(param_names, args)) | kwargs
    list_type_name = params['listtype_name']
    list_cls = getattr(bpy.types, list_type_name, None)
    if list_cls is None:
        raise AttributeError(f"template_list(): UIList '{list_type_name}' is not registered.")

    context = bpy.context
    ui_list = UIProxy(list_cls, context)
    ui_list.list_id = params['list_id']
    ui_list.layout_type = params.get('type', 'DEFAULT')
    data, propname = params['dataptr'], params['propname']

    flt_flags = []
    if hasattr(list_cls, 'filter_items'):
        flt_flags, _flt_neworder = ui_list.filter_items(context, data, propname)
    if hasattr(list_cls, 'draw_filter'):
        ui_list.draw_filter(context, MockUILayout(layout.calls))
    if not hasattr(list_cls, 'draw_item'):
        return

    for index, item in enumerate(getattr(data, propname)):
        flt_flag = flt_flags[index] if flt_flags else 0
        # Mirrors uilist_item_index_is_filtered_visible() in interface_template_list.cc.
        if flt_flags and (flt_flag & UILST_FLT_ITEM_NEVER_SHOW or not flt_flag & UILST_FLT_ITEM):
            continue
        draw_args = (
            context, MockUILayout(layout.calls), data, item, 0,
            params['active_dataptr'], params['active_propname'], index, flt_flag,
        )
        ui_list.draw_item(*draw_args[:_positional_arg_count(list_cls.draw_item, len(draw_args))])


def _registered_type_name(cls: UIClass) -> str:
    """Return the name a class is registered under in bpy.types."""
    idname = getattr(cls, "bl_idname", None)
    if not isinstance(idname, str):
        return cls.__name__
    if issubclass(cls, Operator) and "." in idname:
        # Operators are registered as eg. "POSE_OT_my_op", not by their "pose.my_op" bl_idname.
        category, name = idname.split(".", 1)
        return f"{category.upper()}_OT_{name}"
    return idname


def get_ui_classes(module_prefix: str) -> list[UIClass]:
    """Return the currently registered class of every Panel, Menu and drawable Operator
    defined under module_prefix.

    Resolved by registered name because the registered class may come from somewhere other
    than the module that defines it, eg. a copy of the same code registered from a text datablock.
    """
    type_names = set()
    stack = [sub for base in UI_BASE_CLASSES for sub in base.__subclasses__()]
    while stack:
        cls = stack.pop()
        stack.extend(cls.__subclasses__())
        if not cls.__module__.startswith(module_prefix):
            continue
        if issubclass(cls, Operator) and not hasattr(cls, "draw"):
            continue
        type_names.add(_registered_type_name(cls))
    return [
        getattr(bpy.types, type_name)
        for type_name in sorted(type_names)
        if hasattr(bpy.types, type_name)
    ]


def run_ui_class(ui_cls: UIClass, context):
    """Run a UI class's poll(), draw_header() and draw(). Drawing always runs, but its
    errors are only raised if poll() returned True."""
    poll_result = True
    if hasattr(ui_cls, "poll"):
        poll_result = ui_cls.poll(context)
    exceptions = () if poll_result else Exception
    try:
        proxy = UIProxy(ui_cls, context)
        if hasattr(ui_cls, "draw_header"):
            proxy.draw_header(context)
        if hasattr(ui_cls, "draw"):
            proxy.draw(context)
    except exceptions:
        # If a UI class errors to draw when the poll function returned False, don't fail the test.
        pass


def run_all_ui(context, module_prefix: str):
    """Run every registered UI class defined under module_prefix, and fail with all errors at once."""
    ui_classes = get_ui_classes(module_prefix)
    assert ui_classes, f"No registered UI classes found under {module_prefix}."
    foreign = [
        cls.__name__ for cls in ui_classes if not cls.__module__.startswith(module_prefix)
    ]
    assert not foreign, f"UI classes not registered from {module_prefix}: {foreign}"

    errors = []
    for ui_cls in ui_classes:
        try:
            run_ui_class(ui_cls, context)
        except Exception:
            errors.append(f"{ui_cls.__name__}:\n{traceback.format_exc()}")
    assert not errors, (
        f"{len(errors)}/{len(ui_classes)} UI classes failed:\n\n" + "\n\n".join(errors)
    )
