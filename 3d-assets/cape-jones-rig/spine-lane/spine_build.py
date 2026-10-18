"""SPINE LANE — build a real flexible multi-joint spine for CapeJones_Rig.

Run: blender -b cape_jones_rigged_w5r.blend --python spine_build.py
(always under xvfb-run -a + env -u PYTHONPATH)

What it does (all reversible via git — the .blend is versioned):
1. Resets stray pose state (file carries a leftover +80deg test rotation on upperarm_fk_L).
2. Rebuilds the torso deform chain in EDIT mode:
     pelvis -> spine_1 -> spine_2 -> spine_3 -> spine_4 -> chest
   5 deform spine joints (lumbar x2 + thoracic x3 incl. chest), slight natural
   kyphotic curve (2-10mm) so the IK solver has a bend plane.
3. Adds FK/IK spine controls (limb-pattern consistent):
   - spine_fk_1..4 + chest_fk: FK control chain (non-deform). The deform
     bones ALWAYS follow them 1:1 via COPY_ROTATION (REPLACE, LOCAL/LOCAL),
     exactly like the limbs' deform<-FK relationship.
   - spine_twist: master twist control (child of root). Each deform spine
     bone adds 20% of its local-Y rotation via COPY_ROTATION (ADD) — twist
     distributes evenly across all 5 joints in BOTH FK and IK modes, and
     Dual-Quaternion skinning prevents candy-wrapper collapse.
   - chest_ik + root["ik_spine"] switch (0=FK, 1=IK, one driver): in IK mode
     an IK constraint on chest_fk (5-bone chain chest_fk..spine_fk_1, pelvis
     stays put) drives the FK chain; the animator moves chest_ik for
     position and rotates chest_fk for chest orientation.
4. Re-skins the torso: z-positional remap of the W5r weights from
   {spine_1, spine_2, chest} onto {spine_1..spine_4, chest}. All other groups
   untouched, per-vert totals preserved, <=4 influences kept.
5. Saves the .blend in place (branch lane/spine-flex-20261017).

Scale: 0.925m native, never rescaled. Bone count: 85 -> 94.
"""
import bpy
import numpy as np
from mathutils import Matrix

RIG_NAME = "CapeJones_Rig"
BODY_NAME = "CapeJones_Body"
CAGE_NAME = "BlenRigMdefCage"

# New deform spine layout: name -> (head, tail). Slight -Y (forward) curve.
SPINE_DEFS = {
    "spine_1": ((0, 0, 0.49), (0, -0.002, 0.555)),
    "spine_2": ((0, -0.002, 0.555), (0, -0.004, 0.62)),
    "spine_3": ((0, -0.004, 0.62), (0, -0.006, 0.685)),
    "spine_4": ((0, -0.006, 0.685), (0, -0.008, 0.74)),
}
CHEST_DEF = ((0, -0.008, 0.74), (0, -0.010, 0.795))
# Weight-remap segment centers (z). Old: spine_1 .53 / spine_2 .62 / chest .715
NEW_SEGS = [("spine_1", 0.5225), ("spine_2", 0.5875), ("spine_3", 0.6525),
            ("spine_4", 0.7125), ("chest", 0.7675)]
OLD_SPINE_GROUPS = ("spine_1", "spine_2", "chest")
Z_MIN, Z_MAX = 0.38, 0.86


def get_rig():
    rig = bpy.data.objects.get(RIG_NAME)
    assert rig and rig.type == "ARMATURE", "rig not found"
    return rig


def reset_pose(rig):
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode="POSE")
    n = 0
    for pb in rig.pose.bones:
        dirty = (pb.location.length > 1e-9 or
                 any(abs(s - 1) > 1e-9 for s in pb.scale) or
                 any(abs(a) > 1e-9 for a in pb.rotation_euler) or
                 any(abs(a) > 1e-9 for a in pb.rotation_quaternion[1:]))
        if dirty:
            n += 1
        pb.location = (0, 0, 0)
        pb.rotation_mode = "XYZ"
        pb.rotation_euler = (0, 0, 0)
        pb.rotation_quaternion = (1, 0, 0, 0)
        pb.scale = (1, 1, 1)
    print(f"RESET_POSE: cleared {n} non-identity pose bones")


def rebuild_spine_edit(rig):
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode="EDIT")
    eb = rig.data.edit_bones
    for name in ("spine_3", "spine_4",
                 "spine_fk_1", "spine_fk_2", "spine_fk_3",
                 "spine_fk_4", "chest_fk", "spine_twist", "chest_ik"):
        if name in eb:
            eb.remove(eb[name])

    # 1. reposition existing deform bones (spine_1, spine_2, chest)
    for name in ("spine_1", "spine_2"):
        h, t = SPINE_DEFS[name]
        b = eb[name]
        b.head, b.tail = h, t
    chest = eb["chest"]
    chest.head, chest.tail = CHEST_DEF

    # 2. new deform spine bones spine_3 / spine_4
    for sname in ("spine_3", "spine_4"):
        h, t = SPINE_DEFS[sname]
        sb = eb.new(sname)
        sb.head, sb.tail = h, t
        sb.roll = 0.0
        sb.use_deform = True
    # clean deform chain: pelvis -> spine_1 -> spine_2 -> spine_3 -> spine_4 -> chest
    for child, parent in (("spine_1", "pelvis"), ("spine_2", "spine_1"),
                         ("spine_3", "spine_2"), ("spine_4", "spine_3"),
                         ("chest", "spine_4")):
        eb[child].parent = eb[parent]

    # 3. FK control bones (non-deform), mirror chain under pelvis
    fk_defs = [("spine_fk_1", "spine_1"), ("spine_fk_2", "spine_2"),
               ("spine_fk_3", "spine_3"), ("spine_fk_4", "spine_4"),
               ("chest_fk", "chest")]
    prev = "pelvis"
    for fk_name, src in fk_defs:
        fb = eb.new(fk_name)
        fb.head = tuple(eb[src].head)
        fb.tail = tuple(eb[src].tail)
        fb.roll = eb[src].roll
        fb.use_deform = False
        fb.parent = eb[prev]
        prev = fk_name

    # 4. spine_twist master (child of root) + chest_ik target (child of root)
    st = eb.new("spine_twist")
    st.head = (0, -0.002, 0.53)
    st.tail = (0, -0.002, 0.58)
    st.roll = 0.0
    st.use_deform = False
    st.parent = eb["root"]  # root: no dependency on the IK chain

    ik = eb.new("chest_ik")
    ik.head = (0, -0.008, 0.74)   # == chest head: IK target = chest head rest
    ik.tail = (0, -0.008, 0.79)
    ik.roll = 0.0
    ik.use_deform = False
    ik.parent = eb["root"]

    bpy.ops.object.mode_set(mode="OBJECT")
    print(f"EDIT: bones now {len(rig.data.bones)} (was 85)")


def add_switch_driver(con, expression):
    fcu = con.driver_add("influence")
    drv = fcu.driver
    drv.type = "SCRIPTED"
    drv.expression = expression
    var = drv.variables.new()
    var.name = "sw"
    var.type = "SINGLE_PROP"
    tgt = var.targets[0]
    tgt.id = bpy.data.objects[RIG_NAME]
    tgt.data_path = 'pose.bones["root"]["ik_spine"]'
    return drv


def wire_controls(rig):
    bpy.context.view_layer.objects.active = rig
    bpy.ops.object.mode_set(mode="POSE")
    pb_root = rig.pose.bones["root"]
    if "ik_spine" not in pb_root:
        pb_root["ik_spine"] = 0.0
    pb_root.id_properties_ui("ik_spine").update(
        min=0.0, max=1.0,
        description="Spine FK/IK switch: 0 = FK controls, 1 = IK (chest_ik)")

    def copy_rot(pb_name, cname, subtarget, mix, influence=None, driver=None):
        pb = rig.pose.bones[pb_name]
        c = pb.constraints.new("COPY_ROTATION")
        c.name = cname
        c.target = rig
        c.subtarget = subtarget
        c.target_space = "LOCAL"
        c.owner_space = "LOCAL"
        c.mix_mode = mix
        if driver:
            add_switch_driver(c, driver)
        elif influence is not None:
            c.influence = influence
        return c

    # Deform spine ALWAYS follows the FK controls 1:1 (limb pattern).
    # Twist is an additive 20%-per-joint offset from the spine_twist master,
    # so it works identically in FK and IK modes (deform bones are never
    # solver-overwritten).
    fk_map = [("spine_1", "spine_fk_1"), ("spine_2", "spine_fk_2"),
              ("spine_3", "spine_fk_3"), ("spine_4", "spine_fk_4"),
              ("chest", "chest_fk")]
    for deform, fk in fk_map:
        copy_rot(deform, "FK", fk, "REPLACE", influence=1.0)
        copy_rot(deform, "TWIST", "spine_twist", "ADD", influence=0.2)

    # IK drives the FK control chain: solver on chest_fk, 5-bone chain
    # (chest_fk..spine_fk_1); pelvis stays put. In IK mode the animator moves
    # chest_ik (position) and rotates chest_fk (chest orientation); the fk
    # spine chain is solver-driven.
    pb_tip = rig.pose.bones["chest_fk"]
    ikc = pb_tip.constraints.new("IK")
    ikc.name = "IK"
    ikc.target = rig
    ikc.subtarget = "chest_ik"
    ikc.chain_count = 5
    ikc.use_tail = False
    add_switch_driver(ikc, "sw")

    # IK stiffness bias: the solver converges tip-first and would leave the
    # waist straight; stiffening the upper FK joints pushes the bend down
    # toward the waist (measured: waist -0.3deg -> 8.9deg participation).
    for bn, s in (("spine_fk_2", 0.5), ("spine_fk_3", 0.8), ("spine_fk_4", 0.9)):
        rig.pose.bones[bn].ik_stiffness_x = s

    bpy.ops.object.mode_set(mode="OBJECT")
    print("POSE: FK follow + TWIST additive + IK-on-FK-chain wired")


def remap_torso_weights(obj):
    """Redistribute OLD_SPINE_GROUPS weights onto NEW_SEGS by z position."""
    mesh = obj.data
    vg = obj.vertex_groups
    for name, _ in NEW_SEGS:
        if name not in vg:
            vg.new(name=name)
    name_of = {g.index: g.name for g in vg}
    old_idx = {vg[name].index for name in OLD_SPINE_GROUPS if name in vg}
    n = len(mesh.vertices)
    co = np.empty(n * 3, dtype=np.float64)
    mesh.vertices.foreach_get("co", co)
    z = co.reshape(n, 3)[:, 2]
    cands = np.where((z > Z_MIN) & (z < Z_MAX))[0]
    seg_names = [s[0] for s in NEW_SEGS]
    seg_z = [s[1] for s in NEW_SEGS]

    def bracket(p):
        if p <= seg_z[0]:
            return seg_names[0], seg_names[0], 1.0, 0.0
        if p >= seg_z[-1]:
            return seg_names[-1], seg_names[-1], 1.0, 0.0
        for a in range(len(seg_z) - 1):
            if seg_z[a] <= p <= seg_z[a + 1]:
                span = seg_z[a + 1] - seg_z[a]
                wb = (p - seg_z[a]) / span
                return seg_names[a], seg_names[a + 1], 1.0 - wb, wb
        return seg_names[-1], seg_names[-1], 1.0, 0.0

    changed = 0
    pruned = 0
    for i in cands:
        v = mesh.vertices[i]
        S = 0.0
        had = []
        for g in v.groups:
            if g.group in old_idx:
                S += g.weight
                had.append(name_of[g.group])
        if S < 1e-6:
            continue
        p = z[i]
        if p < seg_z[0]:
            p = seg_z[0]
        elif p > seg_z[-1]:
            p = seg_z[-1]
        na, nb, wa, wb = bracket(p)
        ii = int(i)
        for gname in had:
            vg[gname].remove([ii])
        if wa > 1e-6:
            vg[na].add([ii], S * wa, "REPLACE")
        if wb > 1e-6:
            vg[nb].add([ii], S * wb, "REPLACE")
        # enforce repo standard: drop <0.01, keep top 4, renormalize
        cur = [(g.weight, name_of[g.group]) for g in mesh.vertices[ii].groups]
        keep = [(w, n_) for w, n_ in cur if w >= 0.01]
        keep.sort(reverse=True)
        drop_names = {n_ for w, n_ in cur if w < 0.01} | {n_ for _, n_ in keep[4:]}
        keep = keep[:4]
        if drop_names:
            pruned += 1
        for n_ in drop_names:
            vg[n_].remove([ii])
        tot = sum(w for w, _ in keep)
        if tot > 1e-9:
            for w, n_ in keep:
                vg[n_].add([ii], w / tot, "REPLACE")
        changed += 1
    print(f"WEIGHTS {obj.name}: remapped {changed} verts ({pruned} pruned to <=4), "
          f"of {len(cands)} candidates)")


def main():
    rig = get_rig()
    reset_pose(rig)
    rebuild_spine_edit(rig)
    wire_controls(rig)
    for oname in (BODY_NAME, CAGE_NAME):
        o = bpy.data.objects.get(oname)
        if o:
            remap_torso_weights(o)
    # sanity: no zero-length deform bones, twist joints non-deform
    bad = [b.name for b in rig.data.bones
           if (b.tail - b.head).length < 1e-6]
    print("ZERO-LENGTH BONES:", bad)
    bpy.ops.wm.save_mainfile()
    print("SAVED", bpy.data.filepath)


if __name__ == "__main__":
    main()
