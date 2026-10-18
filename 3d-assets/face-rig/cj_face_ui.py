#!/usr/bin/env python3
"""CJ Face (GNM-style) — Blender N-panel add-on.

Slider panel driving the CJ_FaceParams expression vector built by
cj_parametric_face.py, grouped the way GNM groups its 383 params
(EYES / BROW / LOWER FACE / TONGUE / IRIS) + the preset sampler buttons.

Install: Edit > Preferences > Add-ons > Install, pick this file, enable
"CJ Face (GNM-style)". Open a shot file whose scene contains CJ_FaceParams
(built into cj_face_parametric.blend); the "CJ Face" tab appears in the
N-panel (3D viewport sidebar).

All rig-building code lives in cj_parametric_face.py; presets in
cj_face_presets.py (kept next to this file).
"""
import os
import sys

bl_info = {
    "name": "CJ Face (GNM-style)",
    "author": "Cape Jones lane",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > CJ Face",
    "description": "GNM-style parametric sliders + presets for the CJ face rig",
    "category": "Rigging",
}

try:
    import bpy
except ImportError:  # imported outside Blender (docs/tests)
    bpy = None

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

if bpy is not None:
    from bpy.props import StringProperty, FloatProperty

    try:
        import cj_face_presets as presets
    except ImportError:
        presets = None

    GROUPS = [
        ("EYES", ["blink_L", "blink_R", "wide", "squint_L", "squint_R",
                  "look_x", "look_y"]),
        ("BROW", ["brow_L", "brow_R", "brow_squeeze"]),
        ("LOWER FACE", ["jaw_open", "smile", "frown", "grimace",
                       "smirk_L", "smirk_R", "mouth_shift_x"]),
        ("TONGUE", ["tongue_out", "tongue_side"]),
        ("IRIS", ["pupil_toggle"]),
    ]
    PARAM_LABELS = {
        "blink_L": "Blink L", "blink_R": "Blink R", "wide": "Wide",
        "squint_L": "Squint L", "squint_R": "Squint R",
        "look_x": "Look X", "look_y": "Look Y",
        "brow_L": "Brow L", "brow_R": "Brow R", "brow_squeeze": "Squeeze",
        "jaw_open": "Jaw Open", "smile": "Smile", "frown": "Frown",
        "grimace": "Grimace", "smirk_L": "Smirk L", "smirk_R": "Smirk R",
        "mouth_shift_x": "Mouth Shift X",
        "tongue_out": "Tongue Out", "tongue_side": "Tongue Side",
        "pupil_toggle": "Pupils (emphasis)",
    }

    def find_params(context):
        return context.scene.objects.get("CJ_FaceParams")

    def find_mouth_driver(context):
        return context.scene.objects.get("CJ_MouthDriver")

    class CJFACE_OT_preset(bpy.types.Operator):
        bl_idname = "cjface.apply_preset"
        bl_label = "Apply CJ Face Preset"
        preset: StringProperty()

        def execute(self, context):
            p = find_params(context)
            if p is None or presets is None:
                self.report({'WARNING'}, "CJ_FaceParams not in scene")
                return {'CANCELLED'}
            mouth_idx = presets.apply_to_props(p, self.preset)
            md = find_mouth_driver(context)
            if md is not None:
                md["mouth_index"] = mouth_idx
            context.view_layer.update()
            return {'FINISHED'}

    class CJFACE_OT_zero(bpy.types.Operator):
        bl_idname = "cjface.zero"
        bl_label = "Zero All"

        def execute(self, context):
            p = find_params(context)
            if p is None:
                return {'CANCELLED'}
            for grp, names in GROUPS:
                for n in names:
                    p[n] = 0.0
            md = find_mouth_driver(context)
            if md is not None:
                md["mouth_index"] = 0
            context.view_layer.update()
            return {'FINISHED'}

    class CJFACE_PT_panel(bpy.types.Panel):
        bl_label = "CJ Face (GNM-style)"
        bl_idname = "CJFACE_PT_panel"
        bl_space_type = 'VIEW_3D'
        bl_region_type = 'UI'
        bl_category = "CJ Face"

        def draw(self, context):
            lay = self.layout
            p = find_params(context)
            if p is None:
                lay.label(text="No CJ_FaceParams in scene.", icon='ERROR')
                lay.label(text="Open cj_face_parametric.blend")
                return
            for grp, names in GROUPS:
                box = lay.box()
                box.label(text=grp)
                for n in names:
                    row = box.row()
                    row.prop(p, '["%s"]' % n, text=PARAM_LABELS.get(n, n), slider=True)
            lay.separator()
            lay.label(text="Presets (sheet-05 checklist):")
            if presets is not None:
                grid = lay.grid_flow(columns=2, align=True)
                for name in presets.CHECKLIST + presets.DARTS:
                    op = grid.operator("cjface.apply_preset",
                                       text=name.replace("_", " ").title())
                    op.preset = name
            lay.separator()
            lay.operator("cjface.zero", text="Zero All", icon='X')

    CLASSES = (CJFACE_OT_preset, CJFACE_OT_zero, CJFACE_PT_panel)

    def register():
        for c in CLASSES:
            bpy.utils.register_class(c)

    def unregister():
        for c in reversed(CLASSES):
            bpy.utils.unregister_class(c)

    if __name__ == "__main__":
        register()
