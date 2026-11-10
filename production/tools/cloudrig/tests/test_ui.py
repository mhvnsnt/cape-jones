import bpy

from .blender_ui_testing import run_all_ui
from .conftest import advanced_mode, select_obj
from .install_this import disable_this, enable_this, get_addon_module_prefix


def test_all_ui(context_ui):
    # Loading the blend re-registers the rig UI panels from its cloudrig.py text datablock.
    # Re-register the add-on so the repo's own code runs instead, and gets coverage.
    disable_this()
    enable_this()

    run_ui_in_different_contexts(context_ui)


def test_all_ui_advanced_mode(context_ui):
    # Loading the blend re-registers the rig UI panels from its cloudrig.py text datablock.
    # Re-register the add-on so the repo's own code runs instead, and gets coverage.
    disable_this()
    enable_this()

    generator = bpy.data.objects["META-future"].cloudrig.generator
    with advanced_mode(context_ui):
        generator.show_only_nondefaults = True
        run_ui_in_different_contexts(context_ui)
        generator.show_only_nondefaults = False
        run_ui_in_different_contexts(context_ui)


def run_ui_in_different_contexts(context):
    prefix = get_addon_module_prefix()

    # Run with the META-future active object.
    select_obj(context, "META-future")
    rig = bpy.data.objects["META-future"]

    bone_names = (
        "Thigh.L",  # Leg component covers the drawing code for a lot of chain components.
        "Forearm.L",  # Covers `draw_inherited_component()`.`
        "Single Control",  # Cover Single Control params.
        "STR-Bone1_2",  # Cover Bone Tweak params.
        "Curve1",  # Cover IK Curve params.
        "Spline1",  # Cover Spline IK params.
        "Toon_Spine",  # Cover Spine: Cartoon params, parent switching, custom props storage bone picker.
        "Spine1",  # Cover Spine: Simple params.
        "Lattice",  # Cover Lattice params.
        "Phys1",  # Cover Chain: Physics params.
        "Layered1",  # Cover Chain: Layered params.
    )

    for bone_name in bone_names:
        rig.data.bones.active = rig.data.bones[bone_name]
        run_all_ui(context, prefix)

    # Run with no active object.
    context.view_layer.objects.active = None
    run_all_ui(context, prefix)
