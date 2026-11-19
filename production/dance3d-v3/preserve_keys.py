import bpy, sys
act = bpy.data.actions["CJ_Dance_3D_V3"]
bones = sorted({fc.data_path.split('"')[1] for fc in act.fcurves if '"' in fc.data_path})
other = sorted({fc.data_path for fc in act.fcurves if '"' not in fc.data_path})
print("KEYED_BONES", len(bones), bones); print("OTHER_PATHS", other); sys.stdout.flush()
