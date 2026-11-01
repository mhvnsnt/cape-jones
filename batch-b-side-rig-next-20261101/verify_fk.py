"""Print FK fcurves from the side .blend (Blender 4.5 slotted-action API)."""
import bpy, sys
path = sys.argv[sys.argv.index('--') + 1]
bpy.ops.wm.open_mainfile(filepath=path)
a = bpy.data.actions[0]
print('ACTION', a.name)
for slot in a.slots:
    print('SLOT', repr(slot))
    for layer in a.layers:
        for strip in layer.strips:
            try:
                cb = strip.channelbag(slot=slot)
            except Exception as e:
                print('  CB-ERR', e)
                continue
            for fc in cb.fcurves:
                print(' FC', fc.data_path, fc.array_index,
                      'frames', [round(k.co.x) for k in fc.keyframe_points],
                      'vals', [round(k.co.y, 3) for k in fc.keyframe_points])
