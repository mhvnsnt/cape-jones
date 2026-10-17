# Surface Heat Diffuse Skinning v3.4.2 (meshonline) — headless notes

**Upstream:** https://github.com/meshonline/Surface-Heat-Diffuse-Skinning
**License:** MIT (repo LICENSE) + GPL header in `__init__.py` — free, commercial OK.
**Why pulled:** open-source "never fails" alternative to Blender's Bone Heat
(`ARMATURE_AUTO`). Blender's heat solver fails on some meshes; this one diffuses
heat over the surface from ray-cast samples and always returns a weight set.

## Build

Upstream's `bin/Linux/` ships empty. Build the solver:

```bash
./build_linux.sh   # g++ *.cpp -> addon/surface_heat_diffuse_skinning/bin/Linux/shd
```

## Headless use (no GUI — the addon's operator is modal, so we drive the flow directly)

The addon's `execute()` does 5 things; `tools/weights/cj_bakeoff/bakeoff.py::weights_surface_heat`
replicates them without the modal timer:

1. **Write mesh** → `untitled-mesh.txt`: `v,x,y,z` per vertex (world), `f,i,j,...` per polygon.
2. **Write bones** → `untitled-bone.txt`: `b,name,hx,hy,hz,tx,ty,tz` per deform bone (world).
3. **Run solver**:
   `shd untitled-mesh.txt untitled-bone.txt untitled-weight.txt <res> <loops> <samples> <influence> <falloff> <sharpness> <solidify>`
   Defaults used: res=128, loops=5, samples=64, influence=8, falloff=0.2, sharpness=3 (Sharp), solidify=n.
   (These are the addon's UI defaults — see `bl_info`/scene props in `__init__.py`.)
4. **Read weights** → `untitled-weight.txt`: `b,name` lines then `w,vert_idx,bone_idx,weight`.
   Create/replace one vertex group per bone, `REPLACE` mode.
5. **Bind** → plain `ARMATURE` modifier targeting the rig (the addon's `parent_set(type='ARMATURE')`
   equivalent without the auto-weight step).

## Bake-off result

See `docs/research/WEIGHT-BAKEOFF-2026.md` (entry W3). Tested on the 991k-vert
Cape Jones mesh at native 0.925 m scale.
