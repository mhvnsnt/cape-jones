import bpy
from mathutils import Matrix

rig = bpy.data.objects.get("CapeJones_Rig")
if not rig:
    print("ERROR: rig not found")
else:
    print("BEFORE: rig world loc =", tuple(round(v,4) for v in rig.matrix_world.translation))
    # His locked placement (column-major -> row-major as specified)
    M = Matrix((
        (0.29237170472273677, 0.9563047559630354, 0, 0.07750696541475),
        (-0.9563047559630354, 0.29237170472273677, 0, 4.337572671573705),
        (0, 0, 1, -0.325),
        (0, 0, 0, 1),
    ))
    rig.matrix_world = M @ rig.matrix_world
    bpy.context.view_layer.update()
    print("AFTER: rig world loc =", tuple(round(v,4) for v in rig.matrix_world.translation))
    # verify it's a rigid transform
    import math
    det = M.determinant()
    print("det =", round(det, 6), "(should be 1.0)")

# Save to new file (preserve original)
bpy.ops.wm.save_as_mainfile(filepath="/home/hatch/workspace/sitcanon-work/scene_sit_placed.blend")
print("SAVED scene_sit_placed.blend")
