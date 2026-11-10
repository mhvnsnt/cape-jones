// build-fla-timeline.jsfl — Cape Jones timeline builder, joint-locked v5
// STATUS: written 2026-10-31, NOT run in Adobe Animate here (no Animate in this VM).
// Open in Animate, run, then check the timeline by eye before calling it done.
// WHAT IT DOES:
//  1. Creates Graphic Symbols for: Head_Front, Torso_Chest, Pelvis,
//     Arm_Front_Upper/Lower (ARM 1, our left), Arm_Back_Upper/Lower (ARM 2, our right),
//     Leg_Front_Upper/Lower (LEG 1, our left), Leg_Back_Upper/Lower (LEG 2, our right),
//     Cape_Back_Main, Cape_Collar, Neck, Belt.
//  2. Makes layers with those names, in that order, bottom to top.
//  3. For each keyframe in the clip JSON (paste the clip object below as CLIP),
//     inserts a keyframe at that frame number and sets each limb's rotation.
// ANGLE CONVERSION, read this before editing:
//  Clip angles are v5 screen angles: 0 = straight down, positive = toward screen-right,
//  end = joint + length * (sin(angle), cos(angle)).
//  Animate rotation is clockwise in degrees, with 0 = pointing right.
//  A limb pointing down (clip 0) is Animate 90. A limb pointing screen-right
//  (clip +90) is Animate 0. So: animateRotation = 90 - clipAngle.
//  Pivots: set each symbol's registration point to its joint anchor before
//  placing it — shoulder (430,445)/(670,445), hip (485,740)/(615,740) on the
//  1100x1500 canvas, scale 0.95. Do NOT centre pivots; centre pivots break the lock.
//  Cape is NOT rotated by this script — cape states (draped/swinging/billowing)
//  are Pack 5 pieces, still missing. Swap the Cape symbol per shot, do not rotate a flat cape and call it billowing.

var CLIP = {
  // PASTE a clip here, e.g. punch-clip.json / flying-clip.json / jump-clip.json
  // Format: { "clip": "punch", "fps": 24, "keyframes": [
  //   { "frame": 1, "hold": 6, "pose": "windup",
  //     "arm1_upper": -20, "arm1_lower": -120, "arm2_upper": 20, "arm2_lower": 160,
  //     "leg1_upper": -10, "leg1_lower": 10, "leg2_upper": 10, "leg2_lower": -10 } ] }
  "clip": "punch",
  "fps": 24,
  "keyframes": []
};

function animateRotation(clipAngle) { return 90 - clipAngle; }

var doc = fl.createDocument();
doc.frameRate = CLIP.fps;
var timeline = doc.getTimeline();
var layers = ["Cape_Back_Main", "Leg1_Upper", "Leg1_Lower", "Leg2_Upper", "Leg2_Lower",
  "Arm1_Upper", "Arm2_Upper", "Pelvis", "Cape_Collar", "Torso_Chest", "Belt",
  "Arm1_Lower", "Arm2_Lower", "Neck", "Head_Front"];
// Layers are created top-first in Animate; reverse so Cape_Back ends up at the bottom.
for (var i = layers.length - 1; i >= 0; i--) {
  timeline.addNewLayer(layers[i]);
}
// Keyframes: one per clip keyframe, at its frame number.
for (var k = 0; k < CLIP.keyframes.length; k++) {
  var kf = CLIP.keyframes[k];
  var frame = kf.frame - 1; // Animate frames are 0-based
  var map = {
    "Arm1_Upper": kf.arm1_upper, "Arm1_Lower": kf.arm1_lower,
    "Arm2_Upper": kf.arm2_upper, "Arm2_Lower": kf.arm2_lower,
    "Leg1_Upper": kf.leg1_upper, "Leg1_Lower": kf.leg1_lower,
    "Leg2_Upper": kf.leg2_upper, "Leg2_Lower": kf.leg2_lower
  };
  for (var li = 0; li < timeline.layerCount; li++) {
    var layer = timeline.layers[li];
    if (map.hasOwnProperty(layer.name)) {
      timeline.currentLayer = li;
      timeline.insertKeyframe(frame);
      var el = timeline.layers[li].frames[frame].elements[0];
      if (el) { el.rotation = animateRotation(map[layer.name]); }
    }
  }
}
fl.trace("Cape Jones timeline built: " + CLIP.clip + ", " + CLIP.keyframes.length + " keyframes. Check pivots by eye before calling it done.");
