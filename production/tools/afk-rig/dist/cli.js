#!/usr/bin/env node
var __defProp = Object.defineProperty;
var __getOwnPropNames = Object.getOwnPropertyNames;
var __esm = (fn, res, err) => function __init() {
  if (err) throw err[0];
  try {
    return fn && (res = (0, fn[__getOwnPropNames(fn)[0]])(fn = 0)), res;
  } catch (e) {
    throw err = [e], e;
  }
};
var __export = (target, all) => {
  for (var name in all)
    __defProp(target, name, { get: all[name], enumerable: true });
};

// src/io.ts
import { NodeIO } from "@gltf-transform/core";
import { ALL_EXTENSIONS } from "@gltf-transform/extensions";
import { MeshoptDecoder } from "meshoptimizer";
import draco3d from "draco3dgltf";
async function get_io() {
  io_promise ??= (async () => {
    await MeshoptDecoder.ready;
    return new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({
      "draco3d.decoder": await draco3d.createDecoderModule(),
      "meshopt.decoder": MeshoptDecoder
    });
  })();
  return await io_promise;
}
var io_promise;
var init_io = __esm({
  "src/io.ts"() {
    "use strict";
    io_promise = null;
  }
});

// src/model.ts
import { resolve } from "node:path";
import { statSync } from "node:fs";
import { BufferGeometry, Float32BufferAttribute, Uint32BufferAttribute, Euler, Matrix4, Quaternion, Vector3 } from "three";
function transform_matrix(transform) {
  const m = new Matrix4();
  if (transform === void 0) return m;
  const deg = Math.PI / 180;
  const r = transform.rotate ?? [0, 0, 0];
  const rotation = new Quaternion().setFromEuler(new Euler(r[0] * deg, r[1] * deg, r[2] * deg, "XYZ"));
  const t = transform.translate ?? [0, 0, 0];
  const s = transform.scale ?? 1;
  return m.compose(new Vector3(t[0], t[1], t[2]), rotation, new Vector3(s, s, s));
}
function combine_transforms(first, second) {
  return new Matrix4().multiplyMatrices(second, first);
}
async function load_model(path, model_matrix = new Matrix4(), excluded = /* @__PURE__ */ new Set()) {
  const full_path = resolve(path);
  const io = await get_io();
  const doc = await io.read(full_path);
  const root = doc.getRoot();
  const primitives = [];
  let skipped = 0;
  const scene = root.getDefaultScene() ?? root.listScenes()[0];
  const mesh_nodes = [];
  scene?.traverse((node) => {
    if (node.getMesh() !== null) mesh_nodes.push(node);
  });
  const meshes = [];
  mesh_nodes.forEach((node, mesh_id) => {
    const mesh = node.getMesh();
    const matrix = combine_transforms(new Matrix4().fromArray(node.getWorldMatrix()), model_matrix);
    const skin = skin_matrices(node);
    const baked = [];
    for (const primitive of mesh.listPrimitives()) {
      if (primitive.getMode() !== TRIANGLES || primitive.getAttribute("POSITION") === null) {
        skipped++;
        continue;
      }
      baked.push({ mesh_id, node, primitive, matrix, geometry: bake_geometry(primitive, matrix, skin, model_matrix) });
    }
    const lo = new Vector3(Infinity, Infinity, Infinity);
    const hi = new Vector3(-Infinity, -Infinity, -Infinity);
    let tris = 0;
    for (const b of baked) {
      b.geometry.computeBoundingBox();
      lo.min(b.geometry.boundingBox.min);
      hi.max(b.geometry.boundingBox.max);
      tris += b.geometry.index.count / 3;
    }
    meshes.push({
      id: mesh_id,
      name: node.getName() !== "" ? node.getName() : mesh.getName(),
      triangles: tris,
      min: [lo.x, lo.y, lo.z].map((n) => Number(n.toPrecision(5))),
      max: [hi.x, hi.y, hi.z].map((n) => Number(n.toPrecision(5))),
      excluded: excluded.has(mesh_id)
    });
    if (!excluded.has(mesh_id)) primitives.push(...baked);
  });
  if (primitives.length === 0) throw new Error("No triangle meshes left to rig (all excluded, or the file has none).");
  const triangles = collect_triangles(primitives);
  const min = new Vector3(Infinity, Infinity, Infinity);
  const max = new Vector3(-Infinity, -Infinity, -Infinity);
  for (let i = 0; i < triangles.length; i += 3) {
    min.x = Math.min(min.x, triangles[i]);
    max.x = Math.max(max.x, triangles[i]);
    min.y = Math.min(min.y, triangles[i + 1]);
    max.y = Math.max(max.y, triangles[i + 1]);
    min.z = Math.min(min.z, triangles[i + 2]);
    max.z = Math.max(max.z, triangles[i + 2]);
  }
  let vertices = 0;
  for (const p of primitives) vertices += p.geometry.attributes.position.count;
  return {
    path: full_path,
    doc,
    primitives,
    meshes,
    triangles,
    min,
    max,
    info: {
      file: full_path,
      file_size_bytes: statSync(full_path).size,
      triangles: triangles.length / 9,
      vertices,
      meshes: mesh_nodes.length,
      primitives: primitives.length,
      materials: root.listMaterials().length,
      textures: root.listTextures().length,
      already_rigged: root.listSkins().length > 0,
      existing_animations: root.listAnimations().length,
      skipped_primitives: skipped
    }
  };
}
function skin_matrices(node) {
  const skin = node.getSkin();
  if (skin === null) return null;
  const ibm = skin.getInverseBindMatrices();
  return skin.listJoints().map((joint, i) => {
    const world = new Matrix4().fromArray(joint.getWorldMatrix());
    return ibm !== null ? world.multiply(new Matrix4().fromArray(ibm.getElement(i, []))) : world;
  });
}
function vertex_skin_matrices(primitive, skin) {
  const sets = [];
  for (let k = 0; ; k++) {
    const joints = primitive.getAttribute(`JOINTS_${k}`);
    const weights = primitive.getAttribute(`WEIGHTS_${k}`);
    if (joints === null || weights === null) break;
    sets.push([joints, weights]);
  }
  if (sets.length === 0) return null;
  const count = primitive.getAttribute("POSITION").getCount();
  const out = [];
  const j = [];
  const w = [];
  for (let i = 0; i < count; i++) {
    const blended = new Array(16).fill(0);
    let total = 0;
    for (const [joints, weights] of sets) {
      joints.getElement(i, j);
      weights.getElement(i, w);
      for (let c = 0; c < 4; c++) {
        if (w[c] === 0 || skin[j[c]] === void 0) continue;
        const e = skin[j[c]].elements;
        for (let n = 0; n < 16; n++) blended[n] += e[n] * w[c];
        total += w[c];
      }
    }
    out.push(total > 1e-6 ? new Matrix4().fromArray(blended.map((x) => x / total)) : null);
  }
  return out;
}
function bake_geometry(primitive, matrix, skin, model_matrix) {
  const position = primitive.getAttribute("POSITION");
  const normal = primitive.getAttribute("NORMAL");
  const count = position.getCount();
  const per_vertex = skin !== null ? vertex_skin_matrices(primitive, skin) : null;
  const vertex_matrix = (i) => {
    const skinned = per_vertex?.[i];
    return skinned != null ? new Matrix4().multiplyMatrices(model_matrix, skinned) : matrix;
  };
  const positions = new Float32Array(count * 3);
  const element = [];
  const v = new Vector3();
  for (let i = 0; i < count; i++) {
    position.getElement(i, element);
    v.set(element[0], element[1], element[2]).applyMatrix4(vertex_matrix(i));
    positions[i * 3] = v.x;
    positions[i * 3 + 1] = v.y;
    positions[i * 3 + 2] = v.z;
  }
  const geometry = new BufferGeometry();
  geometry.setAttribute("position", new Float32BufferAttribute(positions, 3));
  const index_accessor = primitive.getIndices();
  let indices;
  if (index_accessor !== null) {
    indices = Uint32Array.from(index_accessor.getArray());
  } else {
    indices = new Uint32Array(count);
    for (let i = 0; i < count; i++) indices[i] = i;
  }
  if ((per_vertex !== null ? model_matrix : matrix).determinant() < 0) {
    for (let i = 0; i + 2 < indices.length; i += 3) {
      const t = indices[i + 1];
      indices[i + 1] = indices[i + 2];
      indices[i + 2] = t;
    }
  }
  geometry.setIndex(new Uint32BufferAttribute(indices, 1));
  if (normal !== null) {
    const normals = new Float32Array(count * 3);
    const normal_matrix = new Matrix4().copy(matrix).invert().transpose();
    for (let i = 0; i < count; i++) {
      normal.getElement(i, element);
      v.set(element[0], element[1], element[2]).transformDirection(per_vertex !== null ? vertex_matrix(i) : normal_matrix);
      normals[i * 3] = v.x;
      normals[i * 3 + 1] = v.y;
      normals[i * 3 + 2] = v.z;
    }
    geometry.setAttribute("normal", new Float32BufferAttribute(normals, 3));
  } else {
    geometry.computeVertexNormals();
  }
  return geometry;
}
function collect_triangles(primitives) {
  let total = 0;
  for (const p of primitives) total += (p.geometry.index.count / 3 | 0) * 9;
  const out = new Float32Array(total);
  let o = 0;
  for (const p of primitives) {
    const pos = p.geometry.attributes.position.array;
    const index = p.geometry.index.array;
    for (let k = 0; k + 2 < index.length; k += 3) {
      for (let c = 0; c < 3; c++) {
        const vi = index[k + c] * 3;
        out[o++] = pos[vi];
        out[o++] = pos[vi + 1];
        out[o++] = pos[vi + 2];
      }
    }
  }
  return out;
}
var TRIANGLES;
var init_model = __esm({
  "src/model.ts"() {
    "use strict";
    init_io();
    TRIANGLES = 4;
  }
});

// src/assets.ts
import { fileURLToPath } from "node:url";
function asset_path(relative) {
  return fileURLToPath(new URL("../assets/" + relative, import.meta.url));
}
var init_assets = __esm({
  "src/assets.ts"() {
    "use strict";
  }
});

// ../../rigger/src/lib/enums/SkeletonType.ts
var init_SkeletonType = __esm({
  "../../rigger/src/lib/enums/SkeletonType.ts"() {
    "use strict";
  }
});

// ../../rigger/src/lib/RigModelVariations.ts
function createVariation(type, spec) {
  return {
    model_file: `models-variation/${type}/${spec.variant}.glb`,
    // all variations are in the same folder for now
    display_name: spec.displayName,
    attribution: spec.attribution ?? "",
    // attribution only needed for CC-SA and CC-BY
    license: spec.license ?? "CC0",
    // defaults to CC0 unless otherwise specified
    preview_image: `models-variation/${type}/preview/${spec.variant}.png`,
    // all preview images are stored in the profiles folder
    expandArms: spec.expandArms ?? 0,
    // default to 0 unless a human variation overrides it for the Explore page
    pelvis_position_scale: spec.pelvisPositionScale ?? 1
    // 1.0 keeps the authored hip height from the animation data
  };
}
var HUMAN_TYPE, humanVariations, FOX_TYPE, foxVariations, BIRD_TYPE, birdVariations, KAIJU_TYPE, kaijuVariations, FISH_TYPE, fishVariations;
var init_RigModelVariations = __esm({
  "../../rigger/src/lib/RigModelVariations.ts"() {
    "use strict";
    HUMAN_TYPE = "human";
    humanVariations = [
      createVariation(HUMAN_TYPE, { variant: "male", displayName: "Male", attribution: "Quaternius", license: "CC0" }),
      createVariation(HUMAN_TYPE, { variant: "zombie", displayName: "Zombie", attribution: "Kenney.nl", license: "CC0" }),
      createVariation(HUMAN_TYPE, { variant: "female", displayName: "Female", attribution: "Quaternius", license: "CC0" }),
      createVariation(HUMAN_TYPE, { variant: "female_8", displayName: "Female 8", attribution: "elbolilloduro", license: "CC0" }),
      createVariation(HUMAN_TYPE, { variant: "female_9", displayName: "Female 9", attribution: "elbolilloduro", license: "CC0", pelvisPositionScale: 1.02 }),
      createVariation(HUMAN_TYPE, { variant: "female_31", displayName: "Female 31", attribution: "elbolilloduro", license: "CC0", pelvisPositionScale: 0.92 }),
      createVariation(HUMAN_TYPE, { variant: "male_5", displayName: "Male 5", attribution: "elbolilloduro", license: "CC0" }),
      createVariation(HUMAN_TYPE, { variant: "male_6", displayName: "Male 6", attribution: "elbolilloduro", license: "CC0" }),
      createVariation(HUMAN_TYPE, { variant: "male_10", displayName: "Male 10", attribution: "elbolilloduro", license: "CC0" }),
      createVariation(HUMAN_TYPE, { variant: "male_15", displayName: "Male 15", attribution: "elbolilloduro", license: "CC0" }),
      createVariation(HUMAN_TYPE, { variant: "male_32", displayName: "Male 32", attribution: "elbolilloduro", license: "CC0", pelvisPositionScale: 0.96 }),
      createVariation(HUMAN_TYPE, { variant: "doctor_m", displayName: "Doctor Male", attribution: "elbolilloduro", license: "CC0" }),
      createVariation(HUMAN_TYPE, { variant: "swat_male", displayName: "SWAT Male", attribution: "elbolilloduro", license: "CC0" }),
      createVariation(HUMAN_TYPE, { variant: "police_male", displayName: "Police Male", attribution: "elbolilloduro", license: "CC0" }),
      createVariation(HUMAN_TYPE, { variant: "police_female", displayName: "Police Female", attribution: "elbolilloduro", license: "CC0" }),
      createVariation(HUMAN_TYPE, { variant: "hazmat_female", displayName: "Hazmat Female", attribution: "elbolilloduro", license: "CC0" }),
      createVariation(HUMAN_TYPE, { variant: "hazmat_suit_male", displayName: "Hazmat Suit Male", attribution: "elbolilloduro", license: "CC0", pelvisPositionScale: 1.05 }),
      createVariation(HUMAN_TYPE, { variant: "killer_4", displayName: "Killer 4", attribution: "elbolilloduro", license: "CC0", pelvisPositionScale: 1.02 }),
      createVariation(HUMAN_TYPE, { variant: "killer_5", displayName: "Killer 5", attribution: "elbolilloduro", license: "CC0", pelvisPositionScale: 1.05 }),
      createVariation(HUMAN_TYPE, { variant: "killer_6", displayName: "Killer 6", attribution: "elbolilloduro", license: "CC0", pelvisPositionScale: 1.05 }),
      createVariation(HUMAN_TYPE, { variant: "killer_7", displayName: "Killer 7", attribution: "elbolilloduro", license: "CC0" }),
      createVariation(HUMAN_TYPE, { variant: "monster", displayName: "Monster", attribution: "elbolilloduro", license: "CC0", pelvisPositionScale: 1.37 }),
      createVariation(HUMAN_TYPE, { variant: "monster_3", displayName: "Monster 3", attribution: "elbolilloduro", license: "CC0", pelvisPositionScale: 1.05 }),
      createVariation(HUMAN_TYPE, { variant: "monster_4", displayName: "Monster 4", attribution: "elbolilloduro", license: "CC0", pelvisPositionScale: 1.55 }),
      createVariation(HUMAN_TYPE, { variant: "monster_5", displayName: "Monster 5", attribution: "elbolilloduro", license: "CC0", pelvisPositionScale: 1.12 }),
      createVariation(HUMAN_TYPE, { variant: "sophia", displayName: "Sophia", attribution: "Tysan Tan", license: "CC-SA 4.0" }),
      createVariation(HUMAN_TYPE, { variant: "jay", displayName: "Jay", attribution: "Blender Studio", license: "CC-BY" }),
      createVariation(HUMAN_TYPE, { variant: "sintel", displayName: "Sintel", attribution: "Blender Studio", license: "CC-BY" }),
      createVariation(HUMAN_TYPE, { variant: "bunny", displayName: "Bunny", attribution: "Blender Studio", license: "CC-BY", expandArms: -30 })
    ];
    FOX_TYPE = "fox";
    foxVariations = [
      createVariation(FOX_TYPE, { variant: "fox", displayName: "Fox" }),
      createVariation(FOX_TYPE, { variant: "dog", displayName: "Dog" }),
      createVariation(FOX_TYPE, { variant: "cat", displayName: "Carrot", attribution: "David Revoy", license: "CC-BY" }),
      createVariation(FOX_TYPE, { variant: "panda", displayName: "Panda" })
    ];
    BIRD_TYPE = "bird";
    birdVariations = [
      createVariation(BIRD_TYPE, { variant: "seagull", displayName: "Seagull" }),
      createVariation(BIRD_TYPE, { variant: "eagle", displayName: "Bald Eagle" })
    ];
    KAIJU_TYPE = "kaiju";
    kaijuVariations = [
      createVariation(KAIJU_TYPE, { variant: "lizard", displayName: "Lizard" }),
      createVariation(KAIJU_TYPE, { variant: "t-rex", displayName: "T-Rex" })
    ];
    FISH_TYPE = "fish";
    fishVariations = [
      createVariation(FISH_TYPE, { variant: "shark", displayName: "Shark" }),
      createVariation(FISH_TYPE, { variant: "whale", displayName: "Whale" })
    ];
  }
});

// ../../rigger/src/lib/RigConfig.ts
var RigConfig;
var init_RigConfig = __esm({
  "../../rigger/src/lib/RigConfig.ts"() {
    "use strict";
    init_SkeletonType();
    init_RigModelVariations();
    RigConfig = class {
      static {
        this.all = [
          {
            skeleton_type: "human" /* Human */,
            model_file: "models/model-human.glb",
            rig_file: "rigs/rig-human.glb",
            rig_display_name: "Human",
            animation_files: [
              "../animations/human-base-animations.glb",
              "../animations/human-addon-animations.glb",
              "../animations/human-mocap-animations.glb"
            ],
            animation_preview_folder: "human",
            position_tracking_bone_name: "pelvis",
            skeleton_template_image_url: "rigs/reference/human.png",
            model_variations: humanVariations
          },
          {
            skeleton_type: "fox" /* Fox */,
            model_file: "models/model-fox.glb",
            rig_file: "rigs/rig-fox.glb",
            rig_display_name: "Fox",
            animation_files: ["../animations/fox-animations.glb"],
            animation_preview_folder: "fox",
            position_tracking_bone_name: "hips",
            skeleton_template_image_url: "rigs/reference/fox.png",
            model_variations: foxVariations
          },
          {
            skeleton_type: "bird" /* Bird */,
            model_file: "models/model-bird.glb",
            rig_file: "rigs/rig-bird.glb",
            rig_display_name: "Bird",
            animation_files: ["../animations/bird-animations.glb"],
            animation_preview_folder: "bird",
            position_tracking_bone_name: "hips",
            skeleton_template_image_url: "rigs/reference/bird.png",
            model_variations: birdVariations
          },
          {
            skeleton_type: "dragon" /* Dragon */,
            model_file: "models/model-dragon.glb",
            rig_file: "rigs/rig-dragon.glb",
            rig_display_name: "Dragon",
            animation_files: ["../animations/dragon-animations.glb"],
            animation_preview_folder: "dragon",
            position_tracking_bone_name: "hips",
            skeleton_template_image_url: "rigs/reference/dragon.png"
          },
          {
            skeleton_type: "kaiju" /* Kaiju */,
            model_file: "models/model-kaiju.glb",
            rig_file: "rigs/rig-kaiju.glb",
            rig_display_name: "Kaiju",
            animation_files: ["../animations/kaiju-animations.glb"],
            animation_preview_folder: "kaiju",
            position_tracking_bone_name: "hips",
            skeleton_template_image_url: "rigs/reference/kaiju.png",
            model_variations: kaijuVariations
          },
          {
            skeleton_type: "spider" /* Spider */,
            model_file: "models/model-spider.glb",
            rig_file: "rigs/rig-spider.glb",
            rig_display_name: "Spider",
            animation_files: ["../animations/spider-animations.glb"],
            animation_preview_folder: "spider",
            position_tracking_bone_name: "hips",
            skeleton_template_image_url: "rigs/reference/spider.png"
          },
          {
            skeleton_type: "snake" /* Snake */,
            model_file: "models/model-snake.glb",
            rig_file: "rigs/rig-snake.glb",
            rig_display_name: "Snake",
            animation_files: ["../animations/snake-animations.glb"],
            animation_preview_folder: "snake",
            position_tracking_bone_name: "head",
            // snake doesn't have hips, so we track position from the head instead
            skeleton_template_image_url: "rigs/reference/snake.png"
          },
          {
            skeleton_type: "fish" /* Fish */,
            model_file: "models/model-shark.glb",
            rig_file: "rigs/rig-shark.glb",
            rig_display_name: "Fish",
            animation_files: ["../animations/shark-animations.glb"],
            animation_preview_folder: "shark",
            position_tracking_bone_name: "pelvis",
            skeleton_template_image_url: "rigs/reference/shark.png",
            model_variations: fishVariations
          },
          {
            skeleton_type: "horse" /* Horse */,
            model_file: "models/model-horse.glb",
            rig_file: "rigs/rig-horse.glb",
            rig_display_name: "Horse",
            animation_files: ["../animations/horse-animations.glb"],
            animation_preview_folder: "horse",
            position_tracking_bone_name: "hips",
            skeleton_template_image_url: "rigs/reference/horse.png"
          }
        ];
      }
      /** Look up a rig by its SkeletonType enum value (which is also used as the key). */
      static by_key(rig_key) {
        return this.all.find((r) => r.skeleton_type === rig_key);
      }
      /** Look up a rig by its SkeletonType enum value. */
      static by_skeleton_type(skeleton_type) {
        return this.all.find((r) => r.skeleton_type === skeleton_type);
      }
      /** Get the rig GLB file path for a given skeleton type. Returns undefined for Error/None. */
      static rig_file_for(skeleton_type) {
        return this.by_skeleton_type(skeleton_type)?.rig_file;
      }
      /**
       * Get all configured animation file paths for a skeleton type.
       * @param skeleton_type The skeleton type to retrieve animation files for
       * @returns Array of animation file paths, empty array if no files configured
       */
      static get_animation_file_paths(skeleton_type) {
        const config = this.by_skeleton_type(skeleton_type);
        if (config === void 0 || config.animation_files.length === 0) return [];
        return config.animation_files;
      }
    };
  }
});

// ../../rigger/src/lib/processes/load-skeleton/HandHelper.ts
var HandHelper;
var init_HandHelper = __esm({
  "../../rigger/src/lib/processes/load-skeleton/HandHelper.ts"() {
    "use strict";
    init_SkeletonType();
    HandHelper = class {
      modify_hand_skeleton(armature, hand_type) {
        const bones_to_remove = [];
        armature.traverse((child) => {
          if (child.type === "Bone") {
            const bone = child;
            const bone_name = (bone.name ?? "").toLowerCase();
            if (!this.is_hand_bone(bone_name) || this.is_palm_bone(bone_name)) {
              return;
            }
            switch (hand_type) {
              case "thumb-and-index" /* ThumbAndIndex */:
                if (!this.is_thumb_bone(bone_name) && !this.is_middle_finger_bone(bone_name)) {
                  bones_to_remove.push(bone);
                }
                if (this.is_end_tip_bone(bone_name)) {
                  bones_to_remove.push(bone);
                }
                break;
              case "simplified-hand" /* SimplifiedHand */:
                if (this.is_end_tip_bone(bone_name)) {
                  bones_to_remove.push(bone);
                }
                break;
              case "single-bone" /* SingleBone */:
                if (!this.is_middle_finger_bone(bone_name)) {
                  bones_to_remove.push(bone);
                  break;
                }
                if (this.is_end_tip_bone(bone_name) || bone_name.includes("03") || bone_name.includes("04") || bone_name.includes("02")) {
                  bones_to_remove.push(bone);
                }
                break;
            }
          }
        });
        bones_to_remove.forEach((bone) => {
          if (bone.parent != null) {
            bone.parent.remove(bone);
          }
        });
      }
      is_hand_bone(bone_name) {
        const hand_patterns = ["hand", "finger", "thumb", "index", "middle", "ring", "pinky"];
        return hand_patterns.some((pattern) => bone_name.includes(pattern));
      }
      is_palm_bone(bone_name) {
        const hand_patterns = ["hand"];
        return hand_patterns.some((pattern) => bone_name.includes(pattern));
      }
      is_thumb_bone(bone_name) {
        return bone_name.includes("thumb");
      }
      is_middle_finger_bone(bone_name) {
        return bone_name.includes("middle");
      }
      // "tip" bones are the last bone at the end of the fingers and feet
      // they have the word 'tip' in the bone name
      is_end_tip_bone(bone_name) {
        return bone_name.toLowerCase().includes("leaf");
      }
    };
  }
});

// ../../rigger/src/lib/processes/edit-skeleton/auto-fit/PointCloud.ts
import { Vector3 as Vector32 } from "three";
var PointCloud;
var init_PointCloud = __esm({
  "../../rigger/src/lib/processes/edit-skeleton/auto-fit/PointCloud.ts"() {
    "use strict";
    PointCloud = class _PointCloud {
      // points sorted by y so horizontal slabs are a binary search away
      constructor(xs, ys, zs) {
        this.xs = xs;
        this.ys = ys;
        this.zs = zs;
        this.min = new Vector32(Infinity, Infinity, Infinity);
        this.max = new Vector32(-Infinity, -Infinity, -Infinity);
        this.count = xs.length;
        for (let i = 0; i < this.count; i++) {
          this.min.set(Math.min(this.min.x, xs[i]), Math.min(this.min.y, ys[i]), Math.min(this.min.z, zs[i]));
          this.max.set(Math.max(this.max.x, xs[i]), Math.max(this.max.y, ys[i]), Math.max(this.max.z, zs[i]));
        }
      }
      /**
       * Evenly spread points over the surface. Using vertices directly fails on low-poly
       * models, where a thin slice through the body only catches a handful of them.
       * @param triangles world-space triangles, 9 floats each
       * @param sample_count roughly how many points to place, by area
       */
      static from_triangles(triangles, sample_count = 12e4) {
        const triangle_count = Math.floor(triangles.length / 9);
        const areas = new Float32Array(triangle_count);
        let total_area = 0;
        const a = new Vector32();
        const b = new Vector32();
        const c = new Vector32();
        for (let t = 0; t < triangle_count; t++) {
          a.fromArray(triangles, t * 9);
          b.fromArray(triangles, t * 9 + 3);
          c.fromArray(triangles, t * 9 + 6);
          const area = b.sub(a).cross(c.sub(a)).length() / 2;
          areas[t] = area;
          total_area += area;
        }
        let seed = 795556893;
        const random = () => {
          seed = seed + 1831565813 | 0;
          let r = Math.imul(seed ^ seed >>> 15, 1 | seed);
          r = r + Math.imul(r ^ r >>> 7, 61 | r) ^ r;
          return ((r ^ r >>> 14) >>> 0) / 4294967296;
        };
        const points = [];
        const per_area = total_area > 0 ? sample_count / total_area : 0;
        for (let t = 0; t < triangle_count; t++) {
          const o = t * 9;
          points.push(triangles[o], triangles[o + 1], triangles[o + 2]);
          const expected = areas[t] * per_area;
          let samples = Math.floor(expected);
          if (random() < expected - samples) samples++;
          for (let s = 0; s < samples; s++) {
            let u = random();
            let v = random();
            if (u + v > 1) {
              u = 1 - u;
              v = 1 - v;
            }
            const w = 1 - u - v;
            points.push(
              triangles[o] * w + triangles[o + 3] * u + triangles[o + 6] * v,
              triangles[o + 1] * w + triangles[o + 4] * u + triangles[o + 7] * v,
              triangles[o + 2] * w + triangles[o + 5] * u + triangles[o + 8] * v
            );
          }
        }
        return _PointCloud.from_points(new Float32Array(points));
      }
      /**
       * @param flat_points xyz triplets in world space
       * @param voxels_per_height grid resolution, as cells across the model's height
       */
      static from_points(flat_points, voxels_per_height = 250) {
        let min_y = Infinity;
        let max_y = -Infinity;
        for (let i = 1; i < flat_points.length; i += 3) {
          min_y = Math.min(min_y, flat_points[i]);
          max_y = Math.max(max_y, flat_points[i]);
        }
        const cell = Math.max((max_y - min_y) / voxels_per_height, 1e-6);
        const seen = /* @__PURE__ */ new Set();
        const kept = [];
        for (let i = 0; i < flat_points.length; i += 3) {
          const key = `${Math.floor(flat_points[i] / cell)},${Math.floor(flat_points[i + 1] / cell)},${Math.floor(flat_points[i + 2] / cell)}`;
          if (seen.has(key)) continue;
          seen.add(key);
          kept.push(i);
        }
        kept.sort((a, b) => flat_points[a + 1] - flat_points[b + 1]);
        const xs = new Float32Array(kept.length);
        const ys = new Float32Array(kept.length);
        const zs = new Float32Array(kept.length);
        kept.forEach((index, k) => {
          xs[k] = flat_points[index];
          ys[k] = flat_points[index + 1];
          zs[k] = flat_points[index + 2];
        });
        return new _PointCloud(xs, ys, zs);
      }
      get height() {
        return this.max.y - this.min.y;
      }
      lower_bound(y) {
        let lo = 0;
        let hi = this.count;
        while (lo < hi) {
          const mid = lo + hi >> 1;
          if (this.ys[mid] < y) lo = mid + 1;
          else hi = mid;
        }
        return lo;
      }
      /** indices of points with y in [y_min, y_max] */
      slab(y_min, y_max) {
        const indices = [];
        for (let i = this.lower_bound(y_min); i < this.count && this.ys[i] <= y_max; i++) {
          indices.push(i);
        }
        return indices;
      }
      filter(indices, keep) {
        return indices.filter(keep);
      }
      all_indices() {
        return Array.from({ length: this.count }, (_, i) => i);
      }
      /** split values into runs separated by gaps larger than `gap` */
      static intervals(values, gap) {
        if (values.length === 0) return [];
        const sorted = [...values].sort((a, b) => a - b);
        const result = [];
        let current = { min: sorted[0], max: sorted[0], count: 1 };
        for (let i = 1; i < sorted.length; i++) {
          if (sorted[i] - current.max > gap) {
            result.push(current);
            current = { min: sorted[i], max: sorted[i], count: 1 };
          } else {
            current.max = sorted[i];
            current.count++;
          }
        }
        result.push(current);
        return result;
      }
      static median(values) {
        if (values.length === 0) return 0;
        const sorted = [...values].sort((a, b) => a - b);
        return sorted[Math.floor(sorted.length / 2)];
      }
      /** middle of the bounding box of the given points, per axis */
      bounds_mid(indices) {
        if (indices.length === 0) return null;
        const lo = new Vector32(Infinity, Infinity, Infinity);
        const hi = new Vector32(-Infinity, -Infinity, -Infinity);
        for (const i of indices) {
          lo.set(Math.min(lo.x, this.xs[i]), Math.min(lo.y, this.ys[i]), Math.min(lo.z, this.zs[i]));
          hi.set(Math.max(hi.x, this.xs[i]), Math.max(hi.y, this.ys[i]), Math.max(hi.z, this.zs[i]));
        }
        return lo.add(hi).multiplyScalar(0.5);
      }
      point(i) {
        return new Vector32(this.xs[i], this.ys[i], this.zs[i]);
      }
    };
  }
});

// ../../rigger/src/lib/processes/edit-skeleton/auto-fit/HumanoidLandmarks.ts
import { Vector3 as Vector33 } from "three";
var SLAB_STEP, GAP, HumanoidLandmarkFinder;
var init_HumanoidLandmarks = __esm({
  "../../rigger/src/lib/processes/edit-skeleton/auto-fit/HumanoidLandmarks.ts"() {
    "use strict";
    init_PointCloud();
    SLAB_STEP = 5e-3;
    GAP = 0.012;
    HumanoidLandmarkFinder = class {
      constructor(cloud) {
        this.cloud = cloud;
        this.h = cloud.height;
      }
      measure() {
        const floor = this.cloud.min.y;
        const top = this.cloud.max.y;
        const center_x = this.find_center_x(floor);
        const crotch_y = this.plausible_crotch(this.find_crotch_y(floor, center_x), center_x);
        const torso_half_width = this.find_torso_half_width(floor, center_x, crotch_y);
        const arm_line_y = this.find_arm_line_y(floor, top, center_x);
        const arms = /* @__PURE__ */ new Map();
        for (const side of [1, -1]) {
          const arm = this.measure_arm(side, floor, center_x, crotch_y, torso_half_width, arm_line_y);
          if (arm !== null) arms.set(side, arm);
        }
        const shoulder_y = this.shoulder_height(arms, floor);
        const neck_y = this.find_neck_y(center_x, torso_half_width, shoulder_y, top);
        return { floor, top, height: this.h, center_x, crotch_y, torso_half_width, neck_y, arm_line_y, arms };
      }
      find_center_x(floor) {
        const band = this.cloud.slab(floor + 0.25 * this.h, floor + 0.6 * this.h);
        return PointCloud.median(band.map((i) => this.cloud.xs[i]));
      }
      /** intervals along x for a thin horizontal slab */
      x_intervals(y, half_thickness = SLAB_STEP) {
        const slab = this.cloud.slab(y - half_thickness * this.h, y + half_thickness * this.h);
        return PointCloud.intervals(slab.map((i) => this.cloud.xs[i]), GAP * this.h);
      }
      find_crotch_y(floor, center_x) {
        let last_split_y = null;
        let misses = 0;
        for (let f = 0.08; f <= 0.65; f += SLAB_STEP) {
          const y = floor + f * this.h;
          const intervals = this.x_intervals(y);
          const covers_center = intervals.some((i) => i.min <= center_x && i.max >= center_x);
          const has_left = intervals.some((i) => i.min > center_x && i.min - center_x < 0.25 * this.h);
          const has_right = intervals.some((i) => i.max < center_x && center_x - i.max < 0.25 * this.h);
          if (!covers_center && has_left && has_right || this.leg_pair(y, center_x) !== null) {
            last_split_y = y;
            misses = 0;
          } else if (last_split_y !== null) {
            misses++;
            if (misses > 2) break;
          }
        }
        return last_split_y;
      }
      /**
       * The two legs in a slab below the crotch, [left (+X), right (-X)], or null where the legs
       * have joined. The legs are the innermost piece on each side of the middle (hands hanging
       * beside the thighs are further out). Legs a little ahead of each other still count.
       */
      leg_pair(y, center_x) {
        const pieces = this.slab_pieces(y).filter((p) => p.count >= 3 && Math.abs(p.mid.x - center_x) < 0.25 * this.h);
        const left = pieces.filter((p) => p.mid.x >= center_x).sort((a, b) => a.mid.x - b.mid.x)[0];
        const right = pieces.filter((p) => p.mid.x < center_x).sort((a, b) => b.mid.x - a.mid.x)[0];
        if (left === void 0 || right === void 0) return null;
        const middle = (left.mid.x + right.mid.x) / 2;
        if (Math.abs(middle - center_x) > 0.12 * this.h) return null;
        const size = (p) => Math.max(p.max_x - p.min_x, p.max_z - p.min_z);
        if (Math.max(size(left), size(right)) > 2.2 * Math.min(size(left), size(right))) return null;
        const overlap = right.max_x - left.min_x;
        if (overlap > 0.5 * Math.min(left.max_x - left.min_x, right.max_x - right.min_x)) return null;
        return [left, right];
      }
      /** the connected pieces of a thin horizontal slab, split wherever they are apart in x or z */
      slab_pieces(y, half_thickness = SLAB_STEP) {
        const { xs, zs } = this.cloud;
        const cell = GAP * this.h / 2;
        const cells = /* @__PURE__ */ new Map();
        for (const i of this.cloud.slab(y - half_thickness * this.h, y + half_thickness * this.h)) {
          const key = `${Math.floor(xs[i] / cell)},${Math.floor(zs[i] / cell)}`;
          const list2 = cells.get(key);
          if (list2 === void 0) cells.set(key, [i]);
          else list2.push(i);
        }
        const pieces = [];
        const seen = /* @__PURE__ */ new Set();
        for (const start of cells.keys()) {
          if (seen.has(start)) continue;
          seen.add(start);
          const piece = { min_x: Infinity, max_x: -Infinity, min_z: Infinity, max_z: -Infinity, mid: new Vector33(), count: 0 };
          const stack = [start];
          while (stack.length > 0) {
            const key = stack.pop();
            for (const i of cells.get(key)) {
              piece.min_x = Math.min(piece.min_x, xs[i]);
              piece.max_x = Math.max(piece.max_x, xs[i]);
              piece.min_z = Math.min(piece.min_z, zs[i]);
              piece.max_z = Math.max(piece.max_z, zs[i]);
              piece.count++;
            }
            const [cx, cz] = key.split(",").map(Number);
            for (let dx = -1; dx <= 1; dx++) {
              for (let dz = -1; dz <= 1; dz++) {
                const next = `${cx + dx},${cz + dz}`;
                if (!seen.has(next) && cells.has(next)) {
                  seen.add(next);
                  stack.push(next);
                }
              }
            }
          }
          piece.mid.set((piece.min_x + piece.max_x) / 2, y, (piece.min_z + piece.max_z) / 2);
          pieces.push(piece);
        }
        return pieces;
      }
      /**
       * A dress or coat hem looks like a crotch: the "legs" below it are wider than what's
       * above. A real crotch has hips about as wide as both legs together.
       */
      plausible_crotch(crotch_y, center_x) {
        if (crotch_y === null) return null;
        const above = this.central_interval(crotch_y + 0.02 * this.h, center_x);
        const below = [1, -1].map((side) => this.leg_interval(crotch_y - 0.02 * this.h, center_x, side)).filter((i) => i !== null);
        if (above === null || below.length === 0) return crotch_y;
        const legs_span = Math.max(...below.map((i) => i.max)) - Math.min(...below.map((i) => i.min));
        return (above.max - above.min) / legs_span < 0.8 ? null : crotch_y;
      }
      /**
       * The leg on one side of a slab below the crotch: the innermost x interval on that side
       * (hands hanging beside the thighs are further out), or null where the legs have joined.
       */
      leg_interval(y, center_x, side) {
        const pieces = this.x_intervals(y).filter((i) => side === 1 ? i.min > center_x && i.min - center_x < 0.25 * this.h : i.max < center_x && center_x - i.max < 0.25 * this.h);
        if (pieces.length === 0) return null;
        return pieces.sort((a, b) => side === 1 ? a.min - b.min : b.max - a.max)[0];
      }
      /** the x interval that contains the center line at height y, if any */
      central_interval(y, center_x) {
        return this.x_intervals(y).find((i) => i.min <= center_x && i.max >= center_x) ?? null;
      }
      find_torso_half_width(floor, center_x, crotch_y) {
        const start = crotch_y ?? floor + 0.47 * this.h;
        const half_widths = [];
        for (let f = 0.05; f <= 0.25; f += SLAB_STEP) {
          const interval = this.central_interval(start + f * this.h, center_x);
          if (interval !== null) half_widths.push((interval.max - interval.min) / 2);
        }
        if (half_widths.length === 0) return 0.1 * this.h;
        return Math.min(...half_widths);
      }
      /** T-posed arms join the body into one slab much wider than any torso or head */
      find_arm_line_y(floor, top, center_x) {
        let best_y = null;
        let best_width = 0.45 * this.h;
        for (let y = floor + 0.3 * this.h; y <= top - 0.05 * this.h; y += SLAB_STEP * this.h) {
          const interval = this.central_interval(y, center_x);
          if (interval !== null && interval.max - interval.min > best_width) {
            best_width = interval.max - interval.min;
            best_y = y;
          }
        }
        return best_y;
      }
      measure_arm(side, floor, center_x, crotch_y, torso_half_width, arm_line_y) {
        const legs_top = crotch_y ?? floor + 0.45 * this.h;
        const candidates = arm_line_y !== null ? this.cloud.slab(arm_line_y - 0.08 * this.h, arm_line_y + 0.08 * this.h) : this.cloud.slab(floor + 0.3 * this.h, this.cloud.max.y);
        const central_cache = /* @__PURE__ */ new Map();
        const arm_points = candidates.filter((i) => {
          const dx = (this.cloud.xs[i] - center_x) * side;
          if (dx <= 0) return false;
          const y = this.cloud.ys[i];
          if (y < legs_top) {
            return dx > torso_half_width * 1.6;
          }
          const key = Math.round((y - floor) / (SLAB_STEP * this.h));
          if (!central_cache.has(key)) {
            central_cache.set(key, this.central_interval(floor + key * SLAB_STEP * this.h, center_x));
          }
          const central = central_cache.get(key);
          if (arm_line_y !== null) return dx > torso_half_width * 1.35;
          if (central === null || central === void 0 || this.cloud.xs[i] < central.min || this.cloud.xs[i] > central.max) return true;
          return central.max - central.min > 0.45 * this.h && dx > torso_half_width * 1.35;
        });
        if (arm_points.length < 30) return null;
        const origin = new Vector33();
        for (const i of arm_points) origin.add(this.cloud.point(i));
        origin.divideScalar(arm_points.length);
        const cov = [0, 0, 0, 0, 0, 0];
        for (const i of arm_points) {
          const dx = this.cloud.xs[i] - origin.x;
          const dy = this.cloud.ys[i] - origin.y;
          const dz = this.cloud.zs[i] - origin.z;
          cov[0] += dx * dx;
          cov[1] += dx * dy;
          cov[2] += dx * dz;
          cov[3] += dy * dy;
          cov[4] += dy * dz;
          cov[5] += dz * dz;
        }
        let direction = new Vector33(side, -0.3, 0).normalize();
        for (let iteration = 0; iteration < 30; iteration++) {
          direction = new Vector33(
            cov[0] * direction.x + cov[1] * direction.y + cov[2] * direction.z,
            cov[1] * direction.x + cov[3] * direction.y + cov[4] * direction.z,
            cov[2] * direction.x + cov[4] * direction.y + cov[5] * direction.z
          ).normalize();
        }
        if (direction.x * side < 0) direction.negate();
        if (direction.x * side < 0.35) return null;
        let t_tip = -Infinity;
        for (const i of arm_points) {
          t_tip = Math.max(t_tip, this.cloud.point(i).sub(origin).dot(direction));
        }
        const t_edge = (center_x + side * torso_half_width - origin.x) / direction.x;
        if (t_tip - t_edge < 0.15 * this.h) return null;
        return { side, origin, direction, t_edge, t_tip };
      }
      /**
       * Arms hanging at the sides (I-pose, steep A-pose), which measure_arm skips: follow the
       * outermost piece of each horizontal slab below the shoulders and fit a line through
       * their middles. Null when the arm never separates from the body.
       */
      measure_hanging_arm(side, shoulder_y, center_x, torso_half_width, crotch_y, floor) {
        const points = [];
        const lowest = Math.max(floor + 0.2 * this.h, shoulder_y - 0.55 * this.h);
        const expected_x = (y) => {
          if (points.length === 0) return null;
          const last = points[points.length - 1];
          if (points.length < 3) return last.x;
          const first = points[Math.max(0, points.length - 6)];
          const slope = (last.x - first.x) / Math.min(-1e-9, last.y - first.y);
          return last.x + slope * (y - last.y);
        };
        let misses = 0;
        for (let y = shoulder_y - 0.08 * this.h; y >= lowest; y -= 0.01 * this.h) {
          const pieces = this.x_intervals(y).filter((piece) => side === 1 ? piece.min > center_x : piece.max < center_x);
          if (pieces.length === 0) {
            if (points.length > 0) break;
            continue;
          }
          const outer = side === 1 ? pieces[pieces.length - 1] : pieces[0];
          if (outer.max - outer.min > 0.12 * this.h) continue;
          const outer_mid = (outer.min + outer.max) / 2;
          const expected = expected_x(y);
          if (expected !== null && Math.abs(outer_mid - expected) > 0.04 * this.h) {
            if (++misses > 2) break;
            continue;
          }
          const inner_edge = side === 1 ? outer.min - center_x : center_x - outer.max;
          if (crotch_y !== null && y < crotch_y + 0.03 * this.h && inner_edge < torso_half_width * 0.9 && points.length === 0) continue;
          const mid = this.slab_mid(y, outer.min, outer.max, SLAB_STEP);
          if (mid !== null) {
            points.push(mid);
            misses = 0;
          }
        }
        if (points.length < 6) return null;
        const origin = new Vector33();
        for (const p of points) origin.add(p);
        origin.divideScalar(points.length);
        const cov = [0, 0, 0, 0, 0, 0];
        for (const p of points) {
          const d = p.clone().sub(origin);
          cov[0] += d.x * d.x;
          cov[1] += d.x * d.y;
          cov[2] += d.x * d.z;
          cov[3] += d.y * d.y;
          cov[4] += d.y * d.z;
          cov[5] += d.z * d.z;
        }
        let direction = new Vector33(0, -1, 0);
        for (let iteration = 0; iteration < 30; iteration++) {
          direction = new Vector33(
            cov[0] * direction.x + cov[1] * direction.y + cov[2] * direction.z,
            cov[1] * direction.x + cov[3] * direction.y + cov[4] * direction.z,
            cov[2] * direction.x + cov[4] * direction.y + cov[5] * direction.z
          ).normalize();
        }
        if (direction.y > 0) direction.negate();
        if (direction.y > -0.5) return null;
        let t_tip = -Infinity;
        for (const p of points) t_tip = Math.max(t_tip, p.clone().sub(origin).dot(direction));
        const t_edge = (shoulder_y - origin.y) / direction.y;
        return { side, origin, direction, t_edge, t_tip, hanging: true };
      }
      shoulder_height(arms, floor) {
        const heights = [...arms.values()].map((arm) => arm.origin.y + arm.direction.y * arm.t_edge);
        if (heights.length === 0) return floor + 0.8 * this.h;
        return heights.reduce((a, b) => a + b, 0) / heights.length;
      }
      find_neck_y(center_x, torso_half_width, shoulder_y, top) {
        let best_y = null;
        let best_width = Infinity;
        for (let y = shoulder_y + 0.01 * this.h; y <= top - 0.1 * this.h; y += SLAB_STEP * this.h) {
          const interval = this.central_interval(y, center_x);
          if (interval === null) continue;
          const width = interval.max - interval.min;
          if (width < best_width) {
            best_width = width;
            best_y = y;
          }
        }
        if (best_y === null || best_width > torso_half_width * 2 * 0.85) return null;
        let head_width = 0;
        for (let y = best_y + 0.02 * this.h; y <= top; y += SLAB_STEP * this.h) {
          const interval = this.central_interval(y, center_x);
          if (interval !== null) head_width = Math.max(head_width, interval.max - interval.min);
        }
        if (head_width < best_width * 1.25) return null;
        return best_y;
      }
      /** bounding-box middle of the points in a horizontal slab, limited to an x range */
      slab_mid(y, x_min, x_max, half_thickness = 0.01) {
        const slab = this.cloud.slab(y - half_thickness * this.h, y + half_thickness * this.h).filter((i) => this.cloud.xs[i] >= x_min && this.cloud.xs[i] <= x_max);
        return this.cloud.bounds_mid(slab);
      }
      /** bounding-box middle of the limb's cross-section through `point`, in the plane across `direction` */
      cross_section_mid(point, direction) {
        const center = point.clone();
        const half_thickness = 0.012 * this.h;
        const max_radius = 0.08 * this.h;
        const up = new Vector33(0, 1, 0).sub(direction.clone().multiplyScalar(direction.y)).normalize();
        const forward = new Vector33().crossVectors(direction, up).normalize();
        let up_min = Infinity;
        let up_max = -Infinity;
        let fwd_min = Infinity;
        let fwd_max = -Infinity;
        let found = 0;
        const slab = this.cloud.slab(center.y - max_radius - half_thickness, center.y + max_radius + half_thickness);
        for (const i of slab) {
          const offset = this.cloud.point(i).sub(center);
          const along = offset.dot(direction);
          if (Math.abs(along) > half_thickness) continue;
          const u = offset.dot(up);
          const f = offset.dot(forward);
          if (u * u + f * f > max_radius * max_radius) continue;
          up_min = Math.min(up_min, u);
          up_max = Math.max(up_max, u);
          fwd_min = Math.min(fwd_min, f);
          fwd_max = Math.max(fwd_max, f);
          found++;
        }
        if (found < 3) return null;
        return center.addScaledVector(up, (up_min + up_max) / 2).addScaledVector(forward, (fwd_min + fwd_max) / 2);
      }
    };
  }
});

// ../../rigger/src/lib/processes/edit-skeleton/auto-fit/HumanoidFit.ts
import { Quaternion as Quaternion2, Vector3 as Vector34 } from "three";
function fit_humanoid(cloud, template, parents) {
  const finder = new HumanoidLandmarkFinder(cloud);
  const lm = finder.measure();
  const H = lm.height;
  const at = (y_frac) => lm.floor + y_frac * H;
  const fitted = /* @__PURE__ */ new Map();
  const leg_x_range = (side) => side === 1 ? [lm.center_x, lm.center_x + lm.torso_half_width * 1.6] : [lm.center_x - lm.torso_half_width * 1.6, lm.center_x];
  const torso_mid_z = (y) => {
    const mid = finder.slab_mid(y, lm.center_x - lm.torso_half_width, lm.center_x + lm.torso_half_width);
    return mid?.z ?? (cloud.min.z + cloud.max.z) / 2;
  };
  const hip_y = lm.crotch_y !== null ? lm.crotch_y + C.thigh_above_crotch * H : at(C.thigh_y);
  const calf_y = lm.floor + C.calf_height_of_hip * (hip_y - lm.floor);
  const foot_y = lm.floor + C.foot_height_of_hip * (hip_y - lm.floor);
  const thigh_sample_y = (lm.crotch_y ?? hip_y) - C.thigh_sample_below_crotch * H;
  const shin_line_thighs = /* @__PURE__ */ new Map();
  for (const { side, suffix } of SIDES) {
    const [x_lo, x_hi] = leg_x_range(side);
    const leg_range = (y) => lm.crotch_y === null ? null : finder.leg_interval(y, lm.center_x, side);
    const leg_mid = (y) => {
      const range = leg_range(y);
      return (range !== null ? finder.slab_mid(y, range.min, range.max) : null) ?? finder.slab_mid(y, x_lo, x_hi) ?? new Vector34(lm.center_x + side * lm.torso_half_width * 0.5, y, torso_mid_z(y));
    };
    const calf = leg_mid(calf_y);
    fitted.set("calf" + suffix, new Vector34(calf.x, calf_y, calf.z + C.calf_dz * H));
    const foot_range = leg_range(foot_y);
    const foot = leg_mid(foot_y);
    fitted.set("foot" + suffix, new Vector34(foot.x, foot_y, foot.z + C.foot_dz * H));
    const thigh_sample = leg_mid(thigh_sample_y);
    const top = leg_range(thigh_sample_y);
    const calf_range = leg_range(calf_y);
    fitted.set("thigh" + suffix, new Vector34(thigh_sample.x, hip_y, thigh_sample.z + C.thigh_dz * H));
    if (top !== null && calf_range !== null && top.max - top.min > 1.6 * (calf_range.max - calf_range.min)) {
      const t = (hip_y - calf_y) / (calf_y - foot_y);
      shin_line_thighs.set(suffix, new Vector34(calf.x + (calf.x - foot.x) * t, hip_y, calf.z + (calf.z - foot.z) * t + C.thigh_dz * H));
    }
    const [sole_lo, sole_hi] = foot_range !== null ? [foot_range.min - 0.02 * H, foot_range.max + 0.02 * H] : [x_lo, x_hi];
    const sole = cloud.slab(lm.floor, lm.floor + 0.06 * H).filter((i) => cloud.xs[i] >= sole_lo && cloud.xs[i] <= sole_hi);
    let heel = foot.z - 0.05 * H;
    let toe = foot.z + 0.1 * H;
    if (sole.length > 0) {
      heel = Infinity;
      toe = -Infinity;
      for (const i of sole) {
        heel = Math.min(heel, cloud.zs[i]);
        toe = Math.max(toe, cloud.zs[i]);
      }
    }
    const foot_length = toe - heel;
    fitted.set("ball" + suffix, new Vector34(foot.x, lm.floor + C.ball_height_of_hip * (hip_y - lm.floor), heel + C.ball_of_foot_length * foot_length));
    fitted.set("ball_leaf" + suffix, new Vector34(foot.x, lm.floor + C.ball_leaf_y * H, heel + C.ball_leaf_of_foot_length * foot_length));
  }
  const level_arms = [...lm.arms.values()].filter((arm) => Math.abs(arm.direction.y) < C.level_arm_slope);
  const shoulder_y = level_arms.length > 0 ? level_arms.reduce((sum, arm) => sum + arm.origin.y + arm.direction.y * ((lm.center_x + arm.side * C.upperarm_x * H - arm.origin.x) / arm.direction.x), 0) / level_arms.length + C.upperarm_above_level_arm * H : lm.neck_y !== null ? lm.neck_y + C.from_neck.upperarm * H : lm.top - C.below_top.upperarm * H;
  const height_of = (bone) => {
    if (lm.neck_y !== null) return lm.neck_y + C.from_neck[bone] * H;
    if (level_arms.length > 0) return shoulder_y + C.of_shoulder_to_top[bone] * (lm.top - shoulder_y);
    return lm.top - C.below_top[bone] * H;
  };
  const pelvis_y = hip_y - C.pelvis_below_thigh * H;
  const neck_01_y = height_of("neck_01");
  const head_y = height_of("head");
  const head_leaf_y = Math.min(height_of("head_leaf"), lm.top);
  fitted.set("pelvis", new Vector34(lm.center_x, pelvis_y, torso_mid_z(pelvis_y) + C.pelvis_dz * H));
  C.spine_fractions.forEach((fraction, i) => {
    const y = pelvis_y + fraction * (neck_01_y - pelvis_y);
    fitted.set(`spine_0${i + 1}`, new Vector34(lm.center_x, y, torso_mid_z(y) + C.spine_dz[i] * H));
  });
  fitted.set("neck_01", new Vector34(lm.center_x, neck_01_y, torso_mid_z(neck_01_y) + C.neck_dz * H));
  fitted.set("head", new Vector34(lm.center_x, head_y, torso_mid_z(head_y) + C.head_dz * H));
  fitted.set("head_leaf", new Vector34(lm.center_x, head_leaf_y, torso_mid_z(head_leaf_y) + C.head_leaf_dz * H));
  let chest_half_width = Infinity;
  for (let y = shoulder_y - 0.15 * H; y <= shoulder_y - 0.03 * H; y += 5e-3 * H) {
    const interval = finder.central_interval(y, lm.center_x);
    if (interval !== null) chest_half_width = Math.min(chest_half_width, (interval.max - interval.min) / 2);
  }
  const shoulder_offset = Math.max(C.upperarm_x * H, Number.isFinite(chest_half_width) ? C.upperarm_x_of_chest * chest_half_width : 0);
  const arms = new Map(lm.arms);
  const fingertips = /* @__PURE__ */ new Map();
  if (arms.size === 0) {
    for (const { side } of SIDES) {
      const hanging = finder.measure_hanging_arm(side, shoulder_y, lm.center_x, lm.torso_half_width, lm.crotch_y, lm.floor);
      if (hanging !== null) arms.set(side, hanging);
    }
  }
  for (const { side, suffix } of SIDES) {
    const measured = arms.get(side);
    const arm = measured ?? arms.get(side === 1 ? -1 : 1);
    if (arm === void 0) {
      place_resting_arm(fitted, side, suffix, lm, shoulder_y, shoulder_offset, torso_mid_z(shoulder_y));
      continue;
    }
    const mirror = (p) => measured === void 0 ? p.setX(2 * lm.center_x - p.x) : p;
    const shoulder = new Vector34(lm.center_x + side * shoulder_offset, shoulder_y, torso_mid_z(shoulder_y) + C.upperarm_dz * H);
    const tip = mirror(arm.origin.clone().addScaledVector(arm.direction, arm.t_tip));
    if (arm.hanging === true && tip.distanceTo(shoulder) < C.hanging_arm_length * H) {
      const along2 = tip.clone().sub(shoulder).normalize();
      tip.copy(shoulder).addScaledVector(along2, C.hanging_arm_length * H);
    }
    fingertips.set(suffix, tip.clone());
    const reach = tip.clone().sub(shoulder);
    const reach_direction = reach.clone().normalize();
    const along = (fraction) => {
      const point = shoulder.clone().addScaledVector(reach, fraction);
      const probe = mirror(point.clone());
      const probe_direction = measured === void 0 ? reach_direction.clone().setX(-reach_direction.x) : reach_direction;
      const mid = finder.cross_section_mid(probe, probe_direction);
      return mid === null ? point : mirror(mid);
    };
    fitted.set("upperarm" + suffix, shoulder);
    fitted.set("lowerarm" + suffix, along(C.lowerarm_of_arm));
    fitted.set("hand" + suffix, along(C.hand_of_arm));
    const clavicle_y = shoulder.y + C.clavicle_dy * H;
    fitted.set("clavicle" + suffix, new Vector34(
      lm.center_x + C.clavicle_x_of_upperarm * (shoulder.x - lm.center_x),
      clavicle_y,
      torso_mid_z(clavicle_y) + C.clavicle_dz * H
    ));
  }
  for (const [suffix, thigh] of shin_line_thighs) {
    if (fitted.get("hand" + suffix).y < thigh_sample_y + 0.1 * H) fitted.set("thigh" + suffix, thigh);
  }
  symmetrize(fitted, lm.center_x);
  place_remaining_bones(fitted, template, parents);
  fit_fingers_to_tips(fitted, fingertips, parents);
  return { positions: fitted, landmarks: lm };
}
function place_resting_arm(fitted, side, suffix, lm, shoulder_y, shoulder_offset, z2) {
  const H = lm.height;
  const shoulder = new Vector34(lm.center_x + side * shoulder_offset, shoulder_y, z2 + C.upperarm_dz * H);
  const tip_y = Math.min(lm.crotch_y ?? lm.floor + 0.47 * H, shoulder_y - 0.3 * H);
  const tip = new Vector34(lm.center_x + side * (lm.torso_half_width + 0.035 * H), tip_y, shoulder.z);
  const reach = tip.clone().sub(shoulder);
  fitted.set("upperarm" + suffix, shoulder);
  fitted.set("lowerarm" + suffix, shoulder.clone().addScaledVector(reach, C.lowerarm_of_arm));
  fitted.set("hand" + suffix, shoulder.clone().addScaledVector(reach, C.hand_of_arm));
  const clavicle_y = shoulder.y + C.clavicle_dy * H;
  fitted.set("clavicle" + suffix, new Vector34(lm.center_x + C.clavicle_x_of_upperarm * (shoulder.x - lm.center_x), clavicle_y, z2 + C.clavicle_dz * H));
}
function symmetrize(fitted, center_x) {
  for (const [name, left] of fitted) {
    if (!name.endsWith("_l")) continue;
    const right = fitted.get(name.slice(0, -2) + "_r");
    if (right === void 0) continue;
    const half_span = (left.x - center_x - (right.x - center_x)) / 2;
    const y = (left.y + right.y) / 2;
    const z2 = (left.z + right.z) / 2;
    left.set(center_x + half_span, y, z2);
    right.set(center_x - half_span, y, z2);
  }
}
function place_remaining_bones(fitted, template, parents) {
  const body_scale = skeleton_height(fitted) / Math.max(skeleton_height(template), 1e-6);
  const hand_transform = /* @__PURE__ */ new Map();
  for (const side of ["_l", "_r"]) {
    const t_lower = template.get("lowerarm" + side);
    const t_hand = template.get("hand" + side);
    const f_lower = fitted.get("lowerarm" + side);
    const f_hand = fitted.get("hand" + side);
    if (t_lower === void 0 || t_hand === void 0 || f_lower === void 0 || f_hand === void 0) continue;
    const t_forearm = t_hand.clone().sub(t_lower);
    const f_forearm = f_hand.clone().sub(f_lower);
    hand_transform.set("hand" + side, {
      rotation: new Quaternion2().setFromUnitVectors(t_forearm.clone().normalize(), f_forearm.clone().normalize()),
      scale: f_forearm.length() / Math.max(t_forearm.length(), 1e-6)
    });
  }
  const order = [...template.keys()].sort((a, b) => depth(a, parents) - depth(b, parents));
  for (const bone of order) {
    if (fitted.has(bone)) continue;
    const parent = parents.get(bone);
    if (parent === void 0 || !fitted.has(parent) || !template.has(parent)) {
      continue;
    }
    const hand = [...hand_transform.keys()].find((name) => is_under(bone, name, parents));
    const transform = hand !== void 0 ? hand_transform.get(hand) : { rotation: new Quaternion2(), scale: body_scale };
    const offset = template.get(bone).clone().sub(template.get(parent)).multiplyScalar(transform.scale).applyQuaternion(transform.rotation);
    fitted.set(bone, fitted.get(parent).clone().add(offset));
  }
}
function fit_fingers_to_tips(fitted, fingertips, parents) {
  for (const [suffix, tip] of fingertips) {
    const hand = fitted.get("hand" + suffix);
    if (hand === void 0) continue;
    const to_tip = tip.clone().sub(hand);
    const length = to_tip.length();
    if (length < 1e-6) continue;
    const direction = to_tip.divideScalar(length);
    const fingers = [...fitted.keys()].filter((bone) => bone !== "hand" + suffix && is_under(bone, "hand" + suffix, parents));
    const reach = Math.max(0, ...fingers.map((bone) => fitted.get(bone).clone().sub(hand).dot(direction)));
    if (reach <= length) continue;
    const scale = length / reach;
    for (const bone of fingers) fitted.get(bone).sub(hand).multiplyScalar(scale).add(hand);
  }
}
function skeleton_height(positions) {
  const head = positions.get("head_leaf");
  const foot = positions.get("ball_l") ?? positions.get("foot_l");
  return head !== void 0 && foot !== void 0 ? head.y - foot.y : 0;
}
function depth(bone, parents) {
  let d = 0;
  let current = parents.get(bone);
  while (current !== void 0) {
    d++;
    current = parents.get(current);
  }
  return d;
}
function is_under(bone, ancestor, parents) {
  let current = parents.get(bone);
  while (current !== void 0) {
    if (current === ancestor) return true;
    current = parents.get(current);
  }
  return false;
}
var C, SIDES;
var init_HumanoidFit = __esm({
  "../../rigger/src/lib/processes/edit-skeleton/auto-fit/HumanoidFit.ts"() {
    "use strict";
    init_HumanoidLandmarks();
    C = {
      thigh_above_crotch: 0.06,
      pelvis_below_thigh: 7e-3,
      thigh_sample_below_crotch: 0.03,
      thigh_dz: -75e-4,
      calf_height_of_hip: 0.558,
      calf_dz: 6e-3,
      foot_height_of_hip: 0.106,
      foot_dz: -0.0255,
      ball_height_of_hip: 0.02,
      ball_of_foot_length: 0.705,
      ball_leaf_of_foot_length: 1,
      ball_leaf_y: 74e-4,
      // shoulder joint: distance from the center line is the larger of these two
      upperarm_x: 0.078,
      upperarm_x_of_chest: 0.94,
      upperarm_dz: -8e-3,
      // arms flatter than this slope count as a T-pose
      level_arm_slope: 0.3,
      upperarm_above_level_arm: 0.028,
      // elbow and wrist, as fractions of shoulder joint -> fingertips
      lowerarm_of_arm: 0.381,
      hanging_arm_length: 0.4,
      // shoulder to fingertips, in model heights
      hand_of_arm: 0.753,
      clavicle_x_of_upperarm: 0.136,
      clavicle_dy: -0.0104,
      clavicle_dz: 0.04,
      spine_fractions: [0.207, 0.433, 0.686],
      // spine_01..03 between pelvis and neck_01
      pelvis_dz: -0.0213,
      spine_dz: [-95e-4, -71e-4, -34e-4],
      neck_dz: -0.0158,
      head_dz: 83e-4,
      head_leaf_dz: 72e-4,
      // heights relative to the narrowest point of the neck
      from_neck: { neck_01: -0.066, head: -14e-4, head_leaf: 0.037, upperarm: -0.08 },
      // fractions of shoulder -> top of the model, when the neck can't be found
      of_shoulder_to_top: { neck_01: 0.064, head: 0.354, head_leaf: 0.545 },
      // heights below the top of the model, when neither neck nor shoulders can be found
      below_top: { neck_01: 0.185, head: 0.127, head_leaf: 0.094, upperarm: 0.205 },
      // used when the legs never separate (robes, dresses)
      thigh_y: 0.497
    };
    SIDES = [{ side: 1, suffix: "_l" }, { side: -1, suffix: "_r" }];
  }
});

// ../../rigger/src/lib/processes/edit-skeleton/auto-fit/CreatureFit.ts
import { Box3, Vector3 as Vector35 } from "three";
function fit_creature(cloud, template, skeleton_type) {
  const reference = REFERENCE_BOUNDS[skeleton_type];
  const fitted = /* @__PURE__ */ new Map();
  if (reference === void 0) return fitted;
  const bones = [...template.entries()].filter(([name]) => name !== "root");
  const bone_box = new Box3().setFromPoints(bones.map(([, p]) => p));
  const bone_size = bone_box.getSize(new Vector35());
  const model_size = new Vector35().subVectors(cloud.max, cloud.min);
  const ref_min = new Vector35();
  const ref_max = new Vector35();
  AXES.forEach((axis, a) => {
    ref_min[axis] = bone_box.min[axis] + reference.min[a] * bone_size[axis];
    ref_max[axis] = bone_box.min[axis] + reference.max[a] * bone_size[axis];
    if (ref_max[axis] - ref_min[axis] < 1e-6) {
      ref_min[axis] = bone_box.min[axis] - model_size[axis] / 2;
      ref_max[axis] = bone_box.min[axis] + model_size[axis] / 2;
    }
  });
  const ref_size = new Vector35().subVectors(ref_max, ref_min);
  const ref_diagonal = ref_size.length();
  const offset = new Vector35().subVectors(cloud.min, ref_min).length() + new Vector35().subVectors(cloud.max, ref_max).length();
  const size_ratio = model_size.length() / ref_diagonal;
  if (size_ratio > 0.8 && size_ratio < 1.25 && offset < 0.15 * ref_diagonal) return fitted;
  for (const [name, position] of bones) {
    const out = new Vector35();
    AXES.forEach((axis) => {
      const u = (position[axis] - ref_min[axis]) / (ref_max[axis] - ref_min[axis]);
      out[axis] = cloud.min[axis] + u * model_size[axis];
    });
    fitted.set(name, out);
  }
  return fitted;
}
var REFERENCE_BOUNDS, AXES;
var init_CreatureFit = __esm({
  "../../rigger/src/lib/processes/edit-skeleton/auto-fit/CreatureFit.ts"() {
    "use strict";
    init_SkeletonType();
    REFERENCE_BOUNDS = {
      ["fox" /* Fox */]: { min: [-0.082, -0.018, -0.015], max: [1.082, 1.013, 1.009] },
      ["bird" /* Bird */]: { min: [-0.027, -0.026, -0.052], max: [1.027, 1.042, 1.017] },
      ["dragon" /* Dragon */]: { min: [-0.041, -0.023, -0.015], max: [1.041, 1.043, 1.007] },
      ["kaiju" /* Kaiju */]: { min: [-7e-3, -0.039, -8e-3], max: [1.007, 1.053, 1.003] },
      ["spider" /* Spider */]: { min: [-0.015, -3e-3, -0.026], max: [1.015, 1.104, 1.019] },
      ["snake" /* Snake */]: { min: [0, -0.099, -0.017], max: [0, 1.308, 1.016] },
      ["fish" /* Fish */]: { min: [-0.033, -0.027, -0.117], max: [1.033, 2.065, 1.038] },
      ["horse" /* Horse */]: { min: [-0.3, -6e-3, 7e-3], max: [1.3, 1.014, 1.001] }
    };
    AXES = ["x", "y", "z"];
  }
});

// ../../rigger/src/lib/interfaces/BoneTransformState.ts
var BoneTransformState;
var init_BoneTransformState = __esm({
  "../../rigger/src/lib/interfaces/BoneTransformState.ts"() {
    "use strict";
    BoneTransformState = class {
      constructor(name = "", position, rotation, scale) {
        this.name = name;
        this.position = position;
        this.rotation = rotation;
        this.scale = scale;
      }
    };
  }
});

// ../../rigger/src/lib/interfaces/IntersectionPointData.ts
var IntersectionPointData;
var init_IntersectionPointData = __esm({
  "../../rigger/src/lib/interfaces/IntersectionPointData.ts"() {
    "use strict";
    IntersectionPointData = class {
      constructor(vertex_positions, vertex_indices) {
        this.vertex_positions = [];
        this.vertex_indices = [];
        this.vertex_positions = vertex_positions;
        this.vertex_indices = vertex_indices;
      }
    };
  }
});

// ../../rigger/src/lib/Utilities.ts
import {
  Vector3 as Vector36,
  Vector2,
  Mesh,
  Group,
  Bone,
  Euler as Euler2,
  Raycaster
} from "three";
var Utility;
var init_Utilities = __esm({
  "../../rigger/src/lib/Utilities.ts"() {
    "use strict";
    init_BoneTransformState();
    init_IntersectionPointData();
    Utility = class _Utility {
      static distance_between_objects(object_1, object_2) {
        const object_1_position = new Vector36();
        const object_2_position = new Vector36();
        object_1.getWorldPosition(object_1_position);
        object_2.getWorldPosition(object_2_position);
        return object_1_position.distanceTo(object_2_position);
      }
      /**
       * Converts an object's local position to world position
       * This is similar to "localToWorld()", but makes sure the object's world matrix is up to date
       * https://stackoverflow.com/questions/70016922/three-js-getworldposition-localtoworld-position-not-correct
       * (see Mugen87's comment at the bottom)
       * @param {*} object
       * @returns local position for object in a Vector3 object
       */
      static world_position_from_object(object) {
        const position = new Vector36();
        return object.getWorldPosition(position);
      }
      static direction_between_points(point_1, point_2) {
        const direction = new Vector36();
        direction.subVectors(point_2, point_1).normalize();
        return direction;
      }
      static is_point_in_box(point, box_mesh) {
        box_mesh.updateMatrixWorld();
        const local_point = box_mesh.worldToLocal(point.clone());
        if (box_mesh.geometry.boundingBox === null) {
          console.warn("is_point_in_box() - box_mesh does not have a bounding box", box_mesh);
          return false;
        }
        return box_mesh.geometry.boundingBox.containsPoint(local_point);
      }
      static remove_object_array(obj) {
        obj.traverse((child) => {
          if (child instanceof Mesh) {
            child.geometry.dispose();
            for (const key in child.material) {
              const value = child.material[key];
              if (value && typeof value.dispose === "function") {
                value.dispose();
              }
            }
            obj.remove(obj);
          }
        });
      }
      static remove_object_with_children(obj) {
        if (obj.children.length > 0) {
          obj.children.forEach((child) => {
            this.remove_object_with_children(child);
          });
        }
        if (obj instanceof Mesh) {
          if (obj.geometry !== null) {
            obj.geometry.dispose();
          }
          if (obj.material !== void 0) {
            if (Array.isArray(obj.material)) {
              obj.material.forEach((material) => {
                if (material.map) {
                  material.map.dispose();
                }
                material.dispose();
              });
            } else {
              if (obj.material.map) {
                obj.material.map.dispose();
              }
              obj.material.dispose();
            }
          }
        }
        if (obj.parent != null) {
          obj.parent.remove(obj);
        }
        obj.removeFromParent();
      }
      /**
       * A "leaf" bone is an orientation-only tip at the end of a chain (finger/toe
       * tips, head top, tail/ear/wing tips). These are not meant to be animated, so
       * the skinning algorithm ignores them. Identified as childless AND name-marked.
       * Human rigs mark them with `_leaf`; the animal rigs mark them with `tip`.
       */
      static is_leaf_bone(bone) {
        if (bone.children.length > 0) return false;
        const name = bone.name.toLowerCase();
        return name.includes("leaf") || name.includes("tip");
      }
      /**
       * The point halfway between a bone's start joint and its first child's joint.
       * This is the reference point the skinning solvers measure vertex distances
       * against — a bone's "center of mass" rather than its start joint, which
       * keeps long bones from losing vertices to their neighbors.
       * Childless bones fall back to their own world position.
       */
      static bone_midpoint_to_child(bone) {
        const bone_position = _Utility.world_position_from_object(bone);
        if (bone.children.length === 0) {
          return bone_position.clone();
        }
        const child = bone.children[0];
        const child_position = _Utility.world_position_from_object(child);
        return new Vector36().lerpVectors(bone_position, child_position, 0.5);
      }
      static bone_list_from_hierarchy(bone_hierarchy) {
        if (bone_hierarchy === void 0 || bone_hierarchy === null) {
          console.warn("bone_hierarchy is undefined or null");
          return [];
        }
        const bones = [];
        bone_hierarchy.traverse((bone) => {
          if (bone instanceof Bone) {
            bones.push(bone);
          }
        });
        return bones;
      }
      static intersection_points_between_positions_and_mesh(positions, envelope_mesh) {
        const vertex_positions_inside_bone_envelope = [];
        const vertex_indexes_inside_bone_evelope = [];
        const vertex_count = positions.array.length / 3;
        for (let i = 0; i < vertex_count; i++) {
          const vertex_position = new Vector36().fromBufferAttribute(positions, i);
          const is_intersecting = _Utility.is_point_in_box(vertex_position, envelope_mesh);
          if (is_intersecting) {
            vertex_positions_inside_bone_envelope.push(vertex_position);
            vertex_indexes_inside_bone_evelope.push(i);
          }
        }
        return new IntersectionPointData(vertex_positions_inside_bone_envelope, vertex_indexes_inside_bone_evelope);
      }
      /**
       * From a mouse event, return a normalized vector2 for screen space between -1 and 1 (0 being center of screen)
       * This is used for turning a mouse event into a raycaster when determining screen space intersections
       * Top right of screen would return 1, 1. Bottom left would return -1, -1
       * @param {*} mouse_event
       * @returns x and y coordinates normalized between -1 and 1
       */
      static normalized_mouse_position(mouse_event) {
        const mouse = new Vector2();
        mouse.x = mouse_event.clientX / window.innerWidth * 2 - 1;
        mouse.y = -(mouse_event.clientY / window.innerHeight) * 2 + 1;
        return mouse;
      }
      /**
       * Store all the debugging objects in a separate group so they can be easily organized
       * and removed when needed
       * @param {*} scene
       * @returns
       */
      static regenerate_debugging_scene(scene) {
        const debugging_object_name = "Skinning Debug Container";
        const existing_debugging_container = scene.getObjectByName(
          debugging_object_name
        );
        if (existing_debugging_container !== void 0) {
          this.remove_object_array(existing_debugging_container);
          existing_debugging_container.clear();
          scene.remove(existing_debugging_container);
        }
        const debugging_scene_object = new Group();
        debugging_scene_object.name = debugging_object_name;
        scene.add(debugging_scene_object);
        return debugging_scene_object;
      }
      static store_bone_transforms(skeleton) {
        const bone_transforms = [];
        skeleton.bones.forEach((bone) => {
          const new_rotation = new Vector36().setFromEuler(bone.rotation);
          const new_transform_state = new BoneTransformState(
            bone.name,
            bone.position.clone(),
            new_rotation,
            bone.scale.clone()
          );
          bone_transforms.push(new_transform_state);
        });
        return bone_transforms;
      }
      static restore_bone_transforms(skeleton, original_bone_transforms) {
        original_bone_transforms.forEach((bone_transform) => {
          const bone = skeleton.bones.find((bone2) => bone2.name === bone_transform.name) ?? null;
          if (bone !== null) {
            bone.position.copy(bone_transform.position);
            const euler = new Euler2();
            euler.setFromVector3(bone_transform.rotation);
            bone.rotation.copy(euler);
            bone.scale.copy(bone_transform.scale);
          }
        });
      }
      static calculate_bone_base_name(bone_name) {
        let normalized_bone_name = bone_name.toLowerCase().replace(/(_r|_l|_right|_left)$/, "");
        normalized_bone_name = normalized_bone_name.replace(/^(r_|l_|right_|left_)/, "");
        return normalized_bone_name;
      }
      // Find the closest bone for raycaster using screen-space distance to account for camera zoom
      static raycast_closest_bone_test(camera, mouse_event, skeleton) {
        const raycaster = new Raycaster();
        raycaster.setFromCamera(_Utility.normalized_mouse_position(mouse_event), camera);
        const mouse_position = _Utility.normalized_mouse_position(mouse_event);
        let closest_bone = null;
        let closest_bone_index = 0;
        let closest_distance = Infinity;
        skeleton.bones.forEach((bone, bone_index) => {
          const world_position = _Utility.world_position_from_object(bone);
          const bone_screen_position = world_position.clone().project(camera);
          const screen_distance = mouse_position.distanceTo(new Vector2(bone_screen_position.x, bone_screen_position.y));
          if (screen_distance < closest_distance) {
            closest_bone = bone;
            closest_distance = screen_distance;
            closest_bone_index = bone_index;
          }
        });
        const output = [closest_bone, closest_bone_index, closest_distance];
        return output;
      }
      static scale_armature_by_scalar(armature, scalar) {
        armature.traverse((bone) => {
          if (bone.type === "Bone") {
            bone.position.multiplyScalar(scalar);
          }
        });
      }
      static clean_bone_name_for_messaging(bone_name) {
        return bone_name.replace("mixamorig_", "");
      }
      static find_closest_bone_index_from_vertex_index(vertex_index, geometry, bones) {
        const vertex_position = new Vector36().fromBufferAttribute(geometry.attributes.position, vertex_index);
        let closest_bone_distance = 1e4;
        let closest_bone_index = 0;
        bones.forEach((bone, idx) => {
          let distance = _Utility.world_position_from_object(bone.bone_object).distanceTo(vertex_position);
          if (bone.has_child_bone) {
            const child_bone = bone.bone_object.children[0];
            const child_bone_position = _Utility.world_position_from_object(child_bone);
            const bone_position = _Utility.world_position_from_object(bone.bone_object);
            const half_way_point = bone_position.add(child_bone_position).divideScalar(2);
            const distance_to_half_way_point = half_way_point.distanceTo(vertex_position);
            if (distance_to_half_way_point < closest_bone_distance) {
              distance = distance_to_half_way_point;
            }
          }
          if (distance < closest_bone_distance) {
            closest_bone_distance = distance;
            closest_bone_index = idx;
          }
        });
        return closest_bone_index;
      }
      static get_file_extension(file_path) {
        const file_name = file_path.split("/").pop();
        if (file_name === void 0) {
          console.error("Critical Error: Undefined file extension when loading model");
          return "UNDEFINED";
        }
        const file_extension = file_name?.split(".").pop();
        if (file_extension === void 0) {
          console.error('Critical Error: File does not have a "." symbol in the name');
          return "UNDEFINED";
        }
        return file_extension;
      }
      static parse_input_number(value) {
        if (value === void 0 || value === null) {
          return 0;
        }
        value = value.trim();
        if (value === "") {
          return 0;
        }
        const value_numeric = parseFloat(value);
        if (typeof value_numeric !== "number" || !isFinite(value_numeric)) {
          return 0;
        }
        return value_numeric;
      }
      static enum_from_value(val, enumType) {
        const enumName = Object.keys(enumType).find((k) => enumType[k] === val);
        return enumName === void 0 ? void 0 : enumType[enumName];
      }
    };
  }
});

// ../../rigger/src/lib/solvers/HeadWeightCorrector.ts
import { Vector3 as Vector37 } from "three";
var HeadWeightCorrector;
var init_HeadWeightCorrector = __esm({
  "../../rigger/src/lib/solvers/HeadWeightCorrector.ts"() {
    "use strict";
    HeadWeightCorrector = class {
      constructor(geometry, bones_master_data, preview_plane_height) {
        this.geometry = geometry;
        this.bones_master_data = bones_master_data;
        this.preview_plane_height = preview_plane_height;
      }
      /**
       * Apply head weight correction to the skin indices and weights
       * @param skin_indices Array of bone indices for each vertex (4 per vertex)
       * @param skin_weights Array of bone weights for each vertex (4 per vertex)
       */
      apply_head_weight_correction(skin_indices, skin_weights) {
        const head_bone_index = this.find_head_bone_index();
        if (head_bone_index === -1) {
          return;
        }
        const arm_bone_indices = this.find_arm_bone_indices();
        if (arm_bone_indices.length === 0) {
          return;
        }
        this.correct_vertex_weights(skin_indices, skin_weights, head_bone_index, arm_bone_indices);
      }
      /**
       * Find the index of the head bone (looking for "DEF-head" or similar)
       */
      find_head_bone_index() {
        const head_bone_names = ["DEF-head", "head", "Head", "HEAD"];
        for (let i = 0; i < this.bones_master_data.length; i++) {
          const bone_name = this.bones_master_data[i].name;
          if (head_bone_names.includes(bone_name)) {
            return i;
          }
          const lower_bone_name = bone_name.toLowerCase();
          if (head_bone_names.some(
            (name) => lower_bone_name.includes(name.toLowerCase())
          )) {
            return i;
          }
        }
        return -1;
      }
      /**
       * Find the indices of arm bones (looking for arm, shoulder, hand bones)
       */
      find_arm_bone_indices() {
        const arm_bone_keywords = [
          "arm",
          "shoulder",
          "hand",
          "finger",
          "thumb",
          "elbow",
          "forearm",
          "upperarm",
          "thumb",
          "index",
          "middle",
          "ring",
          "pinky"
        ];
        const arm_bone_indices = [];
        for (let i = 0; i < this.bones_master_data.length; i++) {
          const bone_name = this.bones_master_data[i].name.toLowerCase();
          if (arm_bone_keywords.some((keyword) => bone_name.includes(keyword))) {
            arm_bone_indices.push(i);
          }
        }
        return arm_bone_indices;
      }
      /**
       * Correct vertex weights for vertices above the height threshold
       */
      correct_vertex_weights(skin_indices, skin_weights, head_bone_index, arm_bone_indices) {
        const vertex_count = this.geometry.attributes.position.array.length / 3;
        let corrected_count = 0;
        for (let i = 0; i < vertex_count; i++) {
          const vertex_position = new Vector37().fromBufferAttribute(this.geometry.attributes.position, i);
          if (vertex_position.y <= this.preview_plane_height) {
            continue;
          }
          const offset = i * 4;
          const primary_bone_index = skin_indices[offset];
          const primary_weight = skin_weights[offset];
          if (arm_bone_indices.includes(primary_bone_index) && primary_weight > 0.5) {
            skin_indices[offset] = head_bone_index;
            skin_indices[offset + 1] = 0;
            skin_indices[offset + 2] = 0;
            skin_indices[offset + 3] = 0;
            skin_weights[offset] = 1;
            skin_weights[offset + 1] = 0;
            skin_weights[offset + 2] = 0;
            skin_weights[offset + 3] = 0;
            corrected_count++;
            continue;
          }
          for (let j = 0; j < 4; j++) {
            const bone_index = skin_indices[offset + j];
            const weight = skin_weights[offset + j];
            if (arm_bone_indices.includes(bone_index) && weight > 0.3) {
              let head_slot = -1;
              for (let k = 0; k < 4; k++) {
                if (skin_indices[offset + k] === head_bone_index) {
                  head_slot = k;
                  break;
                }
              }
              if (head_slot === -1) {
                skin_indices[offset + j] = head_bone_index;
              } else {
                skin_weights[offset + head_slot] += weight;
                skin_weights[offset + j] = 0;
                skin_indices[offset + j] = 0;
              }
              corrected_count++;
            }
          }
          this.normalize_vertex_weights(skin_weights, offset);
        }
        return corrected_count;
      }
      /**
       * Normalize weights for a single vertex to ensure they sum to 1.0
       */
      normalize_vertex_weights(skin_weights, offset) {
        const total_weight = skin_weights[offset] + skin_weights[offset + 1] + skin_weights[offset + 2] + skin_weights[offset + 3];
        if (total_weight > 0) {
          skin_weights[offset] /= total_weight;
          skin_weights[offset + 1] /= total_weight;
          skin_weights[offset + 2] /= total_weight;
          skin_weights[offset + 3] /= total_weight;
        }
      }
    };
  }
});

// ../../rigger/src/lib/solvers/ArmWeightCorrector.ts
import {
  Vector3 as Vector38,
  Bone as Bone2
} from "three";
var ArmWeightCorrector;
var init_ArmWeightCorrector = __esm({
  "../../rigger/src/lib/solvers/ArmWeightCorrector.ts"() {
    "use strict";
    init_Utilities();
    ArmWeightCorrector = class _ArmWeightCorrector {
      constructor(geometry, bones_master_data, arm_plane_offset) {
        this.geometry = geometry;
        this.bones = bones_master_data;
        this.arm_plane_offset = arm_plane_offset;
      }
      /**
       * Distance from the model's center line to the shoulder joint, which is where
       * the arm plane sits when the user's offset is zero.
       *
       * Shared with the edit-skeleton preview so the plane the user sees and the
       * plane the solver uses are derived the same way. The solver runs against a
       * clone of the edited armature, so both recompute this from bones rather than
       * passing an absolute coordinate around.
       *
       * @returns the absolute world X of the shoulder joint, or null if no arm bone was found
       */
      static shoulder_anchor_x(bones) {
        const shoulder_bone = _ArmWeightCorrector.find_shoulder_bone(bones);
        if (shoulder_bone === void 0) {
          return null;
        }
        return Math.abs(Utility.world_position_from_object(shoulder_bone).x);
      }
      /**
       * The bone the arm plane is anchored to. Human rigs name it `upperarm_l`;
       * the fallbacks cover rigs that use other conventions.
       */
      static find_shoulder_bone(bones) {
        const name_priority = ["upperarm", "shoulder", "arm"];
        for (const keyword of name_priority) {
          const match = bones.find((bone) => bone.name.toLowerCase().includes(keyword));
          if (match !== void 0) {
            return match;
          }
        }
        return void 0;
      }
      /**
       * Reassign arm-bone weights on vertices inboard of the arm plane.
       * Modifies skin_indices and skin_weights in place. Runs before smoothing so
       * the smoother blends the new torso/arm boundary instead of leaving a seam.
       */
      apply_arm_weight_correction(skin_indices, skin_weights) {
        const anchor_x = _ArmWeightCorrector.shoulder_anchor_x(this.bones);
        if (anchor_x === null) {
          return;
        }
        const plane_x = anchor_x + this.arm_plane_offset;
        if (plane_x <= 0) {
          return;
        }
        const arm_bone_indices = this.find_arm_bone_indices();
        if (arm_bone_indices.size === 0) {
          return;
        }
        const fallback_bones = this.build_fallback_bone_candidates(arm_bone_indices);
        if (fallback_bones.length === 0) {
          return;
        }
        this.correct_vertex_weights(skin_indices, skin_weights, plane_x, arm_bone_indices, fallback_bones);
      }
      /**
       * Every upperarm bone plus all of its descendants (lowerarm, hand, fingers),
       * on both sides. Walking the hierarchy rather than matching a keyword list
       * gives exactly "upperarm and below" without needing to enumerate every
       * finger bone name, and it leaves the clavicle alone.
       */
      find_arm_bone_indices() {
        const bone_to_index = /* @__PURE__ */ new Map();
        this.bones.forEach((bone, idx) => bone_to_index.set(bone, idx));
        const arm_bone_indices = /* @__PURE__ */ new Set();
        this.bones.forEach((bone) => {
          if (!bone.name.toLowerCase().includes("upperarm")) {
            return;
          }
          bone.traverse((descendant) => {
            if (!(descendant instanceof Bone2)) {
              return;
            }
            const index = bone_to_index.get(descendant);
            if (index !== void 0) {
              arm_bone_indices.add(index);
            }
          });
        });
        return arm_bone_indices;
      }
      /**
       * Bones a stripped vertex can be handed to: everything that isn't an arm bone,
       * minus the root (global transform only) and leaf/orientation bones, which the
       * solver never assigns vertices to.
       */
      build_fallback_bone_candidates(arm_bone_indices) {
        const candidates = [];
        this.bones.forEach((bone, idx) => {
          if (arm_bone_indices.has(idx)) {
            return;
          }
          if (bone.name === "root" || Utility.is_leaf_bone(bone)) {
            return;
          }
          candidates.push({ index: idx, midpoint: Utility.bone_midpoint_to_child(bone) });
        });
        return candidates;
      }
      correct_vertex_weights(skin_indices, skin_weights, plane_x, arm_bone_indices, fallback_bones) {
        const vertex_count = this.geometry.attributes.position.array.length / 3;
        for (let i = 0; i < vertex_count; i++) {
          const vertex_position = new Vector38().fromBufferAttribute(this.geometry.attributes.position, i);
          if (Math.abs(vertex_position.x) >= plane_x) {
            continue;
          }
          const offset = i * 4;
          let stolen_weight = 0;
          let first_freed_slot = -1;
          for (let j = 0; j < 4; j++) {
            if (!arm_bone_indices.has(skin_indices[offset + j])) {
              continue;
            }
            if (skin_weights[offset + j] <= 0) {
              continue;
            }
            stolen_weight += skin_weights[offset + j];
            skin_weights[offset + j] = 0;
            skin_indices[offset + j] = 0;
            if (first_freed_slot === -1) {
              first_freed_slot = j;
            }
          }
          if (stolen_weight <= 0) {
            continue;
          }
          const replacement_bone_index = this.find_closest_fallback_bone(vertex_position, fallback_bones);
          let target_slot = -1;
          for (let j = 0; j < 4; j++) {
            if (skin_indices[offset + j] === replacement_bone_index && skin_weights[offset + j] > 0) {
              target_slot = j;
              break;
            }
          }
          if (target_slot === -1) {
            target_slot = first_freed_slot;
            skin_indices[offset + target_slot] = replacement_bone_index;
          }
          skin_weights[offset + target_slot] += stolen_weight;
          this.normalize_vertex_weights(skin_weights, offset);
        }
      }
      find_closest_fallback_bone(vertex_position, fallback_bones) {
        let closest_distance = Infinity;
        let closest_index = fallback_bones[0].index;
        for (const candidate of fallback_bones) {
          const distance = candidate.midpoint.distanceTo(vertex_position);
          if (distance < closest_distance) {
            closest_distance = distance;
            closest_index = candidate.index;
          }
        }
        return closest_index;
      }
      /**
       * Normalize weights for a single vertex to ensure they sum to 1.0
       */
      normalize_vertex_weights(skin_weights, offset) {
        const total_weight = skin_weights[offset] + skin_weights[offset + 1] + skin_weights[offset + 2] + skin_weights[offset + 3];
        if (total_weight > 0) {
          skin_weights[offset] /= total_weight;
          skin_weights[offset + 1] /= total_weight;
          skin_weights[offset + 2] /= total_weight;
          skin_weights[offset + 3] /= total_weight;
        }
      }
    };
  }
});

// ../../rigger/src/lib/solvers/WeightCalculator.ts
import {
  Vector3 as Vector39,
  Raycaster as Raycaster2,
  Mesh as Mesh2,
  MeshBasicMaterial,
  DoubleSide
} from "three";
function distance_to_segment(point, a, b) {
  const ab = b.clone().sub(a);
  const length_sq = ab.lengthSq();
  const t = length_sq < 1e-12 ? 0 : Math.max(0, Math.min(1, point.clone().sub(a).dot(ab) / length_sq));
  return point.distanceTo(a.clone().addScaledVector(ab, t));
}
var WeightCalculator;
var init_WeightCalculator = __esm({
  "../../rigger/src/lib/solvers/WeightCalculator.ts"() {
    "use strict";
    init_Utilities();
    init_SkeletonType();
    init_RigConfig();
    WeightCalculator = class {
      constructor(bones, geometry, skeleton_type) {
        this.cached_median_child_bone_positions = [];
        this.bone_object_to_index = /* @__PURE__ */ new Map();
        this.distance_to_bottom_of_position_tracking_bone = 0;
        // height of the crotch: below it, vertices belong to the legs, not the hips
        this.hips_bottom_y = -Infinity;
        // each index will be a bone index. the value will be a list of vertex indices that belong to that bone
        this.bones_vertex_segmentation = [];
        // bone indices that should never receive vertex weights: the root (global
        // transform only) and leaf/orientation bones (finger/toe/tail tips, etc.)
        this.skipped_bone_indices = /* @__PURE__ */ new Set();
        // afk.ai: fingers and toes are short, so their midpoints sit close to whatever the hand or foot
        // rests against (a hand hanging beside the thigh, fingertips by the knee) while a long thigh's
        // midpoint is far away. These bones only claim vertices near their own segment
        this.digit_segments = /* @__PURE__ */ new Map();
        this.bones = bones;
        this.geometry = geometry;
        this.skeleton_type = skeleton_type;
      }
      /**
       * Pre-computes cached values needed for weight calculations.
       * Must be called before calculate_median_bone_weights.
       */
      initialize_caches() {
        this.cached_median_child_bone_positions = this.bones.map((b) => Utility.bone_midpoint_to_child(b));
        this.bones.forEach((b, idx) => this.bone_object_to_index.set(b, idx));
        this.bones.forEach((b, idx) => {
          if (b.name === "root" || Utility.is_leaf_bone(b)) {
            this.skipped_bone_indices.add(idx);
          }
        });
        this.bones.forEach((b, idx) => {
          if (!/thumb|index|middle|ring|pinky|finger|toe/i.test(b.name) || b.children.length === 0) return;
          const head = Utility.world_position_from_object(b);
          const tail = Utility.world_position_from_object(b.children[0]);
          this.digit_segments.set(idx, { head, tail, reach: head.distanceTo(tail) });
        });
        this.distance_to_bottom_of_position_tracking_bone = this.calculate_distance_to_bottom_of_position_tracking_bone();
        this.hips_bottom_y = this.calculate_hips_bottom_y();
      }
      // afk.ai: the hip check used to compare this distance with each vertex's absolute height,
      // which skipped the pelvis for every vertex more than a hand's width above the ground, so
      // the hips ended up on spine_01. Turn the distance into the height it measures down to.
      calculate_hips_bottom_y() {
        const position_tracking_bone_name = RigConfig.by_skeleton_type(this.skeleton_type)?.position_tracking_bone_name ?? "";
        const index = this.bones.findIndex((b) => b.name.toLowerCase().includes(position_tracking_bone_name.toLowerCase()));
        if (index < 0) return -Infinity;
        return this.cached_median_child_bone_positions[index].y - this.distance_to_bottom_of_position_tracking_bone;
      }
      get_cached_median_child_bone_positions() {
        return this.cached_median_child_bone_positions;
      }
      /**
       * Assigns the closest bone to each vertex.
       * Modifies the skin_indices and skin_weights arrays in place.
       */
      calculate_median_bone_weights(skin_indices, skin_weights) {
        const vertex_count = this.geometry.attributes.position.array.length / 3;
        for (let i = 0; i < vertex_count; i++) {
          const vertex_position = new Vector39().fromBufferAttribute(this.geometry.attributes.position, i);
          let closest_bone_distance = 1e3;
          let closest_bone_index = 0;
          this.bones.forEach((bone, idx) => {
            if (this.skipped_bone_indices.has(idx)) {
              return;
            }
            if (this.skeleton_type === "human" /* Human */ && (bone.name.includes("hips") || bone.name.includes("pelvis"))) {
              if (vertex_position.y < this.hips_bottom_y) {
                return;
              }
            }
            const digit = this.digit_segments.get(idx);
            if (digit !== void 0 && distance_to_segment(vertex_position, digit.head, digit.tail) > digit.reach) return;
            const distance = this.cached_median_child_bone_positions[idx].distanceTo(vertex_position);
            if (distance < closest_bone_distance) {
              closest_bone_distance = distance;
              closest_bone_index = idx;
            }
          });
          this.bones_vertex_segmentation[closest_bone_index] ??= [];
          this.bones_vertex_segmentation[closest_bone_index].push(i);
          skin_indices.push(closest_bone_index, 0, 0, 0);
          skin_weights.push(1, 0, 0, 0);
        }
      }
      // every vertex checks to see if it is below the hips area,
      // so do this calculation once and cache it for the lookup later
      calculate_distance_to_bottom_of_position_tracking_bone() {
        const position_tracking_bone_name = RigConfig.by_skeleton_type(this.skeleton_type)?.position_tracking_bone_name || "UNKNOWN POSITION BONE";
        let position_tracking_bone_object = this.bones.find((b) => {
          const name = b.name.toLowerCase();
          return name.includes(position_tracking_bone_name.toLowerCase());
        });
        if (position_tracking_bone_object === void 0) {
          throw new Error("Position tracking bone not found");
        }
        const intesection_point = this.cast_intersection_ray_down_from_bone(position_tracking_bone_object);
        const bone_index = this.bones.findIndex((b) => b === position_tracking_bone_object);
        const bone_position = this.cached_median_child_bone_positions[bone_index];
        let distance_to_bottom = intesection_point?.distanceTo(bone_position) ?? 0;
        distance_to_bottom *= 1.1;
        return distance_to_bottom;
      }
      cast_intersection_ray_down_from_bone(bone) {
        const raycaster = new Raycaster2();
        const bone_index = this.bones.findIndex((b) => b === bone);
        const bone_position = this.cached_median_child_bone_positions[bone_index];
        raycaster.set(bone_position, new Vector39(0, -1, 0));
        const temp_mesh = new Mesh2(this.geometry, new MeshBasicMaterial());
        temp_mesh.material.side = DoubleSide;
        const recursive_check_child_objects = false;
        const intersections = raycaster.intersectObject(temp_mesh, recursive_check_child_objects);
        if (intersections.length > 0) {
          return intersections[0].point;
        }
        return null;
      }
    };
  }
});

// ../../rigger/src/lib/solvers/BoneClassifier.ts
var BoneClassifier;
var init_BoneClassifier = __esm({
  "../../rigger/src/lib/solvers/BoneClassifier.ts"() {
    "use strict";
    BoneClassifier = class {
      constructor(bones) {
        this.bone_categories = /* @__PURE__ */ new Map();
        this.classify_all_bones(bones);
      }
      get_category(bone_index) {
        return this.bone_categories.get(bone_index) ?? "other" /* Other */;
      }
      /**
       * Returns true if the bone pair represents a parent-child relationship
       * where smoothing should only flow toward the child direction.
       * This prevents elbow movement from deforming the bicep.
       */
      is_limb_boundary(bone_index_a, bone_index_b) {
        const cat_a = this.get_category(bone_index_a);
        const cat_b = this.get_category(bone_index_b);
        return cat_a === "limb" /* Limb */ || cat_b === "limb" /* Limb */;
      }
      /**
       * Returns true if the boundary is between two extremity bones
       * (hand↔finger, finger↔finger, foot↔toe). These get no smoothing so
       * small parts like fingers stay rigid instead of turning mushy.
       * Requires both sides to be extremities, so the wrist/ankle
       * (limb↔extremity) is not caught here and keeps its limb smoothing.
       */
      is_extremity_boundary(bone_index_a, bone_index_b) {
        return this.get_category(bone_index_a) === "extremity" /* Extremity */ && this.get_category(bone_index_b) === "extremity" /* Extremity */;
      }
      /**
       * Returns true if the boundary between two bones should get
       * wider multi-ring smoothing (torso regions).
       */
      is_torso_boundary(bone_index_a, bone_index_b) {
        const cat_a = this.get_category(bone_index_a);
        const cat_b = this.get_category(bone_index_b);
        return (cat_a === "torso" /* Torso */ || cat_b === "torso" /* Torso */) && cat_a !== "extremity" /* Extremity */ && cat_b !== "extremity" /* Extremity */;
      }
      classify_all_bones(bones) {
        bones.forEach((bone, idx) => {
          const category = this.classify_bone(bone);
          this.bone_categories.set(idx, category);
        });
      }
      classify_bone(bone) {
        const name = bone.name.toLowerCase();
        const extremity_keywords = [
          "hand",
          "foot",
          "feet",
          "toe",
          "ball",
          "thumb",
          "index",
          "middle",
          "ring",
          "pinky",
          "finger",
          "teeth",
          "eye",
          "tongue",
          "wing",
          "feather",
          "leaf",
          "ear",
          "horn"
        ];
        if (extremity_keywords.some((kw) => name.includes(kw))) {
          return "extremity" /* Extremity */;
        }
        const limb_keywords = [
          "arm",
          "upperarm",
          "lowerarm",
          "forearm",
          "elbow",
          "wrist",
          "nose",
          "shoulder",
          "clavicle",
          "ankle",
          "fin",
          "head",
          "chin",
          "jaw",
          "mouth",
          "thigh",
          "calf",
          "shin",
          "knee",
          "leg",
          "upleg",
          "lowleg",
          "neck",
          "humerus"
        ];
        if (limb_keywords.some((kw) => name.includes(kw))) {
          return "limb" /* Limb */;
        }
        const torso_keywords = [
          "spine",
          "chest",
          "hips",
          "pelvis",
          "torso",
          "abdomen",
          "body",
          "tail",
          "stomach",
          "collar",
          "scapula",
          "ribcage"
        ];
        if (torso_keywords.some((kw) => name.includes(kw))) {
          return "torso" /* Torso */;
        }
        const parent_bone = bone.parent;
        if (parent_bone?.isBone !== true) {
          return "root" /* Root */;
        }
        return "other" /* Other */;
      }
    };
  }
});

// ../../rigger/src/lib/solvers/ExtremityWeightCorrector.ts
import {
  Vector3 as Vector310
} from "three";
var ExtremityWeightCorrector;
var init_ExtremityWeightCorrector = __esm({
  "../../rigger/src/lib/solvers/ExtremityWeightCorrector.ts"() {
    "use strict";
    init_Utilities();
    init_BoneClassifier();
    ExtremityWeightCorrector = class {
      constructor(geometry, bones) {
        this.bone_to_index = /* @__PURE__ */ new Map();
        this.geometry = geometry;
        this.bones = bones;
        this.classifier = new BoneClassifier(bones);
        bones.forEach((bone, idx) => this.bone_to_index.set(bone, idx));
      }
      /**
       * Walks every vertex assigned to an extremity bone and reassigns it to the
       * bone's parent when it sits behind the bone's start joint.
       * Modifies skin_indices in place. Runs before smoothing so the corrected
       * assignments are what the smoother sees.
       */
      apply_extremity_weight_correction(skin_indices, skin_weights) {
        const vertex_count = this.geometry.attributes.position.array.length / 3;
        const bone_axes = this.build_extremity_bone_axes();
        for (let i = 0; i < vertex_count; i++) {
          const offset = i * 4;
          const bone_index = skin_indices[offset];
          const axis = bone_axes.get(bone_index);
          if (axis === void 0) continue;
          const vertex_position = new Vector310().fromBufferAttribute(this.geometry.attributes.position, i);
          const to_vertex = vertex_position.sub(axis.head);
          if (to_vertex.dot(axis.direction) < 0) {
            skin_indices[offset] = axis.parent_index;
          }
        }
      }
      /**
       * Builds, for each extremity bone that has a parent bone in our list, the
       * start-joint position, the axis pointing toward its child, and the parent
       * bone index. Leaf extremity bones (no child) fall back to the direction
       * coming from the parent joint.
       */
      build_extremity_bone_axes() {
        const axes = /* @__PURE__ */ new Map();
        this.bones.forEach((bone, idx) => {
          if (this.classifier.get_category(idx) !== "extremity" /* Extremity */) return;
          const parent = bone.parent;
          if (parent === null) return;
          const parent_index = this.bone_to_index.get(parent);
          if (parent_index === void 0) return;
          const head = Utility.world_position_from_object(bone);
          let direction;
          if (bone.children.length > 0) {
            const child_head = Utility.world_position_from_object(bone.children[0]);
            direction = Utility.direction_between_points(head, child_head);
          } else {
            const parent_head = Utility.world_position_from_object(parent);
            direction = Utility.direction_between_points(parent_head, head);
          }
          axes.set(idx, { head, direction, parent_index });
        });
        return axes;
      }
    };
  }
});

// ../../rigger/src/lib/solvers/WeightSmoother.ts
var WeightSmoother;
var init_WeightSmoother = __esm({
  "../../rigger/src/lib/solvers/WeightSmoother.ts"() {
    "use strict";
    init_BoneClassifier();
    WeightSmoother = class {
      constructor(geometry, bones) {
        this.geometry = geometry;
        this.bones = bones;
        this.classifier = new BoneClassifier(bones);
      }
      geometry_vertex_count() {
        return this.geometry.attributes.position.array.length / 3;
      }
      /**
       * Smooths skin weights at bone boundaries with category-aware behavior.
       * - Torso boundaries get multi-ring gradient smoothing (3 rings, tapering weights)
       * - Limb boundaries get directional child-only smoothing
       * - Other boundaries get standard single-ring 50/50 blending
       */
      smooth_bone_weight_boundaries(skin_indices, skin_weights) {
        const adjacency = this.build_vertex_adjacency();
        const position_to_indices = this.build_position_map();
        const boundary_pairs = this.find_boundary_pairs(skin_indices, skin_weights, adjacency);
        this.apply_torso_smoothing(skin_indices, skin_weights, adjacency, position_to_indices, boundary_pairs);
        this.apply_limb_smoothing(skin_indices, skin_weights, position_to_indices, boundary_pairs);
        this.apply_standard_smoothing(skin_indices, skin_weights, position_to_indices, boundary_pairs);
        this.apply_extremity_smoothing(boundary_pairs);
      }
      /**
       * A boundary pair tracks two adjacent vertices assigned to different bones.
       */
      find_boundary_pairs(skin_indices, skin_weights, adjacency) {
        const vertex_count = this.geometry_vertex_count();
        const visited = /* @__PURE__ */ new Set();
        const pairs = [];
        for (let i = 0; i < vertex_count; i++) {
          const offset_a = i * 4;
          const bone_a = skin_indices[offset_a];
          const weight_a = skin_weights[offset_a];
          if (weight_a !== 1) continue;
          for (const j of adjacency[i]) {
            const offset_b = j * 4;
            const bone_b = skin_indices[offset_b];
            const weight_b = skin_weights[offset_b];
            if (bone_a === bone_b || weight_b !== 1) continue;
            const key = i < j ? `${i},${j}` : `${j},${i}`;
            if (visited.has(key)) continue;
            visited.add(key);
            let smoothing_type = "standard" /* Standard */;
            if (this.classifier.is_torso_boundary(bone_a, bone_b)) {
              smoothing_type = "torso" /* Torso */;
            } else if (this.classifier.is_limb_boundary(bone_a, bone_b)) {
              smoothing_type = "limb" /* Limb */;
            } else if (this.classifier.is_extremity_boundary(bone_a, bone_b)) {
              smoothing_type = "extremity" /* Extremity */;
            }
            pairs.push({ vertex_a: i, vertex_b: j, bone_a, bone_b, smoothing_type });
          }
        }
        return pairs;
      }
      /**
       * Torso smoothing: expands the blend region outward from the boundary
       * by multiple rings, applying tapering weight gradients.
       * This creates a wider, more natural transition for voluminous areas.
       */
      apply_torso_smoothing(skin_indices, skin_weights, adjacency, position_to_indices, pairs) {
        const torso_pairs = pairs.filter((p) => p.smoothing_type === "torso" /* Torso */);
        if (torso_pairs.length === 0) return;
        const boundary_vertices = /* @__PURE__ */ new Set();
        for (const pair of torso_pairs) {
          boundary_vertices.add(pair.vertex_a);
          boundary_vertices.add(pair.vertex_b);
        }
        const ring_weights = [0.5, 0.25, 0.1];
        const processed = /* @__PURE__ */ new Set();
        let current_ring_vertices = /* @__PURE__ */ new Set();
        for (const pair of torso_pairs) {
          this.blend_vertex_pair(
            skin_indices,
            skin_weights,
            position_to_indices,
            pair.vertex_a,
            pair.vertex_b,
            pair.bone_a,
            pair.bone_b,
            ring_weights[0]
          );
          processed.add(pair.vertex_a);
          processed.add(pair.vertex_b);
          current_ring_vertices.add(pair.vertex_a);
          current_ring_vertices.add(pair.vertex_b);
        }
        for (let ring = 1; ring < ring_weights.length; ring++) {
          const next_ring_vertices = /* @__PURE__ */ new Set();
          const secondary_weight = ring_weights[ring];
          for (const vertex_idx of current_ring_vertices) {
            const offset = vertex_idx * 4;
            const primary_bone = skin_indices[offset];
            for (const neighbor of adjacency[vertex_idx]) {
              if (processed.has(neighbor)) continue;
              const neighbor_offset = neighbor * 4;
              const neighbor_bone = skin_indices[neighbor_offset];
              if (neighbor_bone !== primary_bone) continue;
              if (skin_weights[neighbor_offset] !== 1) continue;
              const other_bone = this.find_neighbor_bone_from_boundary(vertex_idx, skin_indices, primary_bone);
              if (other_bone === -1) continue;
              const shared = this.get_shared_vertices(neighbor, position_to_indices);
              for (const idx of shared) {
                const off = idx * 4;
                skin_indices[off + 0] = neighbor_bone;
                skin_indices[off + 1] = other_bone;
                skin_weights[off + 0] = 1 - secondary_weight;
                skin_weights[off + 1] = secondary_weight;
                skin_indices[off + 2] = 0;
                skin_indices[off + 3] = 0;
                skin_weights[off + 2] = 0;
                skin_weights[off + 3] = 0;
              }
              processed.add(neighbor);
              next_ring_vertices.add(neighbor);
            }
          }
          current_ring_vertices = next_ring_vertices;
        }
      }
      /**
       * Limb smoothing: only blends in the direction of the child bone.
       * When bone A is the parent of bone B, only vertices on the B side
       * get blended. This prevents elbow movement from deforming the bicep.
       */
      apply_limb_smoothing(skin_indices, skin_weights, position_to_indices, pairs) {
        const limb_pairs = pairs.filter((p) => p.smoothing_type === "limb" /* Limb */);
        for (const pair of limb_pairs) {
          const a_is_parent = this.is_parent_of(pair.bone_a, pair.bone_b);
          const b_is_parent = this.is_parent_of(pair.bone_b, pair.bone_a);
          if (a_is_parent) {
            this.blend_single_side(
              skin_indices,
              skin_weights,
              position_to_indices,
              pair.vertex_b,
              pair.bone_b,
              pair.bone_a,
              0.5
            );
          } else if (b_is_parent) {
            this.blend_single_side(
              skin_indices,
              skin_weights,
              position_to_indices,
              pair.vertex_a,
              pair.bone_a,
              pair.bone_b,
              0.5
            );
          } else {
            this.blend_vertex_pair(
              skin_indices,
              skin_weights,
              position_to_indices,
              pair.vertex_a,
              pair.vertex_b,
              pair.bone_a,
              pair.bone_b,
              0.5
            );
          }
        }
      }
      /**
       * Extremity smoothing: intentionally does nothing. Hands, fingers, feet, and
       * toes stay 100% rigid to their assigned bone — any blend smears across the
       * small part and looks mushy. Kept as an explicit pass so the intent is clear
       * and so these boundaries aren't accidentally handled elsewhere.
       */
      apply_extremity_smoothing(pairs) {
        void pairs;
      }
      /**
       * Standard smoothing: simple 50/50 blend at boundaries (original behavior).
       */
      apply_standard_smoothing(skin_indices, skin_weights, position_to_indices, pairs) {
        const standard_pairs = pairs.filter((p) => p.smoothing_type === "standard" /* Standard */);
        for (const pair of standard_pairs) {
          this.blend_vertex_pair(
            skin_indices,
            skin_weights,
            position_to_indices,
            pair.vertex_a,
            pair.vertex_b,
            pair.bone_a,
            pair.bone_b,
            0.5
          );
        }
      }
      /**
       * Blends both vertices of a boundary pair symmetrically.
       * secondary_weight is how much influence the "other" bone gets (e.g., 0.5 = 50/50).
       */
      blend_vertex_pair(skin_indices, skin_weights, position_to_indices, vertex_a, vertex_b, bone_a, bone_b, secondary_weight) {
        const primary_weight = 1 - secondary_weight;
        const shared_a = this.get_shared_vertices(vertex_a, position_to_indices);
        for (const idx of shared_a) {
          const off = idx * 4;
          skin_indices[off + 0] = bone_a;
          skin_indices[off + 1] = bone_b;
          skin_weights[off + 0] = primary_weight;
          skin_weights[off + 1] = secondary_weight;
          skin_indices[off + 2] = 0;
          skin_indices[off + 3] = 0;
          skin_weights[off + 2] = 0;
          skin_weights[off + 3] = 0;
        }
        const shared_b = this.get_shared_vertices(vertex_b, position_to_indices);
        for (const idx of shared_b) {
          const off = idx * 4;
          skin_indices[off + 0] = bone_b;
          skin_indices[off + 1] = bone_a;
          skin_weights[off + 0] = primary_weight;
          skin_weights[off + 1] = secondary_weight;
          skin_indices[off + 2] = 0;
          skin_indices[off + 3] = 0;
          skin_weights[off + 2] = 0;
          skin_weights[off + 3] = 0;
        }
      }
      /**
       * Blends only one side of a boundary — used for directional limb smoothing.
       * The vertex gets a blend, but its counterpart on the other side stays rigid.
       */
      blend_single_side(skin_indices, skin_weights, position_to_indices, vertex, primary_bone, secondary_bone, secondary_weight) {
        const primary_weight = 1 - secondary_weight;
        const shared = this.get_shared_vertices(vertex, position_to_indices);
        for (const idx of shared) {
          const off = idx * 4;
          skin_indices[off + 0] = primary_bone;
          skin_indices[off + 1] = secondary_bone;
          skin_weights[off + 0] = primary_weight;
          skin_weights[off + 1] = secondary_weight;
          skin_indices[off + 2] = 0;
          skin_indices[off + 3] = 0;
          skin_weights[off + 2] = 0;
          skin_weights[off + 3] = 0;
        }
      }
      /**
       * Checks if bone at index_a is a direct parent of bone at index_b
       * by walking up the bone hierarchy.
       */
      is_parent_of(parent_index, child_index) {
        const parent_bone = this.bones[parent_index];
        const child_bone = this.bones[child_index];
        if (parent_bone === void 0 || child_bone === void 0) return false;
        return child_bone.parent === parent_bone;
      }
      /**
       * Finds the secondary bone index from a vertex that was already blended,
       * used when expanding torso rings outward.
       */
      find_neighbor_bone_from_boundary(vertex_idx, skin_indices, primary_bone) {
        const offset = vertex_idx * 4;
        const secondary_bone = skin_indices[offset + 1];
        if (secondary_bone !== primary_bone && secondary_bone !== 0) {
          return secondary_bone;
        }
        return -1;
      }
      get_shared_vertices(vertex, position_to_indices) {
        const pos = this.geometry.attributes.position;
        const x = pos.getX(vertex);
        const y = pos.getY(vertex);
        const z2 = pos.getZ(vertex);
        const key = `${x.toFixed(6)},${y.toFixed(6)},${z2.toFixed(6)}`;
        return position_to_indices.get(key) || [vertex];
      }
      build_position_map() {
        const vertex_count = this.geometry_vertex_count();
        const position_to_indices = /* @__PURE__ */ new Map();
        for (let i = 0; i < vertex_count; i++) {
          const pos = this.geometry.attributes.position;
          const x = pos.getX(i);
          const y = pos.getY(i);
          const z2 = pos.getZ(i);
          const key = `${x.toFixed(6)},${y.toFixed(6)},${z2.toFixed(6)}`;
          if (!position_to_indices.has(key)) position_to_indices.set(key, []);
          position_to_indices.get(key).push(i);
        }
        return position_to_indices;
      }
      /**
       * Builds a spatial adjacency map for the mesh vertices using geometry's index (faces).
       * Returns an array of Sets, where each Set contains the indices of neighboring vertices.
       */
      build_vertex_adjacency() {
        const vertex_count = this.geometry_vertex_count();
        const adjacency = Array.from({ length: vertex_count }, () => /* @__PURE__ */ new Set());
        const index_attribute = this.geometry.index;
        if (index_attribute === null) return adjacency;
        const indices = index_attribute.array;
        for (let i = 0; i < indices.length; i += 3) {
          const a = indices[i];
          const b = indices[i + 1];
          const c = indices[i + 2];
          adjacency[a].add(b);
          adjacency[a].add(c);
          adjacency[b].add(a);
          adjacency[b].add(c);
          adjacency[c].add(a);
          adjacency[c].add(b);
        }
        return adjacency;
      }
    };
  }
});

// ../../rigger/src/lib/solvers/WeightNormalizer.ts
var WeightNormalizer;
var init_WeightNormalizer = __esm({
  "../../rigger/src/lib/solvers/WeightNormalizer.ts"() {
    "use strict";
    WeightNormalizer = class {
      constructor(geometry) {
        this.geometry = geometry;
      }
      geometry_vertex_count() {
        return this.geometry.attributes.position.array.length / 3;
      }
      /**
       * Returns an array of vertex indices whose weights do not sum to 1.0 (within a small epsilon).
       */
      find_vertices_with_incorrect_weight_sum(skin_weights) {
        const epsilon = 1e-4;
        const incorrect_vertices = [];
        const vertex_count = this.geometry_vertex_count();
        for (let i = 0; i < vertex_count; i++) {
          const offset = i * 4;
          const sum = skin_weights[offset] + skin_weights[offset + 1] + skin_weights[offset + 2] + skin_weights[offset + 3];
          if (Math.abs(sum - 1) > epsilon) {
            incorrect_vertices.push(i);
          }
        }
        return incorrect_vertices;
      }
      /**
       * Normalizes weights for vertices that don't sum to 1.0.
       * Distributes the remaining weight across non-zero influence slots.
       */
      normalize_weights(all_skin_weights) {
        const vertices_that_do_not_have_influences_adding_to_one = this.find_vertices_with_incorrect_weight_sum(all_skin_weights);
        for (const vertex_index of vertices_that_do_not_have_influences_adding_to_one) {
          const offset = vertex_index * 4;
          const weights = [
            all_skin_weights[offset],
            all_skin_weights[offset + 1],
            all_skin_weights[offset + 2],
            all_skin_weights[offset + 3]
          ];
          const weight_sum = weights.reduce((a, b) => a + b, 0);
          const weight_per_index = (1 - weight_sum) / 3;
          console.log(weight_per_index);
          for (let i = 0; i < 4; i++) {
            if (weights[i] !== 0) {
              all_skin_weights[offset + i] += weight_per_index;
            }
          }
        }
      }
    };
  }
});

// ../../rigger/src/lib/solvers/SkinningAlgorithm.ts
import {
  BufferGeometry as BufferGeometry2
} from "three";
var SkinningAlgorithm;
var init_SkinningAlgorithm = __esm({
  "../../rigger/src/lib/solvers/SkinningAlgorithm.ts"() {
    "use strict";
    init_Utilities();
    init_HeadWeightCorrector();
    init_ArmWeightCorrector();
    init_WeightCalculator();
    init_ExtremityWeightCorrector();
    init_WeightSmoother();
    init_WeightNormalizer();
    SkinningAlgorithm = class {
      constructor(bone_hier, skeleton_type) {
        this.bones_master_data = [];
        this.geometry = new BufferGeometry2();
        this.skeleton_type = null;
        // Head weight correction properties
        this.use_head_weight_correction = false;
        this.preview_plane_height = 1.4;
        // Arm plane correction properties. The offset is relative to the shoulder
        // joint's X, which the corrector reads off the bones itself.
        this.use_arm_plane_correction = false;
        this.arm_plane_offset = 0;
        this.skeleton_type = skeleton_type;
        this.bones_master_data = Utility.bone_list_from_hierarchy(bone_hier);
      }
      set_geometry(geom) {
        this.geometry = geom;
      }
      set_head_weight_correction_enabled(enabled) {
        this.use_head_weight_correction = enabled;
      }
      set_preview_plane_height(height) {
        this.preview_plane_height = height;
      }
      set_arm_plane_correction_enabled(enabled) {
        this.use_arm_plane_correction = enabled;
      }
      set_arm_plane_offset(offset) {
        this.arm_plane_offset = offset;
      }
      calculate_indexes_and_weights() {
        const skin_indices = [];
        const skin_weights = [];
        const weight_calculator = new WeightCalculator(this.bones_master_data, this.geometry, this.skeleton_type);
        weight_calculator.initialize_caches();
        console.time("calculate_closest_bone_weights");
        weight_calculator.calculate_median_bone_weights(skin_indices, skin_weights);
        const extremity_corrector = new ExtremityWeightCorrector(this.geometry, this.bones_master_data);
        extremity_corrector.apply_extremity_weight_correction(skin_indices, skin_weights);
        if (this.use_arm_plane_correction) {
          const arm_weight_corrector = new ArmWeightCorrector(
            this.geometry,
            this.bones_master_data,
            this.arm_plane_offset
          );
          arm_weight_corrector.apply_arm_weight_correction(skin_indices, skin_weights);
        }
        const weight_smoother = new WeightSmoother(this.geometry, this.bones_master_data);
        weight_smoother.smooth_bone_weight_boundaries(skin_indices, skin_weights);
        console.timeEnd("calculate_closest_bone_weights");
        const weight_normalizer = new WeightNormalizer(this.geometry);
        weight_normalizer.normalize_weights(skin_weights);
        if (this.use_head_weight_correction) {
          const head_weight_corrector = new HeadWeightCorrector(
            this.geometry,
            this.bones_master_data,
            this.preview_plane_height
          );
          console.log("applying the head weight correction...");
          head_weight_corrector.apply_head_weight_correction(skin_indices, skin_weights);
        }
        console.log("do we have any leftover incorrect weights ", weight_normalizer.find_vertices_with_incorrect_weight_sum(skin_weights));
        return [skin_indices, skin_weights];
      }
    };
  }
});

// src/rigger.ts
var init_rigger = __esm({
  "src/rigger.ts"() {
    "use strict";
    init_SkeletonType();
    init_RigConfig();
    init_HandHelper();
    init_PointCloud();
    init_HumanoidFit();
    init_CreatureFit();
    init_SkinningAlgorithm();
    init_Utilities();
  }
});

// src/skeleton.ts
import { Bone as Bone3, Object3D, Quaternion as Quaternion3, Vector3 as Vector311 } from "three";
function skeleton_types() {
  return RigConfig.all.map((entry) => entry.skeleton_type);
}
function parse_skeleton(name) {
  const type = skeleton_types().find((t) => t === name.toLowerCase().trim());
  if (type === void 0) {
    throw new Error(`Unknown skeleton "${name}". Choose one of: ${skeleton_types().join(", ")}`);
  }
  return type;
}
async function load_template(type, hands = "all-fingers") {
  const key = `${type}:${hands}`;
  let cached = template_cache.get(key);
  if (cached === void 0) {
    cached = read_template(type, hands);
    template_cache.set(key, cached);
  }
  return await cached;
}
async function read_template(type, hands) {
  const entry = RigConfig.by_skeleton_type(type);
  if (entry === void 0) throw new Error(`No rig for skeleton ${type}`);
  const io = await get_io();
  const doc = await io.read(asset_path(entry.rig_file));
  const root_doc = doc.getRoot();
  const joint_nodes = new Set(root_doc.listSkins().flatMap((skin) => skin.listJoints()));
  const scene = root_doc.getDefaultScene() ?? root_doc.listScenes()[0];
  const holder = new Object3D();
  const build = (node, parent) => {
    const object = joint_nodes.has(node) ? new Bone3() : new Object3D();
    object.name = node.getName();
    object.position.fromArray(node.getTranslation());
    object.quaternion.fromArray(node.getRotation());
    object.scale.fromArray(node.getScale());
    parent.add(object);
    for (const child of node.listChildren()) build(child, object);
  };
  for (const node of scene.listChildren()) build(node, holder);
  const armature = holder.children[0];
  armature.removeFromParent();
  if (type === "human" /* Human */ && hands !== "all-fingers") {
    new HandHelper().modify_hand_skeleton(armature, hands);
  }
  armature.updateMatrixWorld(true);
  const root = armature.children.find((c) => c.isBone === true);
  if (root === void 0) throw new Error(`Rig for ${type} has no root bone`);
  const bones = Utility.bone_list_from_hierarchy(root);
  const positions = /* @__PURE__ */ new Map();
  const parents = /* @__PURE__ */ new Map();
  for (const bone of bones) {
    positions.set(bone.name, bone.getWorldPosition(new Vector311()));
    const parent = bone.parent;
    parents.set(bone.name, parent?.isBone === true ? parent.name : void 0);
  }
  return { type, hands, armature, root, bones, positions, parents, tracking_bone: entry.position_tracking_bone_name };
}
async function describe_skeletons() {
  return await Promise.all(RigConfig.all.map(async (entry) => ({
    name: entry.skeleton_type,
    description: DESCRIPTIONS[entry.skeleton_type] ?? entry.rig_display_name,
    bones: (await load_template(entry.skeleton_type)).bones.length
  })));
}
function is_limb_bone(name) {
  return /clavicle|shoulder|upperarm|lowerarm|forearm|arm|hand|thumb|index|middle|ring|pinky|finger|thigh|calf|shin|knee|foot|ball|toe|ankle|leg|wing|paw|elbow/i.test(name);
}
function build_rig(template, joints, rest3 = "limbs") {
  const armature = template.armature.clone(true);
  armature.updateMatrixWorld(true);
  const by_name = /* @__PURE__ */ new Map();
  armature.traverse((o) => {
    if (o.isBone === true) by_name.set(o.name, o);
  });
  const ordered = [...by_name.values()].sort((a, b) => depth2(a) - depth2(b));
  const target = (bone) => joints.get(bone.name) ?? template.positions.get(bone.name);
  if (rest3 === "template") {
    for (const bone of ordered) {
      const parent = bone.parent;
      parent.updateWorldMatrix(true, false);
      bone.position.copy(parent.worldToLocal(target(bone).clone()));
      bone.updateWorldMatrix(false, true);
    }
  } else {
    const template_world = /* @__PURE__ */ new Map();
    template.armature.updateMatrixWorld(true);
    template.armature.traverse((o) => {
      if (o.isBone === true) template_world.set(o.name, o.getWorldQuaternion(new Quaternion3()));
    });
    const swing = /* @__PURE__ */ new Map();
    const world_rotation = /* @__PURE__ */ new Map();
    const template_local = /* @__PURE__ */ new Map();
    template.armature.traverse((o) => {
      if (o.isBone === true) template_local.set(o.name, o.quaternion.clone());
    });
    for (const bone of ordered) {
      const parent_bone = bone.parent.isBone === true ? bone.parent : null;
      const align = parent_bone !== null && (rest3 === "aligned" || is_limb_bone(bone.name));
      if (!align) {
        const parent_world = parent_bone !== null ? world_rotation.get(parent_bone.name) : bone.parent.getWorldQuaternion(new Quaternion3());
        const world = parent_world.clone().multiply(template_local.get(bone.name));
        world_rotation.set(bone.name, world);
        swing.set(bone.name, world.clone().multiply(template_world.get(bone.name).clone().invert()));
        continue;
      }
      let d = parent_bone !== null ? (swing.get(parent_bone.name) ?? new Quaternion3()).clone() : new Quaternion3();
      const child = parent_bone === null ? void 0 : primary_child(template, bone.name);
      if (child !== void 0 && joints.has(bone.name) && joints.has(child)) {
        const from = template.positions.get(child).clone().sub(template.positions.get(bone.name));
        const to = joints.get(child).clone().sub(joints.get(bone.name));
        if (from.lengthSq() > 1e-12 && to.lengthSq() > 1e-12) {
          d = new Quaternion3().setFromUnitVectors(from.normalize(), to.normalize());
        }
      }
      swing.set(bone.name, d);
      world_rotation.set(bone.name, d.clone().multiply(template_world.get(bone.name)));
    }
    for (const bone of ordered) {
      const parent = bone.parent;
      const parent_rotation = parent.isBone === true ? world_rotation.get(parent.name) : parent.getWorldQuaternion(new Quaternion3());
      const parent_position = parent.isBone === true ? target(parent) : parent.getWorldPosition(new Vector311());
      const inverse_parent = parent_rotation.clone().invert();
      bone.quaternion.copy(inverse_parent.clone().multiply(world_rotation.get(bone.name)));
      bone.position.copy(target(bone).clone().sub(parent_position).applyQuaternion(inverse_parent));
      bone.scale.set(1, 1, 1);
    }
    armature.updateMatrixWorld(true);
  }
  const root = by_name.get(template.root.name);
  const bones = template.bones.map((b) => by_name.get(b.name));
  return { armature, root, bones, by_name };
}
function primary_child(template, bone_name) {
  let best;
  let best_cos = 0.8;
  for (const [child, parent] of template.parents) {
    if (parent !== bone_name) continue;
    const child_bone = template.bones.find((b) => b.name === child);
    if (child_bone === void 0) continue;
    const offset = child_bone.position;
    const length = offset.length();
    if (length < 1e-9) continue;
    const cos = offset.y / length;
    if (cos > best_cos) {
      best_cos = cos;
      best = child;
    }
  }
  return best;
}
function depth2(object) {
  let d = 0;
  for (let p = object.parent; p !== null; p = p.parent) d++;
  return d;
}
function template_on_model(template, min, max) {
  const t_min = new Vector311(Infinity, Infinity, Infinity);
  const t_max = new Vector311(-Infinity, -Infinity, -Infinity);
  for (const p of template.positions.values()) {
    t_min.min(p);
    t_max.max(p);
  }
  const t_size = t_max.clone().sub(t_min);
  const m_size = max.clone().sub(min);
  const scale = Math.max(m_size.x, m_size.y, m_size.z) / Math.max(t_size.x, t_size.y, t_size.z, 1e-9);
  const t_center = new Vector311((t_min.x + t_max.x) / 2, t_min.y, (t_min.z + t_max.z) / 2);
  const m_center = new Vector311((min.x + max.x) / 2, min.y, (min.z + max.z) / 2);
  const out = /* @__PURE__ */ new Map();
  for (const [name, p] of template.positions) {
    out.set(name, p.clone().sub(t_center).multiplyScalar(scale).add(m_center));
  }
  return out;
}
var DESCRIPTIONS, HAND_OPTIONS, template_cache;
var init_skeleton = __esm({
  "src/skeleton.ts"() {
    "use strict";
    init_io();
    init_assets();
    init_rigger();
    DESCRIPTIONS = {
      human: "Humanoids and bipeds: people, robots, zombies, humanoid monsters, stylized characters. Includes fingers.",
      fox: "Small or medium four-legged animals with a tail: fox, dog, wolf, cat.",
      horse: "Long-legged four-legged animals: horse, deer, donkey, cow.",
      bird: "Birds with two legs and two wings.",
      dragon: "Four-legged dragons with wings and a tail.",
      kaiju: "Upright two-legged monsters with a tail: dinosaurs, lizard people, kaiju.",
      spider: "Eight-legged creatures: spiders, crabs, insects.",
      snake: "Legless bodies: snakes, worms, eels.",
      fish: "Fish, sharks and whales."
    };
    HAND_OPTIONS = ["all-fingers", "thumb-and-index", "simplified-hand", "single-bone"];
    template_cache = /* @__PURE__ */ new Map();
  }
});

// src/util.ts
function num(n) {
  if (!Number.isFinite(n)) return n;
  return Number(n.toPrecision(5));
}
function vec(v) {
  return [num(v.x), num(v.y), num(v.z)];
}
function is_minor_joint(name) {
  return /(thumb|index|middle|ring|pinky)_\d|leaf|tip/i.test(name);
}
var init_util = __esm({
  "src/util.ts"() {
    "use strict";
  }
});

// src/fit.ts
import { Vector3 as Vector312 } from "three";
function point_cloud(triangles) {
  let cloud = cloud_cache.get(triangles);
  if (cloud === void 0) {
    cloud = PointCloud.from_triangles(triangles);
    cloud_cache.set(triangles, cloud);
  }
  return cloud;
}
function auto_fit(triangles, min, max, template) {
  const notes = [];
  const cloud = point_cloud(triangles);
  if (cloud.count < 50 || cloud.height <= 0) {
    notes.push("The mesh is too small or flat to measure, so the template was scaled over it instead.");
    return { joints: template_on_model(template, min, max), notes };
  }
  const size = cloud.max.clone().sub(cloud.min);
  const upright = template.type === "human" /* Human */ || template.type === "kaiju" /* Kaiju */;
  const lying = upright && size.z > size.y * 1.4 && size.z >= size.x;
  if (lying) {
    notes.push(`The model is ${size.z.toPrecision(3)} long along Z but only ${size.y.toPrecision(3)} tall along Y, as if it lies on its back or was exported Z-up. If it should stand, rig_transform_model with rotate [-90, 0, 0] (or [90, 0, 0]) stands it up. If the file holds more than the character (a floor, a room, props), rig_meshes can leave those out first.`);
  }
  if (template.type === "human" /* Human */) {
    const chest = cloud.slab(cloud.min.y + 0.62 * cloud.height, cloud.min.y + 0.72 * cloud.height);
    let x0 = Infinity;
    let x1 = -Infinity;
    let z0 = Infinity;
    let z1 = -Infinity;
    for (const i of chest) {
      x0 = Math.min(x0, cloud.xs[i]);
      x1 = Math.max(x1, cloud.xs[i]);
      z0 = Math.min(z0, cloud.zs[i]);
      z1 = Math.max(z1, cloud.zs[i]);
    }
    if (!lying && chest.length > 20 && x1 - x0 < (z1 - z0) * 0.7) {
      notes.push(`At chest height the model is deeper along Z (${(z1 - z0).toPrecision(3)}) than wide along X (${(x1 - x0).toPrecision(3)}). The humanoid fit reads the shoulders along X and expects the character to face +Z, so a character turned sideways will fit badly. rig_transform_model with rotate [0, 90, 0] or [0, -90, 0] can turn it.`);
    }
    const toes = toe_direction(cloud);
    if (!lying && toes === "-Z") {
      notes.push("The feet stick out well behind the ankles, so the character probably faces -Z. Animations and the left/right joint names assume +Z. Confirm with the face in a LEFT render, then rig_transform_model with rotate [0, 180, 0] turns it around.");
    } else if (!lying && toes === "maybe -Z") {
      notes.push("The feet reach further behind the ankles than in front, which can mean the character faces -Z, but chunky boots and robot feet do this too. Only if the face is on the -Z side in a LEFT render, rig_transform_model with rotate [0, 180, 0] turns it around.");
    }
    const { positions, landmarks } = fit_humanoid(cloud, template.positions, template.parents);
    const found_nothing = landmarks.crotch_y === null && landmarks.neck_y === null && landmarks.arms.size === 0 && landmarks.arm_line_y === null;
    const low_arms = landmarks.arm_line_y !== null && landmarks.arm_line_y - landmarks.floor < 0.45 * landmarks.height;
    const wide = landmarks.torso_half_width > 0.3 * landmarks.height;
    if (!lying && (found_nothing || low_arms || wide)) {
      notes.push((found_nothing ? "The fit found no separate legs, no neck and no arms held out." : "The proportions don't look like a standing person" + (low_arms ? " (what reads as arms held out is below half the height)" : " (the body is very wide for its height)") + ".") + " If this isn't a standing humanoid (an object, an animal, a seated or curled-up pose), another skeleton or placing the joints by hand will work better.");
    }
    const joints2 = complete(positions, template);
    place_root(joints2, template, cloud.min.y);
    return {
      joints: joints2,
      notes,
      landmarks: {
        floor_y: num(landmarks.floor),
        top_y: num(landmarks.top),
        height: num(landmarks.height),
        center_x: num(landmarks.center_x),
        crotch_y: landmarks.crotch_y === null ? null : num(landmarks.crotch_y),
        neck_y: landmarks.neck_y === null ? null : num(landmarks.neck_y),
        t_pose_arm_line_y: landmarks.arm_line_y === null ? null : num(landmarks.arm_line_y),
        torso_half_width: num(landmarks.torso_half_width),
        toes_point: toes
      }
    };
  }
  const fitted = fit_creature(cloud, template.positions, template.type);
  if (fitted.size === 0) {
    notes.push("The model already matches the template's size and position, so the template joints were kept.");
    return { joints: new Map([...template.positions].map(([k, v]) => [k, v.clone()])), notes };
  }
  const joints = complete(fitted, template);
  place_root(joints, template, cloud.min.y);
  return { joints, notes };
}
function toe_direction(cloud) {
  const h = cloud.height;
  const center_x = (cloud.min.x + cloud.max.x) / 2;
  const sole = cloud.slab(cloud.min.y, cloud.min.y + 0.025 * h);
  const ankle = cloud.slab(cloud.min.y + 0.07 * h, cloud.min.y + 0.11 * h);
  const verdicts = [1, -1].map((side) => {
    const on_side = (i) => (cloud.xs[i] - center_x) * side > 0;
    const s = sole.filter(on_side);
    const a = ankle.filter(on_side);
    if (s.length < 6 || a.length < 6) return "unclear";
    let s0 = Infinity;
    let s1 = -Infinity;
    let a0 = Infinity;
    let a1 = -Infinity;
    for (const i of s) {
      s0 = Math.min(s0, cloud.zs[i]);
      s1 = Math.max(s1, cloud.zs[i]);
    }
    for (const i of a) {
      a0 = Math.min(a0, cloud.zs[i]);
      a1 = Math.max(a1, cloud.zs[i]);
    }
    const mid = (a0 + a1) / 2;
    const front = s1 - mid;
    const back = mid - s0;
    if (front > back * 2) return "+Z";
    if (back > front * 3) return "-Z";
    if (back > front * 2) return "maybe -Z";
    return "unclear";
  });
  if (verdicts[0] === verdicts[1]) return verdicts[0];
  return verdicts.every((v) => v === "-Z" || v === "maybe -Z") ? "maybe -Z" : "unclear";
}
function complete(fitted, template) {
  const joints = /* @__PURE__ */ new Map();
  for (const bone of template.bones) {
    const placed = fitted.get(bone.name);
    if (placed !== void 0) {
      joints.set(bone.name, placed.clone());
      continue;
    }
    const parent = template.parents.get(bone.name);
    if (parent !== void 0 && joints.has(parent)) {
      const offset = template.positions.get(bone.name).clone().sub(template.positions.get(parent));
      joints.set(bone.name, joints.get(parent).clone().add(offset));
    }
  }
  return joints;
}
function place_root(joints, template, floor_y) {
  const root = template.root.name;
  const carrier = joints.get(template.tracking_bone);
  if (carrier === void 0) {
    if (!joints.has(root)) joints.set(root, template.positions.get(root).clone());
    return;
  }
  joints.set(root, new Vector312(carrier.x, floor_y, carrier.z));
}
var cloud_cache;
var init_fit = __esm({
  "src/fit.ts"() {
    "use strict";
    init_rigger();
    init_skeleton();
    init_util();
    cloud_cache = /* @__PURE__ */ new WeakMap();
  }
});

// src/inspect.ts
import { Vector3 as Vector313 } from "three";
function triangle_index(triangles) {
  let index = index_cache.get(triangles);
  if (index !== void 0) return index;
  const count = triangles.length / 9;
  const bounds = new Float32Array(count * 6);
  for (let t = 0; t < count; t++) {
    for (let axis = 0; axis < 3; axis++) {
      const a = triangles[t * 9 + axis];
      const b = triangles[t * 9 + 3 + axis];
      const c = triangles[t * 9 + 6 + axis];
      bounds[t * 6 + axis] = Math.min(a, b, c);
      bounds[t * 6 + 3 + axis] = Math.max(a, b, c);
    }
  }
  index = { triangles, bounds };
  index_cache.set(triangles, index);
  return index;
}
function ray_triangle(o, d, tri, t) {
  const ax = tri[t * 9];
  const ay = tri[t * 9 + 1];
  const az = tri[t * 9 + 2];
  const e1x = tri[t * 9 + 3] - ax;
  const e1y = tri[t * 9 + 4] - ay;
  const e1z = tri[t * 9 + 5] - az;
  const e2x = tri[t * 9 + 6] - ax;
  const e2y = tri[t * 9 + 7] - ay;
  const e2z = tri[t * 9 + 8] - az;
  const px = d.y * e2z - d.z * e2y;
  const py = d.z * e2x - d.x * e2z;
  const pz = d.x * e2y - d.y * e2x;
  const det = e1x * px + e1y * py + e1z * pz;
  if (Math.abs(det) < 1e-14) return -1;
  const inv = 1 / det;
  const sx = o.x - ax;
  const sy = o.y - ay;
  const sz = o.z - az;
  const u = (sx * px + sy * py + sz * pz) * inv;
  if (u < 0 || u > 1) return -1;
  const qx = sy * e1z - sz * e1y;
  const qy = sz * e1x - sx * e1z;
  const qz = sx * e1y - sy * e1x;
  const v = (d.x * qx + d.y * qy + d.z * qz) * inv;
  if (v < 0 || u + v > 1) return -1;
  const dist = (e2x * qx + e2y * qy + e2z * qz) * inv;
  return dist > 1e-9 ? dist : -1;
}
function raycast(triangles, origin, direction) {
  const { bounds } = triangle_index(triangles);
  const d = direction.clone().normalize();
  const hits = [];
  const count = triangles.length / 9;
  const axis = Math.abs(d.x) > 0.9999 ? 0 : Math.abs(d.y) > 0.9999 ? 1 : Math.abs(d.z) > 0.9999 ? 2 : -1;
  const o = [origin.x, origin.y, origin.z];
  for (let t = 0; t < count; t++) {
    if (axis >= 0) {
      const a1 = (axis + 1) % 3;
      const a2 = (axis + 2) % 3;
      if (o[a1] < bounds[t * 6 + a1] || o[a1] > bounds[t * 6 + 3 + a1] || o[a2] < bounds[t * 6 + a2] || o[a2] > bounds[t * 6 + 3 + a2]) continue;
    }
    const dist = ray_triangle(origin, d, triangles, t);
    if (dist > 0) hits.push({ distance: dist, point: origin.clone().addScaledVector(d, dist) });
  }
  hits.sort((a, b) => a.distance - b.distance);
  return hits;
}
function inside(triangles, p, scale) {
  const nudge = new Vector313(137e-6, 271e-6, 193e-6).multiplyScalar(scale);
  const origin = p.clone().add(nudge);
  let hits = 0;
  for (const d of [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]) {
    if (raycast(triangles, origin, new Vector313(d[0], d[1], d[2])).length > 0) hits++;
  }
  if (hits === 6) return true;
  if (hits <= 4) return false;
  return null;
}
function joint_reports(triangles, joints, template, names) {
  const cloud = point_cloud(triangles);
  const height = Math.max(cloud.height, 1e-9);
  const center_x = joints.get(template.tracking_bone)?.x ?? (cloud.min.x + cloud.max.x) / 2;
  const wanted = names === void 0 ? [...joints.keys()] : names.filter((n) => joints.has(n));
  const children = /* @__PURE__ */ new Map();
  for (const [child, parent] of template.parents) {
    if (parent !== void 0) children.set(parent, [...children.get(parent) ?? [], child]);
  }
  const reports = [];
  for (const name of wanted) {
    const p = joints.get(name);
    let nearest = Infinity;
    for (let i = 0; i < cloud.count; i++) {
      const q = cloud.point(i);
      const d = q.distanceToSquared(p);
      if (d < nearest) nearest = d;
    }
    nearest = Math.sqrt(nearest);
    const report = {
      name,
      parent: template.parents.get(name) ?? null,
      position: vec(p),
      inside_mesh: inside(triangles, p, height),
      nearest_surface: num(nearest)
    };
    const kids = (children.get(name) ?? []).filter((k) => joints.has(k));
    const parent = template.parents.get(name);
    let dir = null;
    if (kids.length === 1) dir = joints.get(kids[0]).clone().sub(p);
    else if (parent !== void 0 && joints.has(parent)) dir = p.clone().sub(joints.get(parent));
    if (dir !== null && dir.lengthSq() > 1e-12) report.section = section(cloud, p, dir.normalize(), nearest, height);
    const partner = /[_.]l$/i.test(name) ? name.slice(0, -1) + (name.endsWith("l") ? "r" : "R") : void 0;
    if (partner !== void 0 && joints.has(partner)) {
      const r = joints.get(partner);
      report.mirror_difference = vec(new Vector313(p.x - center_x + (r.x - center_x), p.y - r.y, p.z - r.z));
    }
    reports.push(report);
  }
  return reports;
}
function section(cloud, p, dir, nearest, height) {
  const slab = 6e-3 * height;
  const reach = Math.min(Math.max(nearest * 3.5, 0.06 * height), 0.25 * height);
  const u = Math.abs(dir.y) < 0.9 ? new Vector313(0, 1, 0).cross(dir).normalize() : new Vector313(1, 0, 0).cross(dir).normalize();
  const v = dir.clone().cross(u).normalize();
  let min_u = Infinity;
  let max_u = -Infinity;
  let min_v = Infinity;
  let max_v = -Infinity;
  let n = 0;
  const rel = new Vector313();
  for (let i = 0; i < cloud.count; i++) {
    rel.copy(cloud.point(i)).sub(p);
    if (Math.abs(rel.dot(dir)) > slab) continue;
    const a = rel.dot(u);
    const b = rel.dot(v);
    if (a * a + b * b > reach * reach) continue;
    n++;
    if (a < min_u) min_u = a;
    if (a > max_u) max_u = a;
    if (b < min_v) min_v = b;
    if (b > max_v) max_v = b;
  }
  if (n < 8) return void 0;
  const offset = u.clone().multiplyScalar((min_u + max_u) / 2).addScaledVector(v, (min_v + max_v) / 2);
  return {
    offset_to_center: vec(offset),
    offset: num(offset.length()),
    width: num(max_u - min_u),
    depth: num(max_v - min_v),
    samples: n
  };
}
function flag_issues(reports, height, include_minor = false) {
  const out = [];
  for (const r of reports) {
    if (!include_minor && is_minor_joint(r.name)) continue;
    if (r.name === "root") continue;
    const issues = [];
    if (r.inside_mesh === false) issues.push(`outside the mesh (${r.nearest_surface} from the surface)`);
    const off_center_counts = !/foot|ankle|ball|toe/i.test(r.name);
    if (off_center_counts && r.section !== void 0 && r.section.samples >= 20) {
      const size = Math.max(r.section.width, r.section.depth);
      if (size > 0 && r.section.offset > size * 0.3) issues.push(`${r.section.offset} from the middle of a ${size}-wide cross-section`);
    }
    if (r.mirror_difference !== void 0) {
      const d = Math.hypot(...r.mirror_difference);
      if (d > height * 0.02) issues.push(`differs from its mirrored partner by ${num(d)}`);
    }
    if (issues.length > 0) out.push({ name: r.name, issues });
  }
  return out;
}
function slice(triangles, axis, at, thickness) {
  const cloud = point_cloud(triangles);
  const height = Math.max(cloud.height, cloud.max.x - cloud.min.x, cloud.max.z - cloud.min.z, 1e-9);
  const half = (thickness ?? 8e-3 * height) / 2;
  const cell = 0.015 * height;
  const pts = [];
  for (let i = 0; i < cloud.count; i++) {
    const q = cloud.point(i);
    if (Math.abs(q[axis] - at) <= half) pts.push(q);
  }
  const [a1, a2] = axis === "x" ? ["y", "z"] : axis === "y" ? ["x", "z"] : ["x", "y"];
  const cells = /* @__PURE__ */ new Map();
  pts.forEach((q, i) => {
    const key = `${Math.floor(q[a1] / cell)},${Math.floor(q[a2] / cell)}`;
    cells.set(key, [...cells.get(key) ?? [], i]);
  });
  const seen = /* @__PURE__ */ new Set();
  const clusters = [];
  for (const start of cells.keys()) {
    if (seen.has(start)) continue;
    const stack = [start];
    seen.add(start);
    const members = [];
    while (stack.length > 0) {
      const key = stack.pop();
      members.push(...cells.get(key));
      const [cx, cy] = key.split(",").map(Number);
      for (let dx = -1; dx <= 1; dx++) {
        for (let dy = -1; dy <= 1; dy++) {
          const k = `${cx + dx},${cy + dy}`;
          if (!seen.has(k) && cells.has(k)) {
            seen.add(k);
            stack.push(k);
          }
        }
      }
    }
    const min = new Vector313(Infinity, Infinity, Infinity);
    const max = new Vector313(-Infinity, -Infinity, -Infinity);
    for (const i of members) {
      min.min(pts[i]);
      max.max(pts[i]);
    }
    min[axis] = at;
    max[axis] = at;
    clusters.push({ center: vec(min.clone().add(max).multiplyScalar(0.5)), min: vec(min), max: vec(max), samples: members.length });
  }
  clusters.sort((a, b) => b.samples - a.samples);
  return clusters.filter((c) => c.samples >= 3);
}
var index_cache;
var init_inspect = __esm({
  "src/inspect.ts"() {
    "use strict";
    init_fit();
    init_util();
    index_cache = /* @__PURE__ */ new WeakMap();
  }
});

// src/render/font.ts
function glyph(ch) {
  return BITMAPS.get(ch.toUpperCase()) ?? BITMAPS.get("?");
}
function text_width(text, scale) {
  return text.length === 0 ? 0 : (text.length * (GLYPH_WIDTH + 1) - 1) * scale;
}
var GLYPHS, BITMAPS, GLYPH_WIDTH, GLYPH_HEIGHT;
var init_font = __esm({
  "src/render/font.ts"() {
    "use strict";
    GLYPHS = {
      A: ".###.|#...#|#...#|#####|#...#|#...#|#...#",
      B: "####.|#...#|#...#|####.|#...#|#...#|####.",
      C: ".###.|#...#|#....|#....|#....|#...#|.###.",
      D: "####.|#...#|#...#|#...#|#...#|#...#|####.",
      E: "#####|#....|#....|####.|#....|#....|#####",
      F: "#####|#....|#....|####.|#....|#....|#....",
      G: ".###.|#...#|#....|#.###|#...#|#...#|.###.",
      H: "#...#|#...#|#...#|#####|#...#|#...#|#...#",
      I: ".###.|..#..|..#..|..#..|..#..|..#..|.###.",
      J: "..###|...#.|...#.|...#.|#..#.|#..#.|.##..",
      K: "#...#|#..#.|#.#..|##...|#.#..|#..#.|#...#",
      L: "#....|#....|#....|#....|#....|#....|#####",
      M: "#...#|##.##|#.#.#|#.#.#|#...#|#...#|#...#",
      N: "#...#|#...#|##..#|#.#.#|#..##|#...#|#...#",
      O: ".###.|#...#|#...#|#...#|#...#|#...#|.###.",
      P: "####.|#...#|#...#|####.|#....|#....|#....",
      Q: ".###.|#...#|#...#|#...#|#.#.#|#..#.|.##.#",
      R: "####.|#...#|#...#|####.|#.#..|#..#.|#...#",
      S: ".####|#....|#....|.###.|....#|....#|####.",
      T: "#####|..#..|..#..|..#..|..#..|..#..|..#..",
      U: "#...#|#...#|#...#|#...#|#...#|#...#|.###.",
      V: "#...#|#...#|#...#|#...#|#...#|.#.#.|..#..",
      W: "#...#|#...#|#...#|#.#.#|#.#.#|#.#.#|.#.#.",
      X: "#...#|#...#|.#.#.|..#..|.#.#.|#...#|#...#",
      Y: "#...#|#...#|.#.#.|..#..|..#..|..#..|..#..",
      Z: "#####|....#|...#.|..#..|.#...|#....|#####",
      0: ".###.|#...#|#..##|#.#.#|##..#|#...#|.###.",
      1: "..#..|.##..|..#..|..#..|..#..|..#..|.###.",
      2: ".###.|#...#|....#|...#.|..#..|.#...|#####",
      3: "#####|...#.|..#..|...#.|....#|#...#|.###.",
      4: "...#.|..##.|.#.#.|#..#.|#####|...#.|...#.",
      5: "#####|#....|####.|....#|....#|#...#|.###.",
      6: "..##.|.#...|#....|####.|#...#|#...#|.###.",
      7: "#####|....#|...#.|..#..|.#...|.#...|.#...",
      8: ".###.|#...#|#...#|.###.|#...#|#...#|.###.",
      9: ".###.|#...#|#...#|.####|....#|...#.|.##..",
      _: ".....|.....|.....|.....|.....|.....|#####",
      ".": ".....|.....|.....|.....|.....|.##..|.##..",
      "-": ".....|.....|.....|#####|.....|.....|.....",
      "+": ".....|..#..|..#..|#####|..#..|..#..|.....",
      ":": ".....|.##..|.##..|.....|.##..|.##..|.....",
      "/": "....#|....#|...#.|..#..|.#...|#....|#....",
      "(": "...#.|..#..|.#...|.#...|.#...|..#..|...#.",
      ")": ".#...|..#..|...#.|...#.|...#.|..#..|.#...",
      ",": ".....|.....|.....|.....|.##..|..#..|.#...",
      "%": "##...|##..#|...#.|..#..|.#...|#..##|...##",
      "=": ".....|.....|#####|.....|#####|.....|.....",
      "[": ".###.|.#...|.#...|.#...|.#...|.#...|.###.",
      "]": ".###.|...#.|...#.|...#.|...#.|...#.|.###.",
      "<": "...#.|..#..|.#...|#....|.#...|..#..|...#.",
      ">": ".#...|..#..|...#.|....#|...#.|..#..|.#...",
      "?": ".###.|#...#|....#|...#.|..#..|.....|..#..",
      "!": "..#..|..#..|..#..|..#..|..#..|.....|..#..",
      "'": "..#..|..#..|.#...|.....|.....|.....|.....",
      " ": ".....|.....|.....|.....|.....|.....|....."
    };
    BITMAPS = /* @__PURE__ */ new Map();
    for (const [ch, rows] of Object.entries(GLYPHS)) {
      BITMAPS.set(ch, rows.split("|").map((row) => [...row].map((c) => c === "#")));
    }
    GLYPH_WIDTH = 5;
    GLYPH_HEIGHT = 7;
  }
});

// src/render/png.ts
import { deflateSync } from "node:zlib";
function crc32(bytes) {
  let c = 4294967295;
  for (let i = 0; i < bytes.length; i++) c = CRC_TABLE[(c ^ bytes[i]) & 255] ^ c >>> 8;
  return (c ^ 4294967295) >>> 0;
}
function chunk(type, data) {
  const out = Buffer.alloc(12 + data.length);
  out.writeUInt32BE(data.length, 0);
  out.write(type, 4, "ascii");
  Buffer.from(data).copy(out, 8);
  out.writeUInt32BE(crc32(out.subarray(4, 8 + data.length)), 8 + data.length);
  return out;
}
function encode_png(width, height, rgb) {
  const header = Buffer.alloc(13);
  header.writeUInt32BE(width, 0);
  header.writeUInt32BE(height, 4);
  header[8] = 8;
  header[9] = 2;
  const raw = Buffer.alloc((width * 3 + 1) * height);
  for (let y = 0; y < height; y++) {
    raw[y * (width * 3 + 1)] = 0;
    Buffer.from(rgb.buffer, rgb.byteOffset + y * width * 3, width * 3).copy(raw, y * (width * 3 + 1) + 1);
  }
  return Buffer.concat([
    Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]),
    chunk("IHDR", header),
    chunk("IDAT", deflateSync(raw, { level: 6 })),
    chunk("IEND", new Uint8Array(0))
  ]);
}
var CRC_TABLE;
var init_png = __esm({
  "src/render/png.ts"() {
    "use strict";
    CRC_TABLE = (() => {
      const table = new Uint32Array(256);
      for (let n = 0; n < 256; n++) {
        let c = n;
        for (let k = 0; k < 8; k++) c = (c & 1) !== 0 ? 3988292384 ^ c >>> 1 : c >>> 1;
        table[n] = c >>> 0;
      }
      return table;
    })();
  }
});

// src/render/raster.ts
function overlaps(a, b) {
  return a.x < b.x + b.w && b.x < a.x + a.w && a.y < b.y + b.h && b.y < a.y + a.h;
}
var Raster;
var init_raster = __esm({
  "src/render/raster.ts"() {
    "use strict";
    init_font();
    init_png();
    Raster = class {
      width;
      height;
      rgb;
      depth;
      /** when set, drawing outside this rectangle is skipped */
      clip = null;
      constructor(width, height, background) {
        this.width = width;
        this.height = height;
        this.rgb = new Uint8Array(width * height * 3);
        this.depth = new Float32Array(width * height).fill(Infinity);
        for (let i = 0; i < width * height; i++) {
          this.rgb[i * 3] = background[0];
          this.rgb[i * 3 + 1] = background[1];
          this.rgb[i * 3 + 2] = background[2];
        }
      }
      blend(x, y, color, alpha = 1) {
        if (x < 0 || y < 0 || x >= this.width || y >= this.height) return;
        const c = this.clip;
        if (c !== null && (x < c.x || y < c.y || x >= c.x + c.w || y >= c.y + c.h)) return;
        const i = ((y | 0) * this.width + (x | 0)) * 3;
        if (alpha >= 1) {
          this.rgb[i] = color[0];
          this.rgb[i + 1] = color[1];
          this.rgb[i + 2] = color[2];
          return;
        }
        this.rgb[i] = this.rgb[i] + (color[0] - this.rgb[i]) * alpha;
        this.rgb[i + 1] = this.rgb[i + 1] + (color[1] - this.rgb[i + 1]) * alpha;
        this.rgb[i + 2] = this.rgb[i + 2] + (color[2] - this.rgb[i + 2]) * alpha;
      }
      /** screen-space triangle with per-vertex depth (smaller is closer), clipped to a rectangle */
      triangle(x0, y0, z0, x1, y1, z1, x2, y2, z2, color, clip) {
        const min_x = Math.max(clip.x, Math.floor(Math.min(x0, x1, x2)));
        const max_x = Math.min(clip.x + clip.w - 1, Math.ceil(Math.max(x0, x1, x2)));
        const min_y = Math.max(clip.y, Math.floor(Math.min(y0, y1, y2)));
        const max_y = Math.min(clip.y + clip.h - 1, Math.ceil(Math.max(y0, y1, y2)));
        if (min_x > max_x || min_y > max_y) return;
        const area = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0);
        if (Math.abs(area) < 1e-12) return;
        const inv = 1 / area;
        for (let y = min_y; y <= max_y; y++) {
          const py = y + 0.5;
          for (let x = min_x; x <= max_x; x++) {
            const px = x + 0.5;
            const w0 = ((x1 - px) * (y2 - py) - (x2 - px) * (y1 - py)) * inv;
            const w1 = ((x2 - px) * (y0 - py) - (x0 - px) * (y2 - py)) * inv;
            const w2 = 1 - w0 - w1;
            if (w0 < 0 || w1 < 0 || w2 < 0) continue;
            const z3 = w0 * z0 + w1 * z1 + w2 * z2;
            const di = y * this.width + x;
            if (z3 >= this.depth[di]) continue;
            this.depth[di] = z3;
            const i = di * 3;
            this.rgb[i] = color[0];
            this.rgb[i + 1] = color[1];
            this.rgb[i + 2] = color[2];
          }
        }
      }
      disc(cx, cy, r, color, alpha = 1) {
        for (let y = Math.floor(cy - r); y <= Math.ceil(cy + r); y++) {
          for (let x = Math.floor(cx - r); x <= Math.ceil(cx + r); x++) {
            const dx = x + 0.5 - cx;
            const dy = y + 0.5 - cy;
            if (dx * dx + dy * dy <= r * r) this.blend(x, y, color, alpha);
          }
        }
      }
      line(x0, y0, x1, y1, color, width = 1, alpha = 1) {
        const length = Math.hypot(x1 - x0, y1 - y0);
        const steps = Math.max(1, Math.ceil(length * 2));
        const r = width / 2;
        const seen = /* @__PURE__ */ new Set();
        for (let s = 0; s <= steps; s++) {
          const t = s / steps;
          const cx = x0 + (x1 - x0) * t;
          const cy = y0 + (y1 - y0) * t;
          for (let y = Math.floor(cy - r); y <= Math.ceil(cy + r); y++) {
            for (let x = Math.floor(cx - r); x <= Math.ceil(cx + r); x++) {
              const dx = x + 0.5 - cx;
              const dy = y + 0.5 - cy;
              if (dx * dx + dy * dy > r * r + 0.25) continue;
              const key = y * this.width + x;
              if (seen.has(key)) continue;
              seen.add(key);
              this.blend(x, y, color, alpha);
            }
          }
        }
      }
      rect(x, y, w, h, color, alpha = 1) {
        for (let yy = Math.max(0, y); yy < Math.min(this.height, y + h); yy++) {
          for (let xx = Math.max(0, x); xx < Math.min(this.width, x + w); xx++) this.blend(xx, yy, color, alpha);
        }
      }
      /** text with its top-left at (x, y); a halo keeps it readable over the mesh */
      text(x, y, text, color, scale = 2, halo) {
        const draw = (ox, oy, c) => {
          let cx = x + ox;
          for (const ch of text) {
            const bitmap = glyph(ch);
            for (let row = 0; row < GLYPH_HEIGHT; row++) {
              for (let col = 0; col < GLYPH_WIDTH; col++) {
                if (!bitmap[row][col]) continue;
                for (let sy = 0; sy < scale; sy++) {
                  for (let sx = 0; sx < scale; sx++) this.blend(cx + col * scale + sx, y + oy + row * scale + sy, c);
                }
              }
            }
            cx += (GLYPH_WIDTH + 1) * scale;
          }
        };
        if (halo !== void 0) {
          for (const [ox, oy] of [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [1, 1], [-1, 1], [1, -1]]) draw(ox, oy, halo);
        }
        draw(0, 0, color);
      }
      text_size(text, scale = 2) {
        return { w: text_width(text, scale), h: GLYPH_HEIGHT * scale };
      }
      png() {
        return encode_png(this.width, this.height, this.rgb);
      }
    };
  }
});

// src/render/render.ts
import { Vector3 as Vector314 } from "three";
function side_of(name) {
  const n = name.toLowerCase();
  if (/(^|_)l$|_l_|left/.test(n)) return "left";
  if (/(^|_)r$|_r_|right/.test(n)) return "right";
  return "center";
}
function render_views(request) {
  const size = Math.max(160, Math.min(2048, Math.round(request.size)));
  const panel_w = MARGIN_LEFT + size;
  const panel_h = HEADER + size + MARGIN_BOTTOM;
  const width = panel_w * request.views.length + GAP2 * (request.views.length - 1);
  const raster = new Raster(width, panel_h, BACKGROUND);
  const panels = [];
  const joint_pixels = {};
  request.views.forEach((view, index) => {
    const basis = VIEWS[view];
    const ox = index * (panel_w + GAP2);
    const area = { x: ox + MARGIN_LEFT, y: HEADER, w: size, h: size };
    let center_r;
    let center_u;
    let span;
    if (request.focus !== void 0) {
      center_r = request.focus.center.dot(basis.right);
      center_u = request.focus.center.dot(basis.up);
      span = request.focus.radius * 2;
    } else {
      let min_r = Infinity;
      let max_r = -Infinity;
      let min_u = Infinity;
      let max_u = -Infinity;
      const v = new Vector314();
      const take = (x, y, z2) => {
        v.set(x, y, z2);
        const r = v.dot(basis.right);
        const u = v.dot(basis.up);
        if (r < min_r) min_r = r;
        if (r > max_r) max_r = r;
        if (u < min_u) min_u = u;
        if (u > max_u) max_u = u;
      };
      for (const mesh of request.meshes) {
        const stride = Math.max(1, Math.floor(mesh.positions.length / 3 / 2e5));
        for (let i = 0; i < mesh.positions.length / 3; i += stride) take(mesh.positions[i * 3], mesh.positions[i * 3 + 1], mesh.positions[i * 3 + 2]);
      }
      for (const p of request.joints?.values() ?? []) take(p.x, p.y, p.z);
      if (!Number.isFinite(min_r)) {
        min_r = -1;
        max_r = 1;
        min_u = -1;
        max_u = 1;
      }
      center_r = (min_r + max_r) / 2;
      center_u = (min_u + max_u) / 2;
      span = Math.max(max_r - min_r, max_u - min_u, 1e-6) * 1.08;
    }
    const scale = size / span;
    const to_px = (p) => [
      area.x + size / 2 + (p.dot(basis.right) - center_r) * scale,
      area.y + size / 2 - (p.dot(basis.up) - center_u) * scale,
      p.dot(basis.forward)
    ];
    draw_grid(raster, area, center_r, center_u, scale, size, axis_sign(basis.right), axis_sign(basis.up));
    const a = new Vector314();
    const b = new Vector314();
    const c = new Vector314();
    const e1 = new Vector314();
    const e2 = new Vector314();
    const n = new Vector314();
    const toward_camera = basis.forward.clone().negate();
    for (const mesh of request.meshes) {
      const pos = mesh.positions;
      const idx = mesh.index;
      for (let t = 0; t + 2 < idx.length; t += 3) {
        a.fromArray(pos, idx[t] * 3);
        b.fromArray(pos, idx[t + 1] * 3);
        c.fromArray(pos, idx[t + 2] * 3);
        n.crossVectors(e1.subVectors(b, a), e2.subVectors(c, a));
        const len = n.length();
        if (len < 1e-20) continue;
        const facing = n.dot(toward_camera) / len;
        let color;
        if (mesh.triangle_colors !== void 0) {
          const k = t / 3 * 3;
          const shade = 0.55 + 0.45 * Math.abs(facing);
          color = [mesh.triangle_colors[k] * shade, mesh.triangle_colors[k + 1] * shade, mesh.triangle_colors[k + 2] * shade];
        } else if (facing >= 0) {
          const shade = 0.42 + 0.58 * facing;
          color = [MESH[0] * shade, MESH[1] * shade, MESH[2] * shade];
        } else {
          const shade = 0.45 + 0.3 * -facing;
          color = [MESH_BACK[0] * shade, MESH_BACK[1] * shade, MESH_BACK[2] * shade];
        }
        const pa = to_px(a);
        const pb = to_px(b);
        const pc = to_px(c);
        raster.triangle(pa[0], pa[1], pa[2], pb[0], pb[1], pb[2], pc[0], pc[1], pc[2], color, area);
      }
    }
    if (request.xray === true) raster.rect(area.x, area.y, area.w, area.h, BACKGROUND, 0.72);
    raster.clip = area;
    const joints = request.joints ?? /* @__PURE__ */ new Map();
    const drawn = [...joints.keys()].filter((name) => request.draw === void 0 || request.draw.has(name));
    const line_width = Math.max(2, size / 300);
    const radius = Math.max(3.5, size / 170);
    const color_of = (name) => side_of(name) === "left" ? LEFT : side_of(name) === "right" ? RIGHT : CENTER;
    for (const name of drawn) {
      const parent = request.parents?.get(name);
      if (parent === void 0 || !drawn.includes(parent)) continue;
      const p = to_px(joints.get(parent));
      const q = to_px(joints.get(name));
      raster.line(p[0], p[1], q[0], q[1], WHITE, line_width + 2, 0.9);
      raster.line(p[0], p[1], q[0], q[1], color_of(name), line_width);
    }
    for (const name of drawn) {
      const [x, y] = to_px(joints.get(name));
      raster.disc(x, y, radius + 1.5, INK);
      raster.disc(x, y, radius, color_of(name));
      joint_pixels[name] ??= {};
      joint_pixels[name][view] = [Math.round(x), Math.round(y)];
    }
    const taken = [];
    const label_scale = size >= 480 ? 2 : 1;
    for (const name of drawn) {
      if (request.label !== void 0 && !request.label.has(name)) continue;
      const [x, y] = to_px(joints.get(name));
      const text = name;
      const { w, h } = raster.text_size(text, label_scale);
      const outward_right = x >= area.x + size / 2;
      const candidates = [
        { x: x + radius + 4, y: y - h / 2, w, h },
        { x: x - radius - 4 - w, y: y - h / 2, w, h },
        { x: x - w / 2, y: y - radius - 4 - h, w, h },
        { x: x - w / 2, y: y + radius + 4, w, h }
      ];
      if (!outward_right) [candidates[0], candidates[1]] = [candidates[1], candidates[0]];
      const spot = candidates.find((r) => r.x >= area.x && r.y >= area.y && r.x + r.w <= area.x + area.w && r.y + r.h <= area.y + area.h && !taken.some((o) => overlaps(o, r)));
      if (spot === void 0) continue;
      taken.push({ x: spot.x - 2, y: spot.y - 2, w: spot.w + 4, h: spot.h + 4 });
      raster.text(Math.round(spot.x), Math.round(spot.y), text, INK, label_scale, WHITE);
    }
    raster.clip = null;
    for (const marker of request.markers ?? []) {
      const [x, y] = to_px(marker.position);
      raster.line(x - 6, y - 6, x + 6, y + 6, MARKER, 2.5);
      raster.line(x - 6, y + 6, x + 6, y - 6, MARKER, 2.5);
      if (marker.label !== void 0) raster.text(Math.round(x + 9), Math.round(y - 7), marker.label, MARKER, label_scale, WHITE);
    }
    const header = `${view.toUpperCase()}  RIGHT ${basis.right_label}  UP ${basis.up_label}`;
    raster.text(ox + MARGIN_LEFT, 6, header, INK, 2);
    if (request.title !== void 0 && index === 0) {
      const tw = raster.text_size(request.title, 2).w;
      if (MARGIN_LEFT + raster.text_size(header, 2).w + 24 + tw < panel_w) raster.text(ox + panel_w - tw, 6, request.title, [82, 82, 91], 2);
    }
    frame(raster, area);
    panels.push({
      view,
      area: [area.x, area.y, area.w, area.h],
      screen_right: basis.right_label,
      screen_up: basis.up_label,
      camera: basis.note,
      pixels_per_unit: num(scale),
      center: [num(center_r * axis_sign(basis.right)), num(center_u * axis_sign(basis.up))]
    });
  });
  return { png: raster.png(), width, height: panel_h, panels, joint_pixels };
}
function axis_sign(v) {
  return v.x + v.y + v.z >= 0 ? 1 : -1;
}
function draw_grid(raster, area, center_r, center_u, scale, size, sign_r, sign_u) {
  const span = size / scale;
  const step = nice_step(span / 8);
  const decimals = Math.max(0, -Math.floor(Math.log10(step) + 1e-9));
  const format = (v) => (Math.abs(v) < step / 1e3 ? 0 : v).toFixed(decimals);
  let ruler_scale = size >= 480 ? 2 : 1;
  const widest = Math.max(...[-1, 1].map((k) => raster.text_size(format(k * (Math.abs(center_r) + Math.abs(center_u) + span)), ruler_scale).w));
  if (widest > MARGIN_LEFT - 12) ruler_scale = 1;
  const every = Math.max(1, Math.ceil((raster.text_size(format(-(Math.abs(center_r) + span)), ruler_scale).w + 10) / (step * scale)));
  const r0 = center_r - span / 2;
  for (let v = Math.ceil(r0 / step) * step; v <= r0 + span; v += step) {
    const x = Math.round(area.x + (v - r0) * scale);
    for (let y = area.y; y < area.y + area.h; y++) raster.blend(x, y, [200, 204, 212], 0.8);
    raster.line(x, area.y + area.h, x, area.y + area.h + 5, INK, 1);
    if (Math.round(v / step) % every !== 0) continue;
    const text = format(v * sign_r);
    const w = raster.text_size(text, ruler_scale).w;
    raster.text(Math.round(x - w / 2), area.y + area.h + 8, text, INK, ruler_scale);
  }
  const u0 = center_u - span / 2;
  for (let v = Math.ceil(u0 / step) * step; v <= u0 + span; v += step) {
    const y = Math.round(area.y + area.h - (v - u0) * scale);
    for (let x = area.x; x < area.x + area.w; x++) raster.blend(x, y, [200, 204, 212], 0.8);
    raster.line(area.x - 5, y, area.x, y, INK, 1);
    const text = format(v * sign_u);
    const w = raster.text_size(text, ruler_scale).w;
    raster.text(area.x - 8 - w, y - Math.round(3.5 * ruler_scale), text, INK, ruler_scale);
  }
}
function frame(raster, area) {
  const c = [113, 113, 122];
  raster.line(area.x, area.y, area.x + area.w, area.y, c, 1);
  raster.line(area.x, area.y + area.h, area.x + area.w, area.y + area.h, c, 1);
  raster.line(area.x, area.y, area.x, area.y + area.h, c, 1);
  raster.line(area.x + area.w, area.y, area.x + area.w, area.y + area.h, c, 1);
}
function nice_step(raw) {
  const power = Math.pow(10, Math.floor(Math.log10(raw)));
  const n = raw / power;
  return (n < 1.5 ? 1 : n < 3.5 ? 2 : n < 7.5 ? 5 : 10) * power;
}
var VIEW_NAMES, VIEWS, BACKGROUND, MESH, MESH_BACK, LEFT, RIGHT, CENTER, INK, WHITE, MARKER, MARGIN_LEFT, MARGIN_BOTTOM, HEADER, GAP2;
var init_render = __esm({
  "src/render/render.ts"() {
    "use strict";
    init_raster();
    init_util();
    VIEW_NAMES = ["front", "back", "left", "right", "top", "bottom"];
    VIEWS = {
      front: { right: new Vector314(1, 0, 0), up: new Vector314(0, 1, 0), forward: new Vector314(0, 0, -1), right_label: "+X", up_label: "+Y", note: "camera at +Z looking toward -Z" },
      back: { right: new Vector314(-1, 0, 0), up: new Vector314(0, 1, 0), forward: new Vector314(0, 0, 1), right_label: "-X", up_label: "+Y", note: "camera at -Z looking toward +Z" },
      left: { right: new Vector314(0, 0, -1), up: new Vector314(0, 1, 0), forward: new Vector314(-1, 0, 0), right_label: "-Z", up_label: "+Y", note: "camera at +X looking toward -X" },
      right: { right: new Vector314(0, 0, 1), up: new Vector314(0, 1, 0), forward: new Vector314(1, 0, 0), right_label: "+Z", up_label: "+Y", note: "camera at -X looking toward +X" },
      top: { right: new Vector314(1, 0, 0), up: new Vector314(0, 0, -1), forward: new Vector314(0, -1, 0), right_label: "+X", up_label: "-Z", note: "camera at +Y looking down" },
      bottom: { right: new Vector314(1, 0, 0), up: new Vector314(0, 0, 1), forward: new Vector314(0, 1, 0), right_label: "+X", up_label: "+Z", note: "camera at -Y looking up" }
    };
    BACKGROUND = [238, 240, 243];
    MESH = [186, 194, 206];
    MESH_BACK = [196, 160, 160];
    LEFT = [37, 99, 235];
    RIGHT = [220, 38, 38];
    CENTER = [234, 130, 12];
    INK = [24, 24, 27];
    WHITE = [255, 255, 255];
    MARKER = [192, 38, 211];
    MARGIN_LEFT = 96;
    MARGIN_BOTTOM = 34;
    HEADER = 26;
    GAP2 = 12;
  }
});

// src/bind.ts
import { Matrix4 as Matrix42, Vector3 as Vector315 } from "three";
function bind(primitives, rig, skeleton_type, options = {}) {
  rig.armature.updateMatrixWorld(true);
  const solver = new SkinningAlgorithm(rig.root, skeleton_type);
  if (options.head_weight_correction_height !== void 0) {
    solver.set_head_weight_correction_enabled(true);
    solver.set_preview_plane_height(options.head_weight_correction_height);
  }
  if (options.arm_plane_correction_offset !== void 0) {
    solver.set_arm_plane_correction_enabled(true);
    solver.set_arm_plane_offset(options.arm_plane_correction_offset);
  }
  const weights = primitives.map((p) => {
    solver.set_geometry(p.geometry);
    const [indices, w] = solver.calculate_indexes_and_weights();
    return { indices: Uint16Array.from(indices), weights: Float32Array.from(w) };
  });
  const result = { weights, bone_names: rig.bones.map((b) => b.name) };
  if (options.fix_stray_patches !== false) fix_stray_patches(primitives, result, rig);
  return result;
}
function fix_stray_patches(primitives, result, rig) {
  rig.armature.updateMatrixWorld(true);
  const joint = rig.bones.map((b) => b.getWorldPosition(new Vector315()));
  const bone_index = new Map(rig.bones.map((b, i) => [b, i]));
  const region = rig.bones.map((bone) => {
    let top = -1;
    for (let b = bone; b !== null && b.isBone === true; b = b.parent) {
      if (is_limb_bone(b.name)) top = bone_index.get(b) ?? top;
    }
    return top;
  });
  let changed = 0;
  primitives.forEach((primitive, pi) => {
    const pos = primitive.geometry.attributes.position.array;
    const { indices, weights } = result.weights[pi];
    const count = pos.length / 3;
    const { weld, neighbors } = connectivity(primitive);
    const owner = new Int32Array(count).fill(-1);
    for (let v = 0; v < count; v++) {
      if (weld[v] !== v) continue;
      let best = -1;
      let best_w = 0;
      for (let k = 0; k < 4; k++) if (weights[v * 4 + k] > best_w) {
        best_w = weights[v * 4 + k];
        best = indices[v * 4 + k];
      }
      owner[v] = best;
    }
    const limb = (v) => owner[v] < 0 ? -2 : region[owner[v]];
    const piece = new Int32Array(count).fill(-1);
    const pieces = [];
    const p3 = new Vector315();
    for (let start = 0; start < count; start++) {
      if (weld[start] !== start || piece[start] !== -1 || limb(start) < 0) continue;
      const l = limb(start);
      const id = pieces.length;
      const members = [];
      let reach = Infinity;
      let bordered = false;
      const stack = [start];
      piece[start] = id;
      while (stack.length > 0) {
        const v = stack.pop();
        members.push(v);
        reach = Math.min(reach, p3.set(pos[v * 3], pos[v * 3 + 1], pos[v * 3 + 2]).distanceToSquared(joint[l]));
        for (const n of neighbors[v]) {
          if (limb(n) === l) {
            if (piece[n] === -1) {
              piece[n] = id;
              stack.push(n);
            }
          } else if (owner[n] >= 0) bordered = true;
        }
      }
      pieces.push({ limb: l, members, reach, bordered });
    }
    const main2 = /* @__PURE__ */ new Map();
    pieces.forEach((p, id) => {
      const current = main2.get(p.limb);
      if (current === void 0 || p.reach < pieces[current].reach) main2.set(p.limb, id);
    });
    const stray = new Uint8Array(count);
    pieces.forEach((p, id) => {
      if (main2.get(p.limb) === id || !p.bordered) return;
      for (const v of p.members) stray[v] = 1;
    });
    let frontier = [];
    for (let v = 0; v < count; v++) {
      if (stray[v] !== 1) continue;
      if (neighbors[v].some((n) => stray[n] === 0 && owner[n] >= 0)) frontier.push(v);
    }
    while (frontier.length > 0) {
      const next = [];
      for (const v of frontier) {
        if (stray[v] !== 1) continue;
        const n = neighbors[v].find((m) => stray[m] === 0 && owner[m] >= 0);
        if (n === void 0) continue;
        owner[v] = owner[n];
        stray[v] = 0;
        changed++;
        for (const m of neighbors[v]) if (stray[m] === 1) next.push(m);
      }
      frontier = next;
    }
    for (let v = 0; v < count; v++) {
      const w = weld[v];
      if (w === v && stray[v] === 0 && changed === 0) continue;
      const o = owner[w];
      if (o < 0) continue;
      let best = -1;
      let best_w = 0;
      for (let k = 0; k < 4; k++) if (weights[v * 4 + k] > best_w) {
        best_w = weights[v * 4 + k];
        best = indices[v * 4 + k];
      }
      if (best === o) continue;
      if (region[best] === region[o] && region[o] >= 0) continue;
      indices[v * 4] = o;
      weights[v * 4] = 1;
      for (let k = 1; k < 4; k++) weights[v * 4 + k] = 0;
    }
  });
  return changed;
}
function connectivity(primitive) {
  const pos = primitive.geometry.attributes.position.array;
  const index = primitive.geometry.index.array;
  const count = pos.length / 3;
  const weld = new Int32Array(count);
  const seen = /* @__PURE__ */ new Map();
  for (let v = 0; v < count; v++) {
    const key = `${Math.round(pos[v * 3] * 1e5)},${Math.round(pos[v * 3 + 1] * 1e5)},${Math.round(pos[v * 3 + 2] * 1e5)}`;
    const first = seen.get(key);
    if (first === void 0) {
      seen.set(key, v);
      weld[v] = v;
    } else weld[v] = first;
  }
  const neighbors = Array.from({ length: count }, () => []);
  for (let t = 0; t + 2 < index.length; t += 3) {
    const a = weld[index[t]];
    const b = weld[index[t + 1]];
    const c = weld[index[t + 2]];
    neighbors[a].push(b, c);
    neighbors[b].push(a, c);
    neighbors[c].push(a, b);
  }
  return { weld, neighbors };
}
function piece_at(primitives, point, meshes) {
  const target = new Vector315(...point);
  const p = new Vector315();
  let best_pi = -1;
  let best_v = -1;
  let best_d = Infinity;
  primitives.forEach((primitive, pi) => {
    if (meshes !== void 0 && !meshes.includes(primitive.mesh_id)) return;
    const pos = primitive.geometry.attributes.position.array;
    for (let v = 0; v < pos.length / 3; v++) {
      const d = p.set(pos[v * 3], pos[v * 3 + 1], pos[v * 3 + 2]).distanceToSquared(target);
      if (d < best_d) {
        best_d = d;
        best_pi = pi;
        best_v = v;
      }
    }
  });
  if (best_pi < 0) return null;
  const { weld, neighbors } = connectivity(primitives[best_pi]);
  const inside2 = new Uint8Array(weld.length);
  const stack = [weld[best_v]];
  inside2[weld[best_v]] = 1;
  while (stack.length > 0) {
    for (const n of neighbors[stack.pop()]) if (inside2[n] === 0) {
      inside2[n] = 1;
      stack.push(n);
    }
  }
  for (let v = 0; v < weld.length; v++) inside2[v] = inside2[weld[v]];
  return [best_pi, inside2];
}
function expand_bones(names, rig) {
  const index = new Map(rig.bones.map((b, i) => [b.name, i]));
  const out = /* @__PURE__ */ new Set();
  for (const raw of names) {
    const subtree = raw.endsWith("*") ? rig.by_name.get(raw.slice(0, -1)) : void 0;
    if (subtree !== void 0) {
      subtree.traverse((b) => {
        const i2 = index.get(b.name);
        if (i2 !== void 0) out.add(i2);
      });
      continue;
    }
    if (raw.includes("*")) {
      const pattern = new RegExp("^" + raw.split("*").map((part) => part.replace(/[.+?^${}()|[\]\\]/g, "\\$&")).join(".*") + "$");
      const matched = rig.bones.filter((b) => pattern.test(b.name));
      if (matched.length === 0) throw new Error(`No bones match "${raw}" in a weight rule.`);
      for (const b of matched) out.add(index.get(b.name));
      continue;
    }
    const i = index.get(raw);
    if (i === void 0) throw new Error(`Unknown bone "${raw}" in a weight rule.`);
    out.add(i);
  }
  return out;
}
function apply_weight_rules(result, primitives, rig, rules) {
  rig.armature.updateMatrixWorld(true);
  const positions = rig.bones.map((b) => b.getWorldPosition(new Vector315()));
  const segments = rig.bones.map((bone, i) => {
    const kids = bone.children.filter((c) => c.isBone === true).map((c) => rig.bones.indexOf(c)).filter((k) => k >= 0);
    return kids.length > 0 ? kids.map((k) => [positions[i], positions[k]]) : [[positions[i], positions[i]]];
  });
  const distance_to_bone = (p2, bone) => {
    let best = Infinity;
    for (const [a, b] of segments[bone]) {
      const ab = b.clone().sub(a);
      const t = ab.lengthSq() > 1e-12 ? Math.min(1, Math.max(0, p2.clone().sub(a).dot(ab) / ab.lengthSq())) : 0;
      best = Math.min(best, a.clone().addScaledVector(ab, t).distanceTo(p2));
    }
    return best;
  };
  const counts = rules.map(() => 0);
  const p = new Vector315();
  rules.forEach((rule, r) => {
    const listed = expand_bones(rule.bones, rig);
    const allowed = (bone) => rule.mode === "only" ? listed.has(bone) : !listed.has(bone);
    const box = rule.box;
    const sphere = rule.sphere;
    const center = sphere !== void 0 ? new Vector315(...sphere.center) : null;
    const piece = rule.piece_at !== void 0 ? piece_at(primitives, rule.piece_at, rule.meshes) : null;
    if (rule.piece_at !== void 0 && piece === null) return;
    primitives.forEach((primitive, pi) => {
      if (rule.meshes !== void 0 && !rule.meshes.includes(primitive.mesh_id)) return;
      if (piece !== null && piece[0] !== pi) return;
      const pos = primitive.geometry.attributes.position.array;
      const { indices, weights } = result.weights[pi];
      for (let v = 0; v < pos.length / 3; v++) {
        p.set(pos[v * 3], pos[v * 3 + 1], pos[v * 3 + 2]);
        if (box !== void 0 && (p.x < box.min[0] || p.y < box.min[1] || p.z < box.min[2] || p.x > box.max[0] || p.y > box.max[1] || p.z > box.max[2])) continue;
        if (center !== null && p.distanceTo(center) > sphere.radius) continue;
        if (piece !== null && piece[1][v] === 0) continue;
        let changed = false;
        let sum = 0;
        for (let k = 0; k < 4; k++) {
          if (weights[v * 4 + k] > 0 && !allowed(indices[v * 4 + k])) {
            weights[v * 4 + k] = 0;
            changed = true;
          }
          sum += weights[v * 4 + k];
        }
        if (!changed) continue;
        counts[r]++;
        if (sum < 1e-6) {
          let best = -1;
          let best_d = Infinity;
          for (let bone = 0; bone < rig.bones.length; bone++) {
            if (!allowed(bone)) continue;
            const d = distance_to_bone(p, bone);
            if (d < best_d) {
              best_d = d;
              best = bone;
            }
          }
          if (best < 0) continue;
          indices[v * 4] = best;
          weights[v * 4] = 1;
          for (let k = 1; k < 4; k++) weights[v * 4 + k] = 0;
        } else {
          for (let k = 0; k < 4; k++) weights[v * 4 + k] /= sum;
        }
      }
    });
  });
  return counts;
}
function bind_stats(result) {
  const per_bone = new Array(result.bone_names.length).fill(0);
  let vertices = 0;
  let unweighted = 0;
  for (const { indices, weights } of result.weights) {
    for (let v = 0; v < weights.length / 4; v++) {
      vertices++;
      let best = -1;
      let best_w = 0;
      let sum = 0;
      for (let k = 0; k < 4; k++) {
        const w = weights[v * 4 + k];
        sum += w;
        if (w > best_w) {
          best_w = w;
          best = indices[v * 4 + k];
        }
      }
      if (sum < 1e-6 || best < 0) unweighted++;
      else per_bone[best]++;
    }
  }
  const vertices_per_bone = {};
  const bones_without_vertices = [];
  result.bone_names.forEach((name, i) => {
    if (per_bone[i] > 0) vertices_per_bone[name] = per_bone[i];
    else bones_without_vertices.push(name);
  });
  return { vertices, unweighted_vertices: unweighted, vertices_per_bone, bones_without_vertices };
}
function lowest_skinned_point(primitives, binding, rest3, limit = 4e3) {
  rest3.armature.updateMatrixWorld(true);
  const inverse = rest3.bones.map((b) => b.matrixWorld.clone().invert());
  let total = 0;
  for (const p of primitives) total += p.geometry.attributes.position.count;
  const stride = Math.max(1, Math.floor(total / limit));
  const samples = [];
  let seen = 0;
  primitives.forEach((p, pi) => {
    const pos = p.geometry.attributes.position.array;
    const { indices, weights } = binding.weights[pi];
    for (let v = 0; v < pos.length / 3; v++, seen++) {
      if (seen % stride !== 0) continue;
      samples.push({ x: pos[v * 3], y: pos[v * 3 + 1], z: pos[v * 3 + 2], j: Array.from(indices.subarray(v * 4, v * 4 + 4)), w: Array.from(weights.subarray(v * 4, v * 4 + 4)) });
    }
  });
  return (posed) => {
    posed.armature.updateMatrixWorld(true);
    const skin = posed.bones.map((b, i) => new Matrix42().multiplyMatrices(b.matrixWorld, inverse[i]).elements);
    let low = Infinity;
    for (const s of samples) {
      let y = 0;
      let total_w = 0;
      for (let k = 0; k < 4; k++) {
        const w = s.w[k];
        if (w === 0) continue;
        const e = skin[s.j[k]];
        y += (e[1] * s.x + e[5] * s.y + e[9] * s.z + e[13]) * w;
        total_w += w;
      }
      if (total_w > 0) low = Math.min(low, y / total_w);
    }
    return low;
  };
}
function skinned_positions(primitive, weights, rest3, posed) {
  rest3.armature.updateMatrixWorld(true);
  posed.armature.updateMatrixWorld(true);
  const skin = posed.bones.map((bone, i) => new Matrix42().multiplyMatrices(bone.matrixWorld, rest3.bones[i].matrixWorld.clone().invert()));
  const src = primitive.geometry.attributes.position.array;
  const out = new Float32Array(src.length);
  const v = new Vector315();
  const t = new Vector315();
  for (let i = 0; i < src.length / 3; i++) {
    let x = 0;
    let y = 0;
    let z2 = 0;
    let total = 0;
    for (let k = 0; k < 4; k++) {
      const w = weights.weights[i * 4 + k];
      if (w === 0) continue;
      t.set(src[i * 3], src[i * 3 + 1], src[i * 3 + 2]).applyMatrix4(skin[weights.indices[i * 4 + k]]);
      x += t.x * w;
      y += t.y * w;
      z2 += t.z * w;
      total += w;
    }
    if (total < 1e-6) {
      v.set(src[i * 3], src[i * 3 + 1], src[i * 3 + 2]);
    } else {
      v.set(x / total, y / total, z2 / total);
    }
    out[i * 3] = v.x;
    out[i * 3 + 1] = v.y;
    out[i * 3 + 2] = v.z;
  }
  return out;
}
var init_bind = __esm({
  "src/bind.ts"() {
    "use strict";
    init_rigger();
    init_skeleton();
  }
});

// src/animation.ts
import { readFileSync } from "node:fs";
import { Quaternion as Quaternion4, Vector3 as Vector316 } from "three";
function catalog() {
  catalog_cache ??= JSON.parse(readFileSync(asset_path("animations/catalog.json"), "utf8"));
  return catalog_cache;
}
function list_clips(skeleton, search) {
  const clips = catalog().skeletons[skeleton]?.clips ?? [];
  if (search === void 0 || search.trim() === "") return clips;
  const terms = search.toLowerCase().split(/[\s,]+/).filter((t) => t !== "");
  return clips.filter((c) => terms.some((t) => c.name.toLowerCase().replace(/[_-]/g, " ").includes(t.replace(/[_-]/g, " "))));
}
async function read_clip_file(file) {
  const io = await get_io();
  const doc = await io.read(asset_path("animations/" + file));
  const clips = [];
  for (const animation of doc.getRoot().listAnimations()) {
    const channels = [];
    let duration = 0;
    for (const channel of animation.listChannels()) {
      const node = channel.getTargetNode();
      const path = channel.getTargetPath();
      const sampler = channel.getSampler();
      const input = sampler?.getInput();
      const output = sampler?.getOutput();
      if (node === null || sampler === null || input == null || output == null) continue;
      if (path !== "rotation" && path !== "translation" && path !== "scale") continue;
      const times = Float32Array.from(input.getArray());
      const size = output.getElementSize();
      const values = new Float32Array(output.getCount() * size);
      const el = [];
      for (let i = 0; i < output.getCount(); i++) {
        output.getElement(i, el);
        for (let k = 0; k < size; k++) values[i * size + k] = el[k];
      }
      duration = Math.max(duration, times[times.length - 1] ?? 0);
      channels.push({ bone: node.getName(), path, interpolation: sampler.getInterpolation(), times, values });
    }
    clips.push({ name: animation.getName(), duration, channels });
  }
  return clips;
}
async function load_clips(skeleton, names) {
  const entries = catalog().skeletons[skeleton]?.clips ?? [];
  const wanted = names === "all" ? entries : names.map((name) => {
    const found = entries.find((c) => c.name === name) ?? entries.find((c) => c.name.toLowerCase() === name.toLowerCase());
    if (found === void 0) {
      throw new Error(`No animation named "${name}" for the ${skeleton} skeleton. rig_animations lists them.`);
    }
    return found;
  });
  const out = [];
  for (const entry of wanted) {
    let file = file_cache.get(entry.file);
    if (file === void 0) {
      file = read_clip_file(entry.file);
      file_cache.set(entry.file, file);
    }
    const clip = (await file).find((c) => c.name === entry.name);
    if (clip !== void 0) out.push(clip);
  }
  return out;
}
function lowest_joint_y(rig) {
  rig.armature.updateMatrixWorld(true);
  let lowest = Infinity;
  const p = new Vector316();
  for (const bone of rig.bones) {
    if (bone === rig.root) continue;
    lowest = Math.min(lowest, bone.getWorldPosition(p).y);
  }
  return lowest;
}
function ground_clip(clip, rig, lowest = lowest_joint_y) {
  if (clip.channels.some((c) => c.bone === rig.root.name && c.path === "translation")) return clip;
  const rest_low = lowest(rig);
  const rest_root = rig.root.position.clone();
  const times = [...new Set(clip.channels.flatMap((c) => Array.from(c.times)))].sort((a, b) => a - b);
  const step = Math.max(1, Math.ceil(times.length / 240));
  const sampled = times.filter((_, i) => i % step === 0 || i === times.length - 1);
  const parent = rig.root.parent;
  const values = new Float32Array(sampled.length * 3);
  sampled.forEach((t, i) => {
    apply_clip(rig, clip, t);
    const lift = rest_low - lowest(rig);
    parent.updateWorldMatrix(true, false);
    const local = parent.worldToLocal(parent.localToWorld(rest_root.clone()).add(new Vector316(0, lift, 0)));
    values[i * 3] = local.x;
    values[i * 3 + 1] = local.y;
    values[i * 3 + 2] = local.z;
  });
  return {
    ...clip,
    channels: [...clip.channels, { bone: rig.root.name, path: "translation", interpolation: "LINEAR", times: Float32Array.from(sampled), values }]
  };
}
function fit_clip(clip, template, rig, joints, options = {}) {
  const scale = position_scale(template, joints);
  const root_motion = clip.name.toLowerCase().endsWith("rm");
  const channels = [];
  for (const channel of clip.channels) {
    if (!rig.by_name.has(channel.bone)) continue;
    if (channel.path === "rotation") {
      channels.push(arm_spread(channel, options.arm_spread_degrees ?? 0));
    } else if (channel.path === "translation") {
      const keep = channel.bone === template.tracking_bone || root_motion && channel.bone === template.root.name;
      if (!keep) continue;
      channels.push({ ...channel, values: channel.values.map((v) => v * scale) });
    }
  }
  return { name: clip.name, duration: clip.duration, channels };
}
function position_scale(template, joints) {
  const bone = template.tracking_bone;
  const parent = template.parents.get(bone);
  if (parent === void 0) return 1;
  const t = template.positions.get(bone).distanceTo(template.positions.get(parent));
  const j = joints.get(bone)?.distanceTo(joints.get(parent) ?? new Vector316());
  if (j === void 0 || t < 1e-9) return 1;
  const s = j / t;
  return Number.isFinite(s) && s > 0 ? s : 1;
}
function arm_spread(channel, degrees) {
  if (degrees === 0) return channel;
  const side = channel.bone.includes("upperarm_l") ? -1 : channel.bone.includes("upperarm_r") ? 1 : 0;
  if (side === 0) return channel;
  const turn = new Quaternion4().setFromAxisAngle(new Vector316(0, 0, side), degrees * Math.PI / 180);
  const values = channel.values.slice();
  const q = new Quaternion4();
  for (let i = 0; i + 3 < values.length; i += 4) {
    q.set(values[i], values[i + 1], values[i + 2], values[i + 3]).multiply(turn);
    values[i] = q.x;
    values[i + 1] = q.y;
    values[i + 2] = q.z;
    values[i + 3] = q.w;
  }
  return { ...channel, values };
}
function apply_clip(rig, clip, time) {
  const t = clip.duration > 0 ? (time % clip.duration + clip.duration) % clip.duration : 0;
  for (const channel of clip.channels) {
    const bone = rig.by_name.get(channel.bone);
    if (bone === void 0) continue;
    const size = channel.path === "rotation" ? 4 : 3;
    const sample = sample_channel(channel, t, size);
    if (channel.path === "rotation") bone.quaternion.set(sample[0], sample[1], sample[2], sample[3]).normalize();
    else if (channel.path === "translation") bone.position.set(sample[0], sample[1], sample[2]);
    else bone.scale.set(sample[0], sample[1], sample[2]);
  }
  rig.armature.updateMatrixWorld(true);
}
function sample_channel(channel, t, size) {
  const { times, values } = channel;
  const cubic = channel.interpolation === "CUBICSPLINE";
  const stride = cubic ? size * 3 : size;
  const value_at = (k2) => {
    const base = k2 * stride + (cubic ? size : 0);
    return Array.from(values.subarray(base, base + size));
  };
  if (times.length === 0) return new Array(size).fill(0);
  if (t <= times[0]) return value_at(0);
  const last = times.length - 1;
  if (t >= times[last]) return value_at(last);
  let k = 0;
  while (k < last && times[k + 1] < t) k++;
  const a = value_at(k);
  if (channel.interpolation === "STEP") return a;
  const b = value_at(k + 1);
  const f = (t - times[k]) / Math.max(times[k + 1] - times[k], 1e-9);
  if (size === 4) {
    qa.set(a[0], a[1], a[2], a[3]);
    qb.set(b[0], b[1], b[2], b[3]);
    qa.slerp(qb, f);
    return [qa.x, qa.y, qa.z, qa.w];
  }
  return a.map((v, i) => v + (b[i] - v) * f);
}
var catalog_cache, file_cache, qa, qb;
var init_animation = __esm({
  "src/animation.ts"() {
    "use strict";
    init_io();
    init_assets();
    catalog_cache = null;
    file_cache = /* @__PURE__ */ new Map();
    qa = new Quaternion4();
    qb = new Quaternion4();
  }
});

// src/export.ts
import { writeFileSync } from "node:fs";
import { extname } from "node:path";
import { PropertyType } from "@gltf-transform/core";
import { prune } from "@gltf-transform/functions";
import { Matrix4 as Matrix43, Vector3 as Vector317 } from "three";
async function write_rigged_model(model, rig, binding, clips, output, drop_excluded = false) {
  const doc = model.doc;
  const root = doc.getRoot();
  if (drop_excluded) {
    const excluded = new Set(model.meshes.filter((m) => m.excluded).map((m) => m.id));
    const scene_nodes = [];
    (root.getDefaultScene() ?? root.listScenes()[0])?.traverse((n) => {
      if (n.getMesh() !== null) scene_nodes.push(n);
    });
    scene_nodes.forEach((node, id) => {
      if (excluded.has(id)) node.setMesh(null);
    });
  }
  const buffer = root.listBuffers()[0] ?? doc.createBuffer();
  const scene = root.getDefaultScene() ?? root.listScenes()[0] ?? doc.createScene("Scene");
  if (root.getDefaultScene() === null) root.setDefaultScene(scene);
  const original_nodes = root.listNodes();
  const replaced_animations = root.listAnimations().map((a) => a.getName());
  const old_joints = new Set(root.listSkins().flatMap((skin2) => skin2.listJoints()));
  for (const node of root.listNodes()) node.setSkin(null);
  for (const skin2 of root.listSkins()) skin2.dispose();
  for (const animation of root.listAnimations()) {
    for (const channel of animation.listChannels()) channel.dispose();
    for (const sampler of animation.listSamplers()) sampler.dispose();
    animation.dispose();
  }
  for (const joint of old_joints) {
    let has_mesh = false;
    joint.traverse((n) => {
      if (n.getMesh() !== null) has_mesh = true;
    });
    if (!has_mesh) joint.dispose();
  }
  const nodes = /* @__PURE__ */ new Map();
  const add = (object, parent) => {
    const q = object.quaternion.clone().normalize();
    const unit = (n) => Math.max(-1, Math.min(1, n));
    const node = doc.createNode(object.name).setTranslation([object.position.x, object.position.y, object.position.z]).setRotation([unit(q.x), unit(q.y), unit(q.z), unit(q.w)]).setScale([object.scale.x, object.scale.y, object.scale.z]);
    if (object.isBone === true) nodes.set(object.name, node);
    if (parent === null) scene.addChild(node);
    else parent.addChild(node);
    for (const child of object.children) add(child, node);
  };
  rig.armature.updateMatrixWorld(true);
  add(rig.armature, null);
  const joints = rig.bones.map((b) => nodes.get(b.name));
  const inverse_binds = new Float32Array(rig.bones.length * 16);
  rig.bones.forEach((bone, i) => {
    new Matrix43().copy(bone.matrixWorld).invert().toArray(inverse_binds, i * 16);
  });
  const skin = doc.createSkin("Skin").setSkeleton(nodes.get(rig.root.name)).setInverseBindMatrices(doc.createAccessor("inverseBindMatrices", buffer).setType("MAT4").setArray(inverse_binds));
  for (const joint of joints) skin.addJoint(joint);
  const joint_type = rig.bones.length > 255 ? Uint16Array : Uint8Array;
  const mesh_for_node = /* @__PURE__ */ new Map();
  let skinned = 0;
  model.primitives.forEach((baked, i) => {
    let mesh = mesh_for_node.get(baked.node);
    if (mesh === void 0) {
      const source = baked.node.getMesh();
      mesh = doc.createMesh(source.getName());
      const weights = source.getWeights();
      if (weights.length > 0) mesh.setWeights(weights);
      mesh_for_node.set(baked.node, mesh);
      const node = doc.createNode(baked.node.getName() !== "" ? baked.node.getName() : source.getName()).setMesh(mesh).setSkin(skin);
      scene.addChild(node);
      skinned++;
    }
    mesh.addPrimitive(skinned_primitive(
      doc,
      buffer,
      baked.primitive,
      baked.matrix,
      baked.geometry.attributes.position.array,
      baked.geometry.index.array,
      baked.geometry.attributes.normal?.array,
      binding.weights[i].indices,
      binding.weights[i].weights,
      joint_type
    ));
  });
  for (const node of mesh_for_node.keys()) node.setMesh(null);
  const keeps = (node) => node.getMesh() !== null || node.getCamera() !== null || node.getExtension("KHR_lights_punctual") !== null;
  for (const node of original_nodes) {
    if (node.isDisposed()) continue;
    let used = false;
    node.traverse((n) => {
      if (keeps(n)) used = true;
    });
    if (!used) node.dispose();
  }
  for (const clip of clips) {
    const animation = doc.createAnimation(clip.name);
    for (const channel of clip.channels) {
      const target = nodes.get(channel.bone);
      if (target === void 0) continue;
      const sampler = doc.createAnimationSampler().setInput(doc.createAccessor(void 0, buffer).setType("SCALAR").setArray(channel.times.slice())).setOutput(doc.createAccessor(void 0, buffer).setType(channel.path === "rotation" ? "VEC4" : "VEC3").setArray(channel.values.slice())).setInterpolation(channel.interpolation);
      animation.addSampler(sampler);
      animation.addChannel(doc.createAnimationChannel().setTargetNode(target).setTargetPath(channel.path).setSampler(sampler));
    }
  }
  for (const extension of root.listExtensionsUsed()) {
    if (["KHR_draco_mesh_compression", "EXT_meshopt_compression", "EXT_mesh_gpu_instancing"].includes(extension.extensionName)) {
      extension.dispose();
    }
  }
  await doc.transform(prune({
    propertyTypes: [PropertyType.ACCESSOR, PropertyType.MESH, PropertyType.PRIMITIVE, PropertyType.PRIMITIVE_TARGET, PropertyType.SKIN, PropertyType.BUFFER],
    keepLeaves: true,
    keepAttributes: true
  }));
  const io = await get_io();
  let bytes;
  if (extname(output).toLowerCase() === ".gltf") {
    await io.write(output, doc);
    bytes = 0;
  } else {
    const data = await io.writeBinary(doc);
    writeFileSync(output, data);
    bytes = data.byteLength;
  }
  return { path: output, bytes, bones: joints.length, skinned_meshes: skinned, animations: clips.map((c) => c.name), replaced_animations };
}
function skinned_primitive(doc, buffer, source, matrix, positions, indices, normals, joint_indices, joint_weights, joint_type) {
  const primitive = doc.createPrimitive().setMode(source.getMode()).setMaterial(source.getMaterial());
  for (const semantic of source.listSemantics()) {
    if (["POSITION", "NORMAL", "TANGENT", "JOINTS_0", "WEIGHTS_0", "JOINTS_1", "WEIGHTS_1"].includes(semantic)) continue;
    primitive.setAttribute(semantic, source.getAttribute(semantic));
  }
  primitive.setAttribute("POSITION", doc.createAccessor(void 0, buffer).setType("VEC3").setArray(new Float32Array(positions)));
  if (normals !== void 0) primitive.setAttribute("NORMAL", doc.createAccessor(void 0, buffer).setType("VEC3").setArray(new Float32Array(normals)));
  const tangent = source.getAttribute("TANGENT");
  if (tangent !== null) primitive.setAttribute("TANGENT", transformed_tangents(doc, buffer, tangent, matrix));
  const count = positions.length / 3;
  const index_array = count > 65535 ? Uint32Array.from(indices) : Uint16Array.from(indices);
  primitive.setIndices(doc.createAccessor(void 0, buffer).setType("SCALAR").setArray(index_array));
  const joints_clean = joint_type.from(joint_indices);
  for (let i = 0; i < joints_clean.length; i++) if (!(joint_weights[i] > 0)) joints_clean[i] = 0;
  primitive.setAttribute("JOINTS_0", doc.createAccessor(void 0, buffer).setType("VEC4").setArray(joints_clean));
  primitive.setAttribute("WEIGHTS_0", doc.createAccessor(void 0, buffer).setType("VEC4").setArray(normalized_weights(joint_weights)));
  const linear = new Matrix43().extractRotation(matrix);
  const scale = new Vector317().setFromMatrixScale(matrix);
  linear.scale(scale);
  for (const target of source.listTargets()) {
    const copy = doc.createPrimitiveTarget(target.getName());
    for (const semantic of target.listSemantics()) {
      const accessor = target.getAttribute(semantic);
      if (semantic === "POSITION" || semantic === "NORMAL") {
        copy.setAttribute(semantic, transformed_vectors(doc, buffer, accessor, semantic === "POSITION" ? linear : new Matrix43().copy(matrix).invert().transpose()));
      } else {
        copy.setAttribute(semantic, accessor);
      }
    }
    primitive.addTarget(copy);
  }
  return primitive;
}
function transformed_vectors(doc, buffer, accessor, m) {
  const out = new Float32Array(accessor.getCount() * 3);
  const el = [];
  const v = new Vector317();
  for (let i = 0; i < accessor.getCount(); i++) {
    accessor.getElement(i, el);
    v.set(el[0], el[1], el[2]).applyMatrix4(new Matrix43().copy(m).setPosition(0, 0, 0));
    out[i * 3] = v.x;
    out[i * 3 + 1] = v.y;
    out[i * 3 + 2] = v.z;
  }
  return doc.createAccessor(void 0, buffer).setType("VEC3").setArray(out);
}
function transformed_tangents(doc, buffer, accessor, matrix) {
  const out = new Float32Array(accessor.getCount() * 4);
  const el = [];
  const v = new Vector317();
  const flip = matrix.determinant() < 0 ? -1 : 1;
  for (let i = 0; i < accessor.getCount(); i++) {
    accessor.getElement(i, el);
    v.set(el[0], el[1], el[2]).transformDirection(matrix);
    out[i * 4] = v.x;
    out[i * 4 + 1] = v.y;
    out[i * 4 + 2] = v.z;
    out[i * 4 + 3] = (el[3] ?? 1) * flip;
  }
  return doc.createAccessor(void 0, buffer).setType("VEC4").setArray(out);
}
function normalized_weights(weights) {
  const out = new Float32Array(weights.length);
  for (let v = 0; v < weights.length / 4; v++) {
    const sum = weights[v * 4] + weights[v * 4 + 1] + weights[v * 4 + 2] + weights[v * 4 + 3];
    if (sum < 1e-8) {
      out[v * 4] = 1;
      continue;
    }
    for (let k = 0; k < 4; k++) out[v * 4 + k] = weights[v * 4 + k] / sum;
  }
  return out;
}
var init_export = __esm({
  "src/export.ts"() {
    "use strict";
    init_io();
  }
});

// src/session.ts
import { existsSync, readFileSync as readFileSync2, writeFileSync as writeFileSync2 } from "node:fs";
import { basename, dirname, extname as extname2, join, resolve as resolve2 } from "node:path";
import { Matrix4 as Matrix44, Quaternion as Quaternion5, Vector3 as Vector318 } from "three";
function mirror_name(name) {
  const match = /^(.*[_.])([lLrR])$/.exec(name);
  if (match === null) return void 0;
  const swap = { l: "r", r: "l", L: "R", R: "L" };
  return match[1] + swap[match[2]];
}
function weight_colors(index, weights, bone) {
  const out = new Uint8Array(index.length / 3 * 3);
  for (let t = 0; t < index.length / 3; t++) {
    if (bone >= 0) {
      let w = 0;
      for (let c = 0; c < 3; c++) {
        const v2 = index[t * 3 + c];
        for (let k = 0; k < 4; k++) if (weights.indices[v2 * 4 + k] === bone) w += weights.weights[v2 * 4 + k];
      }
      w /= 3;
      out[t * 3] = 40 + 215 * w;
      out[t * 3 + 1] = 60 + 40 * (1 - Math.abs(w - 0.5) * 2);
      out[t * 3 + 2] = 40 + 215 * (1 - w);
      continue;
    }
    const v = index[t * 3];
    let best = 0;
    let best_w = -1;
    for (let k = 0; k < 4; k++) {
      if (weights.weights[v * 4 + k] > best_w) {
        best_w = weights.weights[v * 4 + k];
        best = weights.indices[v * 4 + k];
      }
    }
    const [r, g, b] = bone_color(best);
    out[t * 3] = r;
    out[t * 3 + 1] = g;
    out[t * 3 + 2] = b;
  }
  return out;
}
function bone_color(i) {
  const hue = i * 0.618033988749895 % 1;
  const s = 0.65;
  const l = 0.58;
  const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
  const p = 2 * l - q;
  const channel = (t) => {
    t = (t + 1) % 1;
    if (t < 1 / 6) return p + (q - p) * 6 * t;
    if (t < 1 / 2) return q;
    if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6;
    return p;
  };
  return [channel(hue + 1 / 3) * 255, channel(hue) * 255, channel(hue - 1 / 3) * 255];
}
function model_file(project_path, state) {
  return resolve2(dirname(project_path), state.model);
}
var HISTORY_LIMIT, RigSession;
var init_session = __esm({
  "src/session.ts"() {
    "use strict";
    init_model();
    init_skeleton();
    init_fit();
    init_inspect();
    init_render();
    init_bind();
    init_animation();
    init_export();
    init_util();
    HISTORY_LIMIT = 30;
    RigSession = class _RigSession {
      project_path;
      model;
      template;
      state;
      bind_cache = null;
      constructor(project_path, model, template, state) {
        this.project_path = project_path;
        this.model = model;
        this.template = template;
        this.state = state;
      }
      static default_project_path(model) {
        const full = resolve2(model);
        return join(dirname(full), basename(full, extname2(full)) + ".afk-rig.json");
      }
      static async start(options) {
        const model_path = resolve2(options.model);
        if (!existsSync(model_path)) throw new Error(`Model not found: ${model_path}`);
        const skeleton = parse_skeleton(options.skeleton);
        const hands = options.hands ?? "all-fingers";
        if (!HAND_OPTIONS.includes(hands)) throw new Error(`hands must be one of ${HAND_OPTIONS.join(", ")}`);
        const project_path = resolve2(options.project ?? _RigSession.default_project_path(model_path));
        const model = await load_model(model_path);
        const template = await load_template(skeleton, hands);
        const state = { afk_rig: 1, model: model_path, skeleton, hands, joints: {}, history: [], notes: [] };
        const session = new _RigSession(project_path, model, template, state);
        session.fit(options.fit === false ? "template" : "auto");
        session.state.history = [];
        session.save();
        return session;
      }
      static async open(project_path) {
        const full = resolve2(project_path);
        if (!existsSync(full)) throw new Error(`No project at ${full}. Start one with rig_start / afk-rig start.`);
        const state = JSON.parse(readFileSync2(full, "utf8"));
        const matrix = state.model_transform !== void 0 ? new Matrix44().fromArray(state.model_transform) : new Matrix44();
        const model = await load_model(model_file(full, state), matrix, new Set(state.excluded_meshes ?? []));
        const template = await load_template(parse_skeleton(state.skeleton), state.hands ?? "all-fingers");
        return new _RigSession(full, model, template, state);
      }
      save() {
        writeFileSync2(this.project_path, JSON.stringify(this.state, null, 1));
      }
      // ---------------------------------------------------------------- joints
      joints() {
        return new Map(Object.entries(this.state.joints).map(([k, v]) => [k, new Vector318(v[0], v[1], v[2])]));
      }
      joint_names() {
        return this.template.bones.map((b) => b.name);
      }
      commit(joints) {
        this.state.history.push(this.state.joints);
        if (this.state.history.length > HISTORY_LIMIT) this.state.history.shift();
        this.state.joints = Object.fromEntries([...joints].map(([k, v]) => [k, vec(v)]));
        this.bind_cache = null;
        this.save();
      }
      /** auto: the deterministic fit; template: the template scaled over the model */
      fit(mode = "auto", only) {
        const result = mode === "auto" ? auto_fit(this.model.triangles, this.model.min, this.model.max, this.template) : { joints: template_on_model(this.template, this.model.min, this.model.max), notes: ["Template scaled over the model, no fitting."], landmarks: void 0 };
        const joints = only === void 0 ? result.joints : this.joints();
        if (only !== void 0) {
          for (const name of this.check_names(only)) joints.set(name, result.joints.get(name).clone());
        }
        this.state.notes = result.notes;
        if (result.landmarks !== void 0) this.state.landmarks = result.landmarks;
        this.commit(joints);
        return result.notes;
      }
      check_names(names) {
        const known = new Set(this.joint_names());
        for (const name of names) {
          if (!known.has(name)) {
            const close = this.joint_names().filter((n) => n.includes(name) || name.includes(n)).slice(0, 8);
            throw new Error(`Unknown joint "${name}".${close.length > 0 ? " Did you mean: " + close.join(", ") + "?" : ""} rig_status lists every joint.`);
          }
        }
        return names;
      }
      /**
       * Place joints. Values are absolute positions, or offsets when relative is true.
       * mirror also sets each joint's left/right partner, reflected across mirror_x
       * (default: the x of the pelvis/hips). with_children moves everything below a joint along with it.
       */
      set_joints(updates, options = {}) {
        this.check_names(Object.keys(updates));
        const joints = this.joints();
        const center_x = options.mirror_x ?? joints.get(this.template.tracking_bone)?.x ?? (this.model.min.x + this.model.max.x) / 2;
        const apply = (name, value, relative) => {
          const current = joints.get(name);
          const target = relative ? current.clone().add(new Vector318(...value)) : new Vector318(...value);
          const delta = target.clone().sub(current);
          if (options.with_children === true) {
            for (const d of this.descendants(name)) joints.get(d).add(delta);
          }
          current.copy(target);
        };
        const changed = /* @__PURE__ */ new Set();
        const touch = (name) => {
          changed.add(name);
          if (options.with_children === true) for (const d of this.descendants(name)) changed.add(d);
        };
        for (const [name, value] of Object.entries(updates)) {
          apply(name, value, options.relative === true);
          touch(name);
          if (options.mirror === true) {
            const partner = mirror_name(name);
            if (partner !== void 0 && joints.has(partner) && updates[partner] === void 0) {
              const placed = joints.get(name);
              apply(partner, [2 * center_x - placed.x, placed.y, placed.z], false);
              touch(partner);
            }
          }
        }
        this.commit(joints);
        return [...changed].map((name) => ({ name, position: vec(joints.get(name)) }));
      }
      /**
       * Point a bone somewhere: turn everything below `joint` around it so the bone toward
       * `child` (default: the bone's own child) points at `target`. stretch also scales the
       * chain so the child lands on the target. For posing whole limbs, hands and tails at once.
       */
      aim(joint, target, options = {}) {
        this.check_names([joint, ...options.child !== void 0 ? [options.child] : []]);
        const joints = this.joints();
        const child = options.child ?? primary_child(this.template, joint) ?? [...this.template.parents].find(([, parent]) => parent === joint)?.[0];
        if (child === void 0) throw new Error(`${joint} has no child joint to aim.`);
        if (!this.descendants(joint).includes(child)) throw new Error(`${child} is not below ${joint}.`);
        const origin = joints.get(joint);
        const from = joints.get(child).clone().sub(origin);
        const to = new Vector318(...target).sub(origin);
        if (from.lengthSq() < 1e-18 || to.lengthSq() < 1e-18) throw new Error("The target is on top of the joint.");
        const turn = new Quaternion5().setFromUnitVectors(from.clone().normalize(), to.clone().normalize());
        const scale = options.stretch === true ? to.length() / from.length() : 1;
        return this.move_subtree(joint, joints, (p) => p.sub(origin).applyQuaternion(turn).multiplyScalar(scale).add(origin));
      }
      /** turn everything below `joint` around it, by degrees about an axis (world space) */
      rotate(joint, axis, degrees) {
        this.check_names([joint]);
        const joints = this.joints();
        const origin = joints.get(joint);
        const a = new Vector318(...axis);
        if (a.lengthSq() < 1e-18) throw new Error("The axis needs a direction, like [0, 0, 1].");
        const turn = new Quaternion5().setFromAxisAngle(a.normalize(), degrees * Math.PI / 180);
        return this.move_subtree(joint, joints, (p) => p.sub(origin).applyQuaternion(turn).add(origin));
      }
      move_subtree(joint, joints, move) {
        const below = this.descendants(joint);
        for (const name of below) move(joints.get(name));
        this.commit(joints);
        return below.map((name) => ({ name, position: vec(joints.get(name)) }));
      }
      descendants(name) {
        const out = [];
        for (const [child, parent] of this.template.parents) {
          if (parent === name) out.push(child, ...this.descendants(child));
        }
        return out;
      }
      undo(steps = 1) {
        let undone = 0;
        while (undone < steps && this.state.history.length > 0) {
          this.state.joints = this.state.history.pop();
          undone++;
        }
        this.bind_cache = null;
        this.save();
        return undone;
      }
      model_matrix() {
        return this.state.model_transform !== void 0 ? new Matrix44().fromArray(this.state.model_transform) : new Matrix44();
      }
      /**
       * Leave meshes out of fitting and skinning (floors, props, weapons), or bring them back.
       * Meshes are named by id or name from status().meshes. Excluded meshes stay in the
       * exported file as they are, unless the export drops them.
       */
      async set_excluded_meshes(exclude = [], include = []) {
        const resolve_id = (key) => {
          const found = this.model.meshes.find((m) => m.id === key || m.name === key || String(m.id) === String(key));
          if (found === void 0) throw new Error(`No mesh "${key}". status lists meshes with their ids.`);
          return found.id;
        };
        const set = new Set(this.state.excluded_meshes ?? []);
        for (const key of exclude) set.add(resolve_id(key));
        for (const key of include) set.delete(resolve_id(key));
        this.state.excluded_meshes = [...set].sort((a, b) => a - b);
        this.model = await load_model(model_file(this.project_path, this.state), this.model_matrix(), set);
        this.bind_cache = null;
        this.save();
      }
      /** turn, scale or move the model; joints move with it so they stay where they were on the mesh */
      async transform_model(transform) {
        const step = transform_matrix(transform);
        const current = this.state.model_transform !== void 0 ? new Matrix44().fromArray(this.state.model_transform) : new Matrix44();
        const combined = new Matrix44().multiplyMatrices(step, current);
        this.state.model_transform = combined.toArray();
        this.model = await load_model(model_file(this.project_path, this.state), combined, new Set(this.state.excluded_meshes ?? []));
        const joints = this.joints();
        for (const p of joints.values()) p.applyMatrix4(step);
        this.commit(joints);
      }
      // ---------------------------------------------------------------- reading
      status() {
        const size = this.model.max.clone().sub(this.model.min);
        const joints = this.joints();
        return {
          project: this.project_path,
          model: this.model.info,
          skeleton: this.state.skeleton,
          hands: this.state.hands,
          model_bounds: { min: vec(this.model.min), max: vec(this.model.max), size: vec(size) },
          meshes: this.model.meshes,
          model_transform_applied: this.state.model_transform !== void 0,
          fit_notes: this.state.notes,
          weight_rules: this.state.weight_rules ?? [],
          bind_options: this.state.bind_options ?? {},
          landmarks: this.state.landmarks,
          undo_steps_available: this.state.history.length,
          joints: this.joint_names().map((name) => ({
            name,
            parent: this.template.parents.get(name) ?? null,
            side: side_of(name),
            position: joints.has(name) ? vec(joints.get(name)) : null
          }))
        };
      }
      inspect(names) {
        if (names !== void 0) this.check_names(names);
        return joint_reports(this.model.triangles, this.joints(), this.template, names);
      }
      /** only the joints that look off, with reasons */
      issues(names) {
        return flag_issues(this.inspect(names), this.model.max.y - this.model.min.y, names !== void 0);
      }
      slice(axis, at, thickness) {
        return slice(this.model.triangles, axis, at, thickness);
      }
      ray(origin, direction) {
        return raycast(this.model.triangles, new Vector318(...origin), new Vector318(...direction)).map((h) => ({ distance: num(h.distance), point: vec(h.point) }));
      }
      // ---------------------------------------------------------------- binding
      /** solver settings saved with the project, with any given ones on top */
      bind_settings(options = {}) {
        const merged = { ...this.state.bind_options ?? {} };
        for (const [k, v] of Object.entries(options)) if (v !== void 0) merged[k] = v;
        return merged;
      }
      bind(given = {}, rest3 = this.rest()) {
        const options = this.bind_settings(given);
        const key = JSON.stringify([this.state.joints, options, rest3, this.state.model_transform, this.state.excluded_meshes, this.state.weight_rules]);
        if (this.bind_cache?.key === key) return this.bind_cache.result;
        const rig = build_rig(this.template, this.joints(), rest3);
        const result = bind(this.model.primitives, rig, this.template.type, options);
        this.rule_counts = apply_weight_rules(result, this.model.primitives, rig, this.state.weight_rules ?? []);
        this.bind_cache = { key, result };
        return result;
      }
      rule_counts = [];
      /** bind with these solver settings and keep them for previews and export */
      /** the rest rotations to use: given, else saved with the project, else limbs */
      rest(given) {
        return given ?? this.state.rest_rotations ?? "limbs";
      }
      bind_report(options = {}, rest_given) {
        const { reset, ...given } = options;
        this.state.bind_options = reset === true ? {} : this.bind_settings(given);
        if (reset === true) delete this.state.rest_rotations;
        else if (rest_given !== void 0) this.state.rest_rotations = rest_given;
        this.save();
        const stats = bind_stats(this.bind({}, this.rest(rest_given)));
        return { ...stats, bind_options: this.state.bind_options, weight_rules: (this.state.weight_rules ?? []).map((rule, i) => ({ ...rule, vertices_changed: this.rule_counts[i] ?? 0 })) };
      }
      /** add, remove or clear skin weight rules; they apply on every bind and export */
      set_weight_rules(changes) {
        let rules = changes.clear === true ? [] : [...this.state.weight_rules ?? []];
        if (changes.remove !== void 0) rules = rules.filter((_, i) => !changes.remove.includes(i));
        const rig = build_rig(this.template, this.joints());
        for (const rule of changes.add ?? []) {
          if (rule.mode !== "only" && rule.mode !== "never") throw new Error(`A weight rule's mode is "only" or "never".`);
          if (!Array.isArray(rule.bones) || rule.bones.length === 0) throw new Error("A weight rule needs at least one bone.");
          expand_bones(rule.bones, rig);
          rules.push(rule);
        }
        this.state.weight_rules = rules;
        this.bind_cache = null;
        this.save();
        return rules;
      }
      // ---------------------------------------------------------------- pictures
      async render(options = {}) {
        const views = (options.views ?? ["front", "left"]).map((v) => {
          if (!VIEW_NAMES.includes(v)) throw new Error(`Unknown view "${v}". Views: ${VIEW_NAMES.join(", ")}`);
          return v;
        });
        let joints = this.joints();
        let meshes = this.model.primitives.map((p) => ({
          positions: p.geometry.attributes.position.array,
          index: p.geometry.index.array
        }));
        let pose;
        if (options.animation !== void 0) {
          const rest3 = this.rest(options.rest_rotations);
          const binding = this.bind({}, rest3);
          const rest_rig = build_rig(this.template, this.joints(), rest3);
          const posed = build_rig(this.template, this.joints(), rest3);
          const [clip] = await load_clips(this.state.skeleton, [options.animation]);
          let fitted = fit_clip(clip, this.template, posed, this.joints(), { arm_spread_degrees: options.arm_spread_degrees });
          if (options.ground === true) {
            fitted = ground_clip(fitted, build_rig(this.template, this.joints(), rest3), lowest_skinned_point(this.model.primitives, binding, rest_rig));
          }
          const time = options.time ?? clip.duration / 2;
          apply_clip(posed, fitted, time);
          meshes = this.model.primitives.map((p, i) => ({
            positions: skinned_positions(p, binding.weights[i], rest_rig, posed),
            index: p.geometry.index.array
          }));
          joints = new Map(posed.bones.map((b) => [b.name, b.getWorldPosition(new Vector318())]));
          let lowest = Infinity;
          for (const layer of meshes) for (let i = 1; i < layer.positions.length; i += 3) lowest = Math.min(lowest, layer.positions[i]);
          pose = {
            animation: clip.name,
            time: num(time),
            duration: num(clip.duration),
            rest_rotations: rest3,
            grounded: options.ground === true,
            position_scale: num(position_scale(this.template, this.joints())),
            // positive: the model floats above where it stood at rest; negative: it sinks below
            lowest_point_vs_rest_floor: num(lowest - this.model.min.y)
          };
        }
        let legend;
        if (options.weights === true || options.bone !== void 0) {
          const binding = this.bind({}, this.rest(options.rest_rotations));
          const bone_index = options.bone !== void 0 ? binding.bone_names.indexOf(this.check_names([options.bone])[0]) : -1;
          meshes = meshes.map((layer, i) => ({ ...layer, triangle_colors: weight_colors(layer.index, binding.weights[i], bone_index) }));
          if (bone_index < 0) {
            const used = Object.keys(bind_stats(binding).vertices_per_bone);
            legend = Object.fromEntries(used.map((name) => [name, "#" + bone_color(binding.bone_names.indexOf(name)).map((c) => Math.round(c).toString(16).padStart(2, "0")).join("")]));
          } else {
            legend = { scale: "blue = not moved by " + options.bone + ", red = moved fully" };
          }
        }
        const height = Math.max(this.model.max.y - this.model.min.y, 1e-9);
        let focus;
        if (options.focus !== void 0) {
          const center = typeof options.focus === "string" ? joints.get(this.check_names([options.focus])[0]) : new Vector318(...options.focus);
          focus = { center, radius: options.radius ?? height * 0.15 };
        }
        const pick = (selection3, fallback) => {
          const s = selection3 ?? fallback;
          if (s === "all") return new Set(joints.keys());
          if (s === "none") return /* @__PURE__ */ new Set();
          if (s === "main") return new Set([...joints.keys()].filter((n) => !is_minor_joint(n)));
          return new Set(this.check_names(s));
        };
        const result = render_views({
          meshes,
          joints,
          parents: this.template.parents,
          views,
          size: options.size ?? 640,
          focus,
          draw: pick(options.joints, "all"),
          label: pick(options.labels, focus !== void 0 ? "all" : "main"),
          xray: options.xray,
          markers: options.markers?.map((m) => ({ position: new Vector318(...m.position), label: m.label })),
          title: pose !== void 0 ? `${String(pose.animation)} ${Number(pose.time).toFixed(2)}S` : void 0
        });
        return { ...result, ...pose !== void 0 ? { pose } : {}, ...legend !== void 0 ? { weight_colors: legend } : {} };
      }
      // ---------------------------------------------------------------- export
      async export(options) {
        const rest3 = this.rest(options.rest_rotations);
        const bind_options = {
          head_weight_correction_height: options.head_weight_correction_height,
          arm_plane_correction_offset: options.arm_plane_correction_offset
        };
        const binding = this.bind(bind_options, rest3);
        const rig = build_rig(this.template, this.joints(), rest3);
        const names = options.animations ?? [];
        const clips = names === "all" || names.length > 0 ? await load_clips(this.state.skeleton, names) : [];
        const lowest = lowest_skinned_point(this.model.primitives, binding, rig);
        const fitted = clips.map((c) => {
          const clip = fit_clip(c, this.template, rig, this.joints(), options);
          return options.ground === true ? ground_clip(clip, build_rig(this.template, this.joints(), rest3), lowest) : clip;
        });
        const rest_low = lowest(rig);
        const floor_check = fitted.map((clip) => {
          const posed = build_rig(this.template, this.joints(), rest3);
          let low = Infinity;
          let high = -Infinity;
          for (let k = 0; k <= 16; k++) {
            apply_clip(posed, clip, clip.duration * k / 16);
            const gap = lowest(posed) - rest_low;
            low = Math.min(low, gap);
            high = Math.max(high, gap);
          }
          return { animation: clip.name, lowest_point_min: num(low), lowest_point_max: num(high) };
        });
        const fresh = await load_model(model_file(this.project_path, this.state), this.model_matrix(), new Set(this.state.excluded_meshes ?? []));
        const result = await write_rigged_model(fresh, rig, binding, fitted, resolve2(options.output), options.drop_excluded_meshes === true);
        return {
          ...result,
          floor_check,
          floor_check_note: "Lowest point of the model relative to where it stands at rest, over each clip: positive floats, negative sinks. export with ground: true keeps it at 0 (not wanted for jumps).",
          position_scale: num(position_scale(this.template, this.joints())),
          position_scale_note: "The animations' hip movement (bob, sway, root motion) was scaled by position_scale to match this rig's size."
        };
      }
      animations(search) {
        return list_clips(this.state.skeleton, search);
      }
    };
  }
});

// src/guide.ts
var GUIDE;
var init_guide = __esm({
  "src/guide.ts"() {
    "use strict";
    GUIDE = `afk-rig rigs a GLB/glTF model with one of the afk.ai skeletons and exports it with
animations from a library of 250+ clips. Everything runs locally.

How it usually goes: start a project (it runs a deterministic auto-fit), look at renders,
measure, move joints until you're happy, then export. How far to take it is your call.

Coordinates
- Model units, glTF axes: +Y up. Characters are expected to face +Z, with their left side
  toward +X. Joint names ending in _l / _r (or _L / _R) are the character's left / right.
- Renders are orthographic. FRONT looks from +Z (so the character's left is on the image's
  right), LEFT looks at the character's left side from +X, TOP looks down from +Y.
  Rulers on the edges are in model units, and the response lists every joint's pixel position.
- Colors: blue = left joints, red = right, orange = center.

What's available
- start: load a model, pick a skeleton (human, fox, horse, bird, dragon, kaiju, spider, snake,
  fish), auto-fit. status: joints, parents, positions, bounds, fit notes.
- render: views of the mesh with the skeleton, zoom on a joint or point, x-ray, skin-weight
  colors (after binding), or the bound model posed in any animation at any time.
- inspect: per joint, whether it's inside the mesh, distance to the surface, offset from the
  middle of the limb's cross-section and its width, left/right mismatch.
- slice / ray: raw geometry. A slice at a height lists the separate pieces the mesh is cut into
  (two legs, a torso and two arms...) with their bounds; a ray lists surface hits.
- set_joints: absolute or relative positions, optional mirroring to the other side, optionally
  carrying child joints along. aim points a bone at a spot and brings everything below it along;
  rotate turns everything below a joint. Those two pose whole limbs, hands and tails at once,
  which matters for models in arbitrary poses. undo goes back. fit re-runs the auto-fit for
  some or all joints (it assumes a standing pose).
- transform_model: rotate/scale/move the model (e.g. turn it to face +Z); joints move with it.
- meshes: list the model's meshes and leave some out of fitting and skinning (a floor plane,
  a prop, a weapon). status lists them too.
- bind: compute skin weights and report which bones move how many vertices. Solver settings
  given to bind are saved, so renders and export use them too.
- weight_rules: override weights where the solver gets them wrong, by box, sphere, mesh or
  piece_at (the connected part nearest a point, for models built from separate panels):
  "only" these bones (a cape that should follow just the spine) or "never" these bones (a skirt
  that shouldn't follow the calves, hips that shouldn't follow hands resting on them). A bone
  name ending in * includes every bone below it ("thigh_l*"); other * are wildcards ("hand_*").
  Rules apply in order, broad ones first. Check the result with render weights or an animation.
- animations: search the library. export: write a rigged GLB with any animations.

Things that tend to matter
- Animations and the _l/_r names assume the character faces +Z. One facing -Z ends up with
  left and right swapped and walks backwards; the fit notes say when the feet point toward -Z.
  transform_model with rotate [0, 180, 0] turns it around, then fit again. Chunky boots and
  robot feet can look backwards too, so check the face before turning.
- Joints usually belong in the middle of the limb, at the bend (elbow, knee, wrist), and the
  spine runs through the middle of the torso. Fingers follow the hand.
- Previewing an animation after binding (render with animation + time) shows deformation
  problems that a static pose hides: arms pulling the torso, the head pulled by the shoulders.
- rest_rotations decides how animations land on the rig. "limbs" (default) turns arm, leg,
  wing, finger and toe joints so animations reproduce the template's limb poses, which handles
  arms-down and A-posed models, and keeps the character's own spine, neck and head posture.
  "aligned" turns every joint (imposes the template's posture too). "template" turns none, as
  the afk.ai website does. Preview an animation with each if a pose looks off.
- Animation previews report lowest_point_vs_rest_floor: how far the model floats (+) or sinks
  (-) in that frame. Export and render take ground: true to keep the feet down.
- Bind options head_weight_correction_height and arm_plane_correction_offset can fix the head
  following the arms and torso following A-posed arms.
`;
  }
});

// src/log.ts
function quiet_console() {
  const noop = () => {
  };
  console.log = noop;
  console.info = noop;
  console.debug = noop;
  console.time = noop;
  console.timeEnd = noop;
  console.warn = noop;
}
function console_to_stderr() {
  const write = (...args) => {
    process.stderr.write(args.map((a) => typeof a === "string" ? a : JSON.stringify(a)).join(" ") + "\n");
  };
  console.log = write;
  console.info = write;
  console.debug = write;
  console.warn = write;
  console.time = () => {
  };
  console.timeEnd = () => {
  };
}
var init_log = __esm({
  "src/log.ts"() {
    "use strict";
  }
});

// src/mcp.ts
var mcp_exports = {};
__export(mcp_exports, {
  run_mcp_server: () => run_mcp_server
});
import { statSync as statSync2, writeFileSync as writeFileSync3 } from "node:fs";
import { resolve as resolve3 } from "node:path";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
async function open(project2) {
  const path = resolve3(project2);
  const mtime = statSync2(path).mtimeMs;
  const cached = sessions.get(path);
  if (cached !== void 0 && cached.mtime === mtime) return cached.session;
  const session = await RigSession.open(path);
  sessions.set(path, { session, mtime });
  return session;
}
function remember(session) {
  sessions.set(session.project_path, { session, mtime: statSync2(session.project_path).mtimeMs });
}
function json(value) {
  return { content: [{ type: "text", text: JSON.stringify(value, null, 1) }] };
}
async function run(work) {
  try {
    return await work();
  } catch (error) {
    return { content: [{ type: "text", text: error instanceof Error ? error.message : String(error) }], isError: true };
  }
}
async function run_mcp_server() {
  console_to_stderr();
  const server = new McpServer({ name: "afk-rig", version: VERSION }, { instructions: GUIDE });
  server.registerTool("rig_skeletons", {
    description: "List the skeleton templates and how many library animations each has.",
    inputSchema: {}
  }, async () => json((await describe_skeletons()).map((s) => ({ ...s, animations: list_clips(s.name).length }))));
  server.registerTool("rig_start", {
    description: "Load a GLB/glTF model, choose a skeleton and run the deterministic auto-fit. Creates a project JSON (default <model>.afk-rig.json) used by every other tool. Returns the model summary, fit notes and every joint with its parent and position.",
    inputSchema: {
      model: z.string().describe("path to a .glb or .gltf file"),
      skeleton: z.string().describe("human, fox, horse, bird, dragon, kaiju, spider, snake or fish"),
      hands: z.enum(HAND_OPTIONS).optional().describe("human finger detail, default all-fingers"),
      fit: z.boolean().optional().describe("false starts from the template scaled over the model instead of the auto-fit"),
      project: z.string().optional().describe("where to save the project JSON")
    }
  }, async (args) => await run(async () => {
    const session = await RigSession.start(args);
    remember(session);
    return json(session.status());
  }));
  server.registerTool("rig_status", {
    description: "The project's model summary, bounds, fit notes, landmarks and all joints with parents and positions.",
    inputSchema: { project }
  }, async ({ project: project2 }) => await run(async () => json((await open(project2)).status())));
  server.registerTool("rig_render", {
    description: "Orthographic views of the model with the skeleton on top, rulers in model units and joint labels. Can zoom on a joint or point, show skin weights (after binding), or pose the bound model with a library animation at a given time. Returns the image plus each joint's pixel position per view.",
    inputSchema: {
      project,
      views: z.array(z.enum(VIEW_NAMES)).optional().describe("default front and left"),
      size: z.number().optional().describe("pixels per view, default 640"),
      focus: z.union([z.string(), triple]).optional().describe("joint name or [x,y,z] to zoom on"),
      radius: z.number().optional().describe("zoom radius in model units, default 15% of the model height"),
      joints: selection.optional().describe("joints to draw, default all"),
      labels: selection.optional().describe("joints to label, default main (all when zoomed)"),
      xray: z.boolean().optional().describe("lighter see-through mesh"),
      weights: z.boolean().optional().describe("color the mesh by the bone that moves it most"),
      bone: z.string().optional().describe("show one bone's influence, blue (none) to red (full)"),
      animation: z.string().optional().describe("pose the bound model with this animation"),
      time: z.number().optional().describe("seconds into the animation, default the middle"),
      rest_rotations: rest,
      arm_spread_degrees: z.number().optional().describe("raise (+) or lower (-) both upper arms during the animation"),
      ground: z.boolean().optional().describe("keep the lowest joint at its rest height in every frame, as export can"),
      markers: z.array(z.object({ position: triple, label: z.string().optional() })).optional().describe("extra points to mark"),
      save_to: z.string().optional().describe("also write the PNG here")
    }
  }, async ({ project: project2, save_to, ...options }) => await run(async () => {
    const session = await open(project2);
    const result = await session.render(options);
    if (save_to !== void 0) writeFileSync3(resolve3(save_to), result.png);
    const info = { width: result.width, height: result.height, panels: result.panels, joint_pixels: result.joint_pixels, pose: result.pose, weight_colors: result.weight_colors, saved_to: save_to };
    return { content: [{ type: "image", data: result.png.toString("base64"), mimeType: "image/png" }, { type: "text", text: JSON.stringify(info) }] };
  }));
  server.registerTool("rig_inspect", {
    description: "Per joint: inside the mesh or not (null on open meshes like cloth where it can't tell), distance to the surface, offset from the middle of the mesh cross-section across the bone (with its width/depth), and left/right mismatch. issues_only lists just the joints that look off, with reasons.",
    inputSchema: { project, joints: z.array(z.string()).optional().describe("default all"), issues_only: z.boolean().optional() }
  }, async ({ project: project2, joints, issues_only }) => await run(async () => {
    const session = await open(project2);
    return json(issues_only === true ? { issues: session.issues(joints) } : session.inspect(joints));
  }));
  server.registerTool("rig_slice", {
    description: "Cut the mesh with a plane (axis = value) and list the separate pieces it falls into, largest first, with their centers and bounds. E.g. a Y slice through the thighs shows two legs.",
    inputSchema: { project, axis: z.enum(["x", "y", "z"]), at: z.number(), thickness: z.number().optional() }
  }, async ({ project: project2, axis, at, thickness }) => await run(async () => json({ axis, at, pieces: (await open(project2)).slice(axis, at, thickness) })));
  server.registerTool("rig_ray", {
    description: "Cast a ray at the mesh and list every surface hit, nearest first.",
    inputSchema: { project, origin: triple, direction: triple }
  }, async ({ project: project2, origin, direction }) => await run(async () => json({ hits: (await open(project2)).ray(origin, direction) })));
  server.registerTool("rig_set_joints", {
    description: "Move joints. Values are absolute positions, or offsets with relative. mirror also places each joint's left/right partner reflected across mirror_x (default the pelvis/hips x). with_children carries everything below a joint along. Undoable.",
    inputSchema: {
      project,
      joints: z.record(z.string(), triple).describe('{ "joint_name": [x, y, z] }'),
      relative: z.boolean().optional(),
      mirror: z.boolean().optional(),
      mirror_x: z.number().optional(),
      with_children: z.boolean().optional()
    }
  }, async ({ project: project2, joints, ...options }) => await run(async () => {
    const session = await open(project2);
    const changed = session.set_joints(joints, options);
    remember(session);
    return json({ changed });
  }));
  server.registerTool("rig_aim", {
    description: "Point a bone somewhere: everything below the joint turns around it so the bone toward its child points at the target. stretch also scales the chain so the child lands on the target. Poses a whole limb, hand, neck or tail in one step, handy for models in arbitrary poses. Undoable.",
    inputSchema: {
      project,
      joint: z.string(),
      at: triple.describe("world point the bone should point at"),
      child: z.string().optional().describe("which child defines the bone (default the bone's own child)"),
      stretch: z.boolean().optional()
    }
  }, async ({ project: project2, joint, at, child, stretch }) => await run(async () => {
    const session = await open(project2);
    const changed = session.aim(joint, at, { child, stretch });
    remember(session);
    return json({ changed });
  }));
  server.registerTool("rig_rotate", {
    description: "Turn everything below a joint around it, by degrees about a world-space axis (e.g. curl a hand or swing a leg). Undoable.",
    inputSchema: { project, joint: z.string(), axis: triple, degrees: z.number() }
  }, async ({ project: project2, joint, axis, degrees }) => await run(async () => {
    const session = await open(project2);
    const changed = session.rotate(joint, axis, degrees);
    remember(session);
    return json({ changed });
  }));
  server.registerTool("rig_fit", {
    description: "Re-run the auto-fit for all joints or only the listed ones (mode auto), or reset to the template scaled over the model (mode template). Undoable.",
    inputSchema: { project, joints: z.array(z.string()).optional(), mode: z.enum(["auto", "template"]).optional() }
  }, async ({ project: project2, joints, mode }) => await run(async () => {
    const session = await open(project2);
    const notes = session.fit(mode ?? "auto", joints);
    remember(session);
    return json({ notes });
  }));
  server.registerTool("rig_transform_model", {
    description: "Rotate (degrees around X, Y, Z, about the origin), scale or move the model, e.g. to turn it to face +Z. The joints move with it. The exported file uses the transformed model.",
    inputSchema: { project, rotate: triple.optional(), scale: z.number().optional(), translate: triple.optional() }
  }, async ({ project: project2, ...transform }) => await run(async () => {
    const session = await open(project2);
    await session.transform_model(transform);
    remember(session);
    return json({ model_bounds: session.status().model_bounds });
  }));
  server.registerTool("rig_meshes", {
    description: "List the model's meshes (id, name, triangles, bounds), and leave some out of fitting and skinning: floors, props, weapons, stray geometry. Excluded meshes stay in the exported file unrigged unless the export drops them.",
    inputSchema: {
      project,
      exclude: z.array(z.union([z.number(), z.string()])).optional().describe("mesh ids or names to leave out"),
      include: z.array(z.union([z.number(), z.string()])).optional().describe("mesh ids or names to bring back")
    }
  }, async ({ project: project2, exclude, include }) => await run(async () => {
    const session = await open(project2);
    if (exclude !== void 0 || include !== void 0) {
      await session.set_excluded_meshes(exclude, include);
      remember(session);
    }
    const status = session.status();
    return json({ meshes: status.meshes, model_bounds: status.model_bounds });
  }));
  server.registerTool("rig_undo", {
    description: "Undo joint changes.",
    inputSchema: { project, steps: z.number().int().min(1).optional() }
  }, async ({ project: project2, steps }) => await run(async () => {
    const session = await open(project2);
    const undone = session.undo(steps ?? 1);
    remember(session);
    return json({ undone });
  }));
  server.registerTool("rig_bind", {
    description: "Compute skin weights for the current joints and report how many vertices each bone moves most, and bones that move nothing. Solver settings given here are saved and used by rig_render (weights, animation) and rig_export.",
    inputSchema: {
      project,
      rest_rotations: rest,
      fix_stray_patches: z.boolean().optional().describe("default true: hand back patches a limb took from another body part it touches (hips under resting hands)"),
      head_weight_correction_height: z.number().optional().describe("world Y: arm-weighted vertices above it go to the head/neck"),
      arm_plane_correction_offset: z.number().optional().describe("give torso vertices back from arms that hang close to the body; offset from the shoulder x"),
      reset: z.boolean().optional().describe("clear saved solver settings")
    }
  }, async ({ project: project2, rest_rotations, ...options }) => await run(async () => {
    const session = await open(project2);
    const report = session.bind_report(options, rest_rotations);
    remember(session);
    return json(report);
  }));
  const weight_rule = z.object({
    mode: z.enum(["only", "never"]).describe("only: the picked vertices may follow just these bones. never: they may not follow these bones"),
    bones: z.array(z.string()).describe('bone names. "spine_01*" (a bone name then *) is that bone and every bone below it; any other * is a wildcard over names, e.g. "hand_*" or "*_l"'),
    box: z.object({ min: triple, max: triple }).optional(),
    sphere: z.object({ center: triple, radius: z.number() }).optional(),
    meshes: z.array(z.number()).optional().describe("mesh ids from rig_meshes"),
    piece_at: triple.optional().describe("a point on or near a part: picks the connected piece of mesh nearest it (one panel, glove, strap or shell of a model built from separate parts)")
  });
  server.registerTool("rig_weight_rules", {
    description: "Override skin weights where the solver gets them wrong, e.g. keep a cape or skirt off the leg bones, or make a helmet follow only the head. Vertices are picked by box, sphere, meshes and/or piece_at (all given must match). Rules apply in the order added on every bind, weights/animation render and export; when a rule takes every bone from a vertex it goes to the nearest bone that rule allows, even one an earlier rule excluded, so put broad rules first. Returns the rules; rig_bind reports how many vertices each changed.",
    inputSchema: {
      project,
      add: z.array(weight_rule).optional(),
      remove: z.array(z.number().int()).optional().describe("indexes of rules to remove"),
      clear: z.boolean().optional()
    }
  }, async ({ project: project2, add, remove, clear }) => await run(async () => {
    const session = await open(project2);
    const rules = session.set_weight_rules({ add, remove, clear });
    remember(session);
    return json({ weight_rules: rules });
  }));
  server.registerTool("rig_animations", {
    description: "Search the animation library for a skeleton (or a project's skeleton). Returns names, lengths in seconds and whether they move the character through space.",
    inputSchema: { skeleton: z.string().optional(), project: z.string().optional(), search: z.string().optional().describe('words to match, e.g. "walk run"') }
  }, async ({ skeleton, project: project2, search }) => await run(async () => {
    const name = project2 !== void 0 ? (await open(project2)).status().skeleton : parse_skeleton(skeleton ?? "human");
    const clips = list_clips(name, search);
    return json({ skeleton: name, count: clips.length, animations: clips.map((c) => ({ name: c.name, seconds: c.duration, root_motion: c.root_motion })) });
  }));
  server.registerTool("rig_export", {
    description: "Write the rigged model as GLB (or .gltf) with skin weights, the skeleton and the chosen animations. Materials and textures are kept.",
    inputSchema: {
      project,
      output: z.string().describe("path for the .glb"),
      animations: z.union([z.literal("all"), z.array(z.string())]).optional().describe('animation names, or "all"; default none'),
      rest_rotations: rest,
      drop_excluded_meshes: z.boolean().optional().describe("leave excluded meshes out of the file instead of keeping them unrigged"),
      ground: z.boolean().optional().describe("add a root track that keeps the lowest joint at its rest height in every frame, for clips that float or sink on this rig (common for crouches and sits on animals); root-motion clips are left alone"),
      arm_spread_degrees: z.number().optional(),
      head_weight_correction_height: z.number().optional(),
      arm_plane_correction_offset: z.number().optional()
    }
  }, async ({ project: project2, ...options }) => await run(async () => json(await (await open(project2)).export(options))));
  await server.connect(new StdioServerTransport());
}
var VERSION, sessions, triple, selection, rest, project;
var init_mcp = __esm({
  "src/mcp.ts"() {
    "use strict";
    init_session();
    init_skeleton();
    init_animation();
    init_render();
    init_guide();
    init_log();
    VERSION = "0.1.2";
    sessions = /* @__PURE__ */ new Map();
    triple = z.tuple([z.number(), z.number(), z.number()]);
    selection = z.union([z.enum(["all", "main", "none"]), z.array(z.string())]);
    rest = z.enum(["limbs", "aligned", "template"]).optional().describe("How joint rotations are set at rest, which decides how animations land. limbs (default): arms, legs, wings, fingers and toes turn so animations reproduce the template's limb poses (handles A-pose and arms-down models); the spine, neck and head keep the template's rotations so the character's own posture is kept. aligned: every joint turns, which also imposes the template's posture. template: no joint turns, as on the afk.ai website.");
    project = z.string().describe("path to the project JSON from rig_start");
  }
});

// src/cli.ts
init_session();
init_skeleton();
init_animation();
init_guide();
init_log();
import { writeFileSync as writeFileSync4 } from "node:fs";
import { basename as basename2, dirname as dirname2, extname as extname3, join as join2, resolve as resolve4 } from "node:path";
import { parseArgs } from "node:util";
var VERSION2 = "0.1.2";
var HELP = `afk-rig ${VERSION2}: free local auto-rigging, built to be driven by an AI

Usage: afk-rig <command> [arguments]

  auto <model> --skeleton human --out rigged.glb [--animations Walk,Idle_A|all]
        start + export in one go
  start <model> --skeleton <type> [--hands all-fingers] [--no-fit] [--project p.json]
  status <project>
  render <project> [--views front,left] [--size 640] [--focus joint|x,y,z] [--radius r]
        [--joints all|main|none|a,b] [--labels ...] [--xray] [--weights] [--bone name]
        [--animation name --time seconds [--ground]] [--rest limbs|aligned|template] [--out image.png]
  inspect <project> [--joints a,b] [--issues]     --issues lists only joints that look off
  slice <project> --axis y --at 0.9 [--thickness t]
  ray <project> --from x,y,z --dir x,y,z
  set <project> name=x,y,z ... [--relative] [--mirror] [--mirror-x x] [--with-children]
  move <project> name=dx,dy,dz ...      (set --relative)
  aim <project> --joint upperarm_l --at x,y,z [--child lowerarm_l] [--stretch]
        turn everything below a joint so its bone points at a spot (pose a whole limb)
  rotate <project> --joint hand_l --axis 0,0,1 --degrees 30
        turn everything below a joint around it
  fit <project> [--joints a,b] [--template]
  transform <project> [--rotate x,y,z] [--scale s] [--translate x,y,z]
  meshes <project> [--exclude id|name,...] [--include id|name,...]
        leave meshes (floors, props) out of fitting and skinning
  undo <project> [--steps n]
  bind <project> [--rest limbs|aligned|template] [--head-correction y] [--arm-plane-offset o] [--reset]
        settings are saved and used by previews and export
  weights <project> [--add '{"mode":"only","bones":["pelvis","spine_01*"],"box":{"min":[x,y,z],"max":[x,y,z]}}']
        [--remove 0,2] [--clear]      skin weight rules (only / never these bones, by box, sphere, meshes
        or "piece_at":[x,y,z], the connected part nearest a point); applied in order, broad first;
        "thigh_l*" = thigh_l and the bones below it, other * are wildcards ("hand_*")
  animations <skeleton|project> [--search walk]
  skeletons
  export <project> --out rigged.glb [--animations a,b|all] [--rest limbs|aligned|template]
        [--arm-spread degrees] [--ground] [--head-correction y] [--arm-plane-offset o] [--drop-excluded]
  mcp       run as an MCP server on stdio
  guide     how the tools fit together

Skeletons: human, fox, horse, bird, dragon, kaiju, spider, snake, fish.
Projects are JSON files (default: <model>.afk-rig.json next to the model).
`;
var OPTIONS = {
  skeleton: { type: "string" },
  hands: { type: "string" },
  "no-fit": { type: "boolean" },
  project: { type: "string" },
  views: { type: "string" },
  size: { type: "string" },
  focus: { type: "string" },
  radius: { type: "string" },
  joints: { type: "string" },
  labels: { type: "string" },
  xray: { type: "boolean" },
  weights: { type: "boolean" },
  bone: { type: "string" },
  animation: { type: "string" },
  time: { type: "string" },
  rest: { type: "string" },
  out: { type: "string", short: "o" },
  axis: { type: "string" },
  at: { type: "string" },
  thickness: { type: "string" },
  from: { type: "string" },
  dir: { type: "string" },
  relative: { type: "boolean" },
  mirror: { type: "boolean" },
  "mirror-x": { type: "string" },
  "with-children": { type: "boolean" },
  template: { type: "boolean" },
  rotate: { type: "string" },
  scale: { type: "string" },
  translate: { type: "string" },
  steps: { type: "string" },
  "head-correction": { type: "string" },
  "arm-plane-offset": { type: "string" },
  search: { type: "string" },
  animations: { type: "string" },
  "arm-spread": { type: "string" },
  verbose: { type: "boolean" },
  exclude: { type: "string" },
  include: { type: "string" },
  "drop-excluded": { type: "boolean" },
  add: { type: "string", multiple: true },
  remove: { type: "string" },
  clear: { type: "boolean" },
  issues: { type: "boolean" },
  ground: { type: "boolean" },
  joint: { type: "string" },
  child: { type: "string" },
  stretch: { type: "boolean" },
  axis3: { type: "string" },
  degrees: { type: "string" },
  reset: { type: "boolean" },
  help: { type: "boolean", short: "h" },
  version: { type: "boolean", short: "v" }
};
function triple2(value, what) {
  const parts = value.split(",").map((s) => Number(s.trim()));
  if (parts.length !== 3 || parts.some((n) => !Number.isFinite(n))) throw new Error(`${what} needs three numbers like 0.1,1.2,0 (got "${value}")`);
  return parts;
}
function list(value) {
  return value === void 0 ? void 0 : value.split(",").map((s) => s.trim()).filter((s) => s !== "");
}
function selection2(value) {
  if (value === void 0) return void 0;
  if (["all", "main", "none"].includes(value)) return value;
  return list(value);
}
function number(value) {
  if (value === void 0) return void 0;
  const n = Number(value);
  if (!Number.isFinite(n)) throw new Error(`Expected a number, got "${value}"`);
  return n;
}
function rest2(value) {
  if (value === void 0) return void 0;
  if (value !== "limbs" && value !== "template" && value !== "aligned") throw new Error("--rest is limbs, aligned or template");
  return value;
}
function print(value) {
  process.stdout.write(JSON.stringify(value, null, 1) + "\n");
}
function join_negative_values(args) {
  const out = [];
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const next = args[i + 1];
    const name = arg.startsWith("--") ? arg.slice(2) : void 0;
    const takes_value = name !== void 0 && !name.includes("=") && OPTIONS[name]?.type === "string";
    if (takes_value && next !== void 0 && /^-[\d.]/.test(next)) {
      out.push(`${arg}=${next}`);
      i++;
    } else {
      out.push(arg);
    }
  }
  return out;
}
async function main() {
  const { values: o, positionals } = parseArgs({ args: join_negative_values(process.argv.slice(2)), options: OPTIONS, allowPositionals: true, strict: true });
  const [command, ...args] = positionals;
  if (o.version === true) {
    print({ version: VERSION2 });
    return;
  }
  if (command === void 0 || o.help === true || command === "help") {
    process.stdout.write(HELP);
    return;
  }
  if (command !== "mcp" && o.verbose !== true) quiet_console();
  const need = (index, what) => {
    const value = args[index];
    if (value === void 0) throw new Error(`Missing ${what}. Run afk-rig help.`);
    return value;
  };
  switch (command) {
    case "guide":
      process.stdout.write(GUIDE);
      return;
    case "mcp": {
      const { run_mcp_server: run_mcp_server2 } = await Promise.resolve().then(() => (init_mcp(), mcp_exports));
      await run_mcp_server2();
      return;
    }
    case "skeletons":
      print((await describe_skeletons()).map((s) => ({ ...s, animations: list_clips(s.name).length })));
      return;
    case "animations": {
      const target = need(0, "skeleton name or project");
      const skeleton = target.endsWith(".json") ? (await RigSession.open(target)).status().skeleton : parse_skeleton(target);
      const clips = list_clips(skeleton, o.search);
      print({ skeleton, count: clips.length, animations: clips.map((c) => ({ name: c.name, seconds: c.duration, root_motion: c.root_motion })) });
      return;
    }
    case "start":
    case "auto": {
      const model = need(0, "model path");
      if (o.skeleton === void 0) throw new Error("--skeleton is required: human, fox, horse, bird, dragon, kaiju, spider, snake or fish");
      if (o.hands !== void 0 && !HAND_OPTIONS.includes(o.hands)) throw new Error(`--hands is one of ${HAND_OPTIONS.join(", ")}`);
      const session2 = await RigSession.start({ model, skeleton: o.skeleton, hands: o.hands, fit: o["no-fit"] !== true, project: o.project });
      if (command === "start") {
        print(session2.status());
        return;
      }
      const out = o.out ?? join2(dirname2(resolve4(model)), basename2(model, extname3(model)) + ".rigged.glb");
      print({ project: session2.project_path, fit_notes: session2.status().fit_notes, ...await export_with(session2, out, o) });
      return;
    }
  }
  const session = await RigSession.open(need(0, "project path"));
  switch (command) {
    case "status":
      print(session.status());
      return;
    case "inspect":
      print(o.issues === true ? { issues: session.issues(list(o.joints)) } : session.inspect(list(o.joints)));
      return;
    case "slice": {
      const axis = o.axis ?? "y";
      if (axis !== "x" && axis !== "y" && axis !== "z") throw new Error("--axis is x, y or z");
      const at = number(o.at);
      if (at === void 0) throw new Error("--at is required");
      print({ axis, at, pieces: session.slice(axis, at, number(o.thickness)) });
      return;
    }
    case "ray": {
      if (o.from === void 0 || o.dir === void 0) throw new Error("--from and --dir are required");
      print({ hits: session.ray(triple2(o.from, "--from"), triple2(o.dir, "--dir")) });
      return;
    }
    case "set":
    case "move": {
      const updates = {};
      for (const arg of args.slice(1)) {
        const [name, value] = arg.split("=");
        if (value === void 0) throw new Error(`Write joints as name=x,y,z (got "${arg}")`);
        updates[name.trim()] = triple2(value, name);
      }
      if (Object.keys(updates).length === 0) throw new Error("Give at least one joint, like hand_l=0.6,1.2,0");
      print({ changed: session.set_joints(updates, { relative: command === "move" || o.relative === true, mirror: o.mirror, mirror_x: number(o["mirror-x"]), with_children: o["with-children"] }) });
      return;
    }
    case "fit":
      print({ notes: session.fit(o.template === true ? "template" : "auto", list(o.joints)) });
      return;
    case "aim": {
      if (o.joint === void 0 || o.at === void 0) throw new Error("aim needs --joint and --at x,y,z");
      print({ changed: session.aim(o.joint, triple2(o.at, "--at"), { child: o.child, stretch: o.stretch }) });
      return;
    }
    case "rotate": {
      const axis = o.axis3 ?? o.axis;
      if (o.joint === void 0 || axis === void 0 || o.degrees === void 0) throw new Error("rotate needs --joint, --axis x,y,z and --degrees");
      print({ changed: session.rotate(o.joint, triple2(axis, "--axis"), number(o.degrees)) });
      return;
    }
    case "transform": {
      await session.transform_model({
        rotate: o.rotate !== void 0 ? triple2(o.rotate, "--rotate") : void 0,
        scale: number(o.scale),
        translate: o.translate !== void 0 ? triple2(o.translate, "--translate") : void 0
      });
      const status = session.status();
      print({ model_bounds: status.model_bounds, note: "Joints moved with the model. Run fit to place them again if needed." });
      return;
    }
    case "undo":
      print({ undone: session.undo(number(o.steps) ?? 1) });
      return;
    case "weights": {
      const add = (o.add ?? []).map((text) => {
        try {
          return JSON.parse(text);
        } catch {
          throw new Error(`--add takes a JSON rule, got: ${text}`);
        }
      });
      const changing = add.length > 0 || o.remove !== void 0 || o.clear === true;
      const rules = changing ? session.set_weight_rules({ add, remove: list(o.remove)?.map(Number), clear: o.clear }) : session.status().weight_rules;
      print({ weight_rules: rules, note: "Rules apply on every bind, render with weights or animation, and export." });
      return;
    }
    case "meshes": {
      if (o.exclude !== void 0 || o.include !== void 0) await session.set_excluded_meshes(list(o.exclude), list(o.include));
      const status = session.status();
      print({ meshes: status.meshes, model_bounds: status.model_bounds });
      return;
    }
    case "bind":
      print(session.bind_report({ head_weight_correction_height: number(o["head-correction"]), arm_plane_correction_offset: number(o["arm-plane-offset"]), reset: o.reset }, rest2(o.rest)));
      return;
    case "render": {
      const result = await session.render({
        views: list(o.views),
        size: number(o.size),
        focus: o.focus === void 0 ? void 0 : /^[-\d.]+,[-\d.]+,[-\d.]+$/.test(o.focus) ? triple2(o.focus, "--focus") : o.focus,
        radius: number(o.radius),
        joints: selection2(o.joints),
        labels: selection2(o.labels),
        xray: o.xray,
        weights: o.weights,
        bone: o.bone,
        animation: o.animation,
        time: number(o.time),
        rest_rotations: rest2(o.rest),
        arm_spread_degrees: number(o["arm-spread"]),
        ground: o.ground
      });
      const out = resolve4(o.out ?? session.project_path.replace(/\.json$/, "") + ".png");
      writeFileSync4(out, result.png);
      print({ image: out, width: result.width, height: result.height, panels: result.panels, joint_pixels: result.joint_pixels, pose: result.pose, weight_colors: result.weight_colors });
      return;
    }
    case "export": {
      if (o.out === void 0) throw new Error("--out is required");
      print(await export_with(session, o.out, o));
      return;
    }
    default:
      throw new Error(`Unknown command "${command}". Run afk-rig help.`);
  }
}
async function export_with(session, out, o) {
  const names = o.animations;
  return { ...await session.export({
    output: out,
    animations: names === "all" ? "all" : list(names),
    rest_rotations: rest2(o.rest),
    drop_excluded_meshes: o["drop-excluded"] === true,
    ground: o.ground === true,
    arm_spread_degrees: number(o["arm-spread"]),
    head_weight_correction_height: number(o["head-correction"]),
    arm_plane_correction_offset: number(o["arm-plane-offset"])
  }) };
}
main().catch((error) => {
  process.stderr.write(`afk-rig: ${error instanceof Error ? error.message : String(error)}
`);
  process.exit(1);
});
