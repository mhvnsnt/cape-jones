# afk-rig

Free auto-rigging for 3D models that your AI can drive. Give it a GLB, and it fits a skeleton, skins the mesh and exports it with animations from a library of 250+ clips. It runs on your machine: no account, no upload, no per-rig cost.

The automatic fit is deterministic: the same model always gets the same skeleton. On top of that, every joint is open to your AI. It can render the model from any side with the skeleton drawn on, measure the mesh, move joints and preview animations until the rig looks right.

```sh
npx afk-rig auto character.glb --skeleton human --animations Walk,Idle_A
# -> character.rigged.glb
```

## Use it from Claude Code, Cursor or any MCP client

```sh
claude mcp add afk-rig -- npx -y afk-rig mcp
```

Cursor and other clients (`mcp.json`):

```json
{
  "mcpServers": {
    "afk-rig": { "command": "npx", "args": ["-y", "afk-rig", "mcp"] }
  }
}
```

Then ask: *"Rig models/knight.glb with afk-rig, check it in a walk animation and export it with Walk, Run and Idle."* The server's instructions tell the AI how the tools fit together. Renders come back as images it can look at.

Prefer the command line? Every tool is also a CLI command that prints JSON, and `afk-rig guide` prints the same instructions for an agent working through a shell.

## How a rig comes together

1. **start**: load the model, pick a skeleton, run the auto-fit. A project file (`<model>.afk-rig.json`) keeps the joints.
2. **render**: front, side, back and top views with the skeleton on top, rulers in model units and labeled joints. You can zoom on a joint, see through the mesh, color the mesh by skin weights, or pose the bound model in any animation at any time.
3. **inspect / slice / ray**: per joint, whether it's inside the mesh, how far it is from the surface and from the middle of the limb, and left/right mismatch. Slices show how the mesh splits into legs, arms and torso at any height.
4. **set_joints / aim / rotate**: move single joints (mirrored to the other side if you like), or point and turn whole limbs, hands and tails at once. Undo is always there.
5. **bind**: skin weights, with a report of which bones move what. Weight rules fix spots the solver gets wrong, like a cape following the legs.
6. **render with an animation**: pose the bound model in any clip at any time to check how it deforms; the response says if it floats or sinks.
7. **export**: a GLB with the skeleton, weights and the animations you pick. Materials, textures and UVs come through untouched.

How far to take it is up to the AI. Auto-fit alone is often enough for a standard character in a T-pose or A-pose. Long coats, capes, characters facing backwards and unusual proportions are where the loop pays off.

## Skeletons

| Skeleton | For | Bones | Animations |
| --- | --- | --- | --- |
| human | people, robots, zombies, humanoid monsters (fingers included) | 66 | 178 |
| fox | fox, dog, wolf, cat | 49 | 14 |
| horse | horse, deer, cow | 56 | 14 |
| bird | birds | 55 | 5 |
| dragon | winged dragons | 99 | 5 |
| kaiju | upright monsters with tails, dinosaurs | 58 | 10 |
| spider | spiders, crabs, insects | 56 | 10 |
| snake | snakes, worms | 28 | 8 |
| fish | fish, sharks, whales | 33 | 7 |

`afk-rig animations human --search "walk run"` lists clips. Human bones use Unreal-style names (`pelvis`, `spine_01`, `thigh_l`, `hand_r`...).

## CLI

```
afk-rig auto <model> --skeleton <type> [--out file.glb] [--animations a,b|all]
afk-rig start <model> --skeleton <type> [--hands all-fingers|thumb-and-index|simplified-hand|single-bone] [--no-fit]
afk-rig status <project>
afk-rig render <project> [--views front,left,back,right,top] [--size 640] [--focus joint|x,y,z] [--radius r]
                         [--xray] [--weights] [--bone name] [--animation name --time s] [--out image.png]
afk-rig inspect <project> [--joints a,b] [--issues]
afk-rig slice <project> --axis y --at 0.9
afk-rig ray <project> --from x,y,z --dir x,y,z
afk-rig set <project> hand_l=0.62,1.21,0.02 [--mirror] [--with-children]
afk-rig move <project> calf_l=0,0.03,0 [--mirror]
afk-rig aim <project> --joint upperarm_l --at x,y,z [--stretch]
afk-rig rotate <project> --joint hand_l --axis 0,0,1 --degrees 30
afk-rig weights <project> --add '{"mode":"never","bones":["hand_*","lowerarm_*"],"box":{"min":[..],"max":[..]}}'
        # "thigh_l*" = thigh_l and every bone below it; other * are wildcards ("hand_*", "*_l")
        # pick vertices by box, sphere, meshes or "piece_at":[x,y,z] (the connected part nearest a point);
        # rules apply in order, so put broad ones first
afk-rig fit <project> [--joints a,b] [--template]
afk-rig transform <project> [--rotate 0,180,0] [--scale s] [--translate x,y,z]
afk-rig meshes <project> [--exclude 2,floor] [--include 2]
afk-rig undo <project> [--steps n]
afk-rig bind <project> [--arm-plane-offset o] [--head-correction y]
afk-rig export <project> --out file.glb [--animations a,b|all] [--rest limbs|aligned|template] [--arm-spread deg] [--ground] [--drop-excluded]
afk-rig animations <skeleton|project> [--search text]
afk-rig skeletons
afk-rig mcp
afk-rig guide
```

There's also a JavaScript API: `import { RigSession } from 'afk-rig'`.

## Good to know

- No T-pose needed. T-pose, A-pose and arms-down characters work out of the box, including hands resting on the thighs and legs standing apart, and animations adapt to the arm angle. On models built from many separate parts (robots, mannequins) a little hip or thigh skin can still follow a hand that touches it: preview a walk and fix it with `weights` rules (`piece_at` picks a whole part). Characters in action poses (mid-run, crouching) work when your AI places the joints, since auto-fit assumes a standing pose.
- Input is GLB or glTF, including Draco- and meshopt-compressed files. Convert FBX or OBJ to GLB first; Blender does this in a few clicks.
- Models already rigged are read in their rest pose. Their old skeleton and animations are replaced.
- Floors, props and other stray meshes can be left out of the rig with `meshes --exclude`. They stay in the exported file unrigged, or get dropped with `--drop-excluded`.
- Characters should face +Z with +Y up, the glTF convention. The fit notes say when the feet point the other way, and `transform` turns the model around.
- `--rest limbs` (default) turns arm, leg, wing, finger and toe joints so animations reproduce the template's limb poses, which handles arms-down and A-posed characters, while the spine, neck and head keep the character's own posture. `--rest aligned` turns every joint; `--rest template` turns none, as the afk.ai website does.
- Skin weights come from the same solver as the website. They're good for games, but not hand-painted quality.

## Credits

Built by [afk.ai](https://afk.ai). The rigging engine is based on [Mesh2Motion](https://github.com/Mesh2Motion/mesh2motion-app) (MIT). Skeletons and animations are CC0, so use them in anything, commercial included. Questions or bugs: burtndylan@gmail.com.
