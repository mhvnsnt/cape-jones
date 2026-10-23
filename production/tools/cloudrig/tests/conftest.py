from contextlib import contextmanager
from pathlib import Path

import bpy
import pytest
from bpy.types import Scene

from .blender_ui_testing import MockUILayout
from .install_this import disable_this, get_addon_module_prefix, install_this


@pytest.fixture(scope="session")
def install_addon():
    install_this(bpy.context)
    yield
    disable_this()


@pytest.fixture
def context(install_addon):
    ctx = bpy.context
    # Some CloudRig drivers need Python script execution.
    ctx.preferences.filepaths.use_scripts_auto_execute = True
    return ctx


@pytest.fixture
def mock_layout():
    """Fresh MockUILayout for the common case of exercising a single draw() call.
    Tests that need several independent layouts (eg. comparing two draw states)
    should just instantiate MockUILayout() directly instead."""
    return MockUILayout()


#############################


@pytest.fixture
def context_curves(context):
    load_blend("test_curves.blend")
    return context


@pytest.fixture
def context_workflow(context):
    load_blend("test_workflow_ops.blend")
    select_obj(context, "META-Sintel")
    bpy.ops.object.mode_set(mode="POSE")
    bpy.ops.pose.select_all(action="DESELECT")
    return context


@pytest.fixture
def context_simple(context):
    load_blend("test_simple.blend")
    select_obj(context, "META-Simple")
    return context


@pytest.fixture
def context_ui(context):
    load_blend("test_ui.blend")
    select_obj(context, "META-future")
    return context


@pytest.fixture
def context_poses(context) -> Scene:
    load_blend("test_poses.blend")
    return context


@pytest.fixture
def context_actions(context) -> Scene:
    load_blend("test_actions.blend")
    return context


@pytest.fixture
def context_chains(context) -> Scene:
    load_blend("test_chains.blend")
    return context


#############################


def load_blend(blend_name: str):
    blend_path = Path(__file__).parent / Path(f"blends/{blend_name}")
    bpy.ops.wm.open_mainfile(filepath=blend_path.as_posix())
    bpy.context.workspace.use_filter_by_owner = False


def select_obj(context, obj_name=None):
    if context.object:
        bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")
    if obj_name:
        obj = bpy.data.objects[obj_name]
        # Some naive un-hiding...
        obj.hide_set(False)
        obj.hide_viewport = False
        obj.select_set(True)
        context.view_layer.objects.active = obj


def set_pref_without_saving(prefs, prop_name: str, value):
    # The `loading` flag stops update_prefs_on_file() from overwriting the user's real CloudRig.json.
    type(prefs).loading = True
    try:
        setattr(prefs, prop_name, value)
    finally:
        type(prefs).loading = False


@contextmanager
def advanced_mode(context):
    """Enable CloudRig's Advanced Mode within the block, restoring it afterwards.
    Don't re-register the add-on inside the block: unregister() would save it to the user's prefs file.
    """
    prefs = context.preferences.addons[get_addon_module_prefix()].preferences
    original = prefs.advanced_mode
    set_pref_without_saving(prefs, 'advanced_mode', True)
    try:
        yield
    finally:
        set_pref_without_saving(prefs, 'advanced_mode', original)
