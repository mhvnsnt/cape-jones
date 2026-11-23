# cj_swap_addon.py — the Rig Jones 2 / Clean-Up Jones 1 slot swapper.
#
# Gumball method, translated into our language:
#   Gumball:  swapping = changing `firstFrame` of a frame-addressed comp
#              (loop="single frame"); one master symbol per view.
#   Ours:     one SLOT per part; swapping = changing the INDEX of that
#              slot. The slot's variants are frames of the comp.
#
# Two slot kinds (both "replace in place" — never stack a second piece):
#   - IMAGE slots (handR, handL, mouth): ONE plane per slot. Swapping
#     changes ONLY the image on that plane (material image texture).
#     Same plane, same pivot, same position — the swap is INVISIBLE.
#     This is the fix for the jumpy hand swap (owner 2026-11-23 10:42
#     EST): the old 7-planes-per-side swap teleported the hand up to
#     0.24 units sideways at every swap, like a scene cut. The hands
#     themselves were GOOD — only the swap mechanism changed.
#   - VISIBILITY slots (eyes, remote, forearms): variants own objects,
#     exactly one variant's objects visible. The eyes slot shares
#     Eye_L/Eye_R across both variants; visibility is computed as a SET
#     (shown iff the object belongs to the ACTIVE variant), never
#     per-variant in order.
#
# NO CAPS. There is no cap/disc/ball-joint object anywhere in this
# add-on or in the rig it drives. Verified first-hand against GB200:
# Gumball uses no caps — L_ARM/R_ARM are single DOMShapes per pose.
#
# UI: click a part to make its slot active; scroll the mouse wheel to
# roll through variants (WHEELUP = next, WHEELDOWN = previous);
# scrolling back and forth plays like an animation. ESC / RMB exits.
# Panel: View3D > Sidebar > CJ Slots, with < > buttons + variant name.
import bpy
import json
import os

BL_IDNAME = "cj.swap_addon"


def get_slots(arm, slots=None):
    if slots is not None:
        return slots
    if "cj_slots" in arm:
        return json.loads(arm["cj_slots"])
    return {}


def slot_of_object(arm, ob):
    """Which slot does this object belong to? Works for both kinds:
    image slots via their single plane, visibility slots via variants."""
    if ob is None:
        return None
    slots = get_slots(arm)
    for name, spec in slots.items():
        if spec.get("object") == ob.name:
            return name
        for variant in spec.get("variants", []):
            if ob.name in variant.get("objects", []):
                return name
    return None


def _set_image(arm, spec, image_name):
    """Swap the image on the slot's single plane (image-swap slot)."""
    ob = bpy.data.objects[spec["object"]]
    path = os.path.join(spec["art_dir"], image_name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"swap image not found: {path}")
    if ob.data.materials:
        mat = ob.data.materials[0]
        for node in mat.node_tree.nodes:
            if node.type == "TEX_IMAGE":
                img = bpy.data.images.load(path, check_existing=True)
                node.image = img
                node.image_user.frame_current = 0
                return
    raise RuntimeError(f"no image texture node on {ob.name}")


def _set_visibility(arm, spec, index, set_viewport):
    """Show exactly the active variant's objects (visibility slot).
    Computed as a SET: shown iff the object belongs to the active
    variant. Never per-variant in order — that let the last variant's
    hide win and hid the eye whites on every Normal frame."""
    variants = spec["variants"]
    index %= len(variants)
    active = set(variants[index].get("objects", []))
    for variant in variants:
        for obname in variant.get("objects", []):
            ob = bpy.data.objects.get(obname)
            if ob is None:
                continue
            show = obname in active
            ob.hide_render = not show
            if set_viewport:
                ob.hide_viewport = not show


def cj_set_slot(arm, slot_name, index, set_viewport=True, slots=None):
    """Headless + operator API: set slot `slot_name` to variant `index`
    (wraps). Returns the variant name.

    Blender gotcha (proven 2026-11-23): never set hide_viewport on
    objects whose hide_render you keyframe and read back via frame_set
    — hide_viewport excludes the object from the depsgraph and the
    hide_render F-Curve is never evaluated. Headless callers pass
    set_viewport=False.
    """
    slots = get_slots(arm, slots)
    spec = slots[slot_name]
    variants = spec["variants"]
    index %= len(variants)
    if "image" in variants[0]:
        _set_image(arm, spec, variants[index]["image"])
    else:
        _set_visibility(arm, spec, index, set_viewport)
    arm["cj_active_slot"] = slot_name
    arm["cj_active_index_" + slot_name] = index
    arm["cj_active_" + slot_name] = index
    return variants[index]["name"]


def cj_cycle_slot(arm, slot_name, step, set_viewport=True, slots=None):
    slots = get_slots(arm, slots)
    cur = int(arm.get("cj_active_index_" + slot_name, 0))
    return cj_set_slot(arm, slot_name, cur + step, set_viewport, slots)


def cj_slot_names(arm):
    return list(get_slots(arm).keys())


def cj_active_variant(arm, slot):
    return int(arm.get("cj_active_index_" + slot, 0))


# ---------------------------------------------------------------- operators
class CJ_OT_slot_wheel(bpy.types.Operator):
    """Roll the mouse wheel to cycle the active slot's variants."""
    bl_idname = "cj.slot_wheel"
    bl_label = "CJ Slot Wheel"
    bl_options = {"REGISTER", "UNDO"}

    def modal(self, context, event):
        if event.type in {"ESC", "RIGHTMOUSE"}:
            return {"FINISHED"}
        if event.type == "WHEELUPMOUSE":
            arm = context.active_object
            cj_cycle_slot(arm, arm["cj_active_slot"], +1)
            return {"RUNNING_MODAL"}
        if event.type == "WHEELDOWNMOUSE":
            arm = context.active_object
            cj_cycle_slot(arm, arm["cj_active_slot"], -1)
            return {"RUNNING_MODAL"}
        return {"PASS_THROUGH"}

    def invoke(self, context, event):
        return {"RUNNING_MODAL"}


class CJ_OT_slot_cycle(bpy.types.Operator):
    bl_idname = "cj.slot_cycle"
    bl_label = "CJ Slot Cycle"
    slot: bpy.props.StringProperty()
    step: bpy.props.IntProperty(default=1)

    def execute(self, context):
        arm = context.active_object
        name = cj_cycle_slot(arm, self.slot, self.step)
        self.report({"INFO"}, f"{self.slot}: {name}")
        return {"FINISHED"}


class CJ_OT_slot_set(bpy.types.Operator):
    bl_idname = "cj.slot_set"
    bl_label = "CJ Slot Set"
    slot: bpy.props.StringProperty()
    index: bpy.props.IntProperty(default=0)

    def execute(self, context):
        arm = context.active_object
        name = cj_set_slot(arm, self.slot, self.index)
        self.report({"INFO"}, f"{self.slot}: {name}")
        return {"FINISHED"}


class CJ_PT_slots(bpy.types.Panel):
    bl_label = "CJ Slots"
    bl_idname = "CJ_PT_slots"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "CJ"

    def draw(self, context):
        layout = self.layout
        arm = context.active_object
        if not arm or "cj_slots" not in arm:
            layout.label(text="Select the CJ rig armature")
            return
        slots = json.loads(arm["cj_slots"])
        for name, spec in slots.items():
            row = layout.row(align=True)
            op = row.operator("cj.slot_cycle", text="<")
            op.slot = name
            op.step = -1
            idx = int(arm.get("cj_active_index_" + name, 0))
            variants = spec["variants"]
            row.label(text=f"{name}: {variants[idx % len(variants)]['name']}")
            op = row.operator("cj.slot_cycle", text=">")
            op.slot = name
            op.step = 1


_CLASSES = (CJ_OT_slot_wheel, CJ_OT_slot_cycle, CJ_OT_slot_set, CJ_PT_slots)


def register():
    for cls in _CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(_CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
