// Cape Jones — Adobe Animate rig builder, v8 (locked default T-pose, 2026-10-31)
// V8 changes vs v7: legs 460/705 and 640/705 (180 apart, up 15px). V7 changes vs v2: Head lowered to 250 (jaw on neck), Neck scale 1.05
// (wider), Pelvis up to 680, Belt up to 670, legs 450/650, arms both
// Arm_Front with a VERTICAL (top-to-bottom) flip on the left arm,
// pads top / fists bottom, screen-right leg is Leg_Back_GRAFTED.png
// (full toe). See TPOSE-LOCKED-v7.md and locked-default-tpose.json.
var folder = fl.browseForFolderURL("Pick the cape-jones-rig/sliced folder");
if (!folder) { fl.trace("Cancelled."); } else {
  var dom = fl.getDocumentDOM();
  if (!dom) { dom = fl.createDocument(); }
  dom.width = 1920; dom.height = 1080; dom.frameRate = 24;
  var tl = dom.getTimeline();
  // Bottom to top. Hand/Mouth swaps are imported last as their own symbols.
  // V2 2026-10-31, Mars cape correction: Cape_Collar over Cape_Back_Main,
  // Torso_Chest over Cape_Collar. Cape_Back_Main top at shoulders in the
  // stage layout, not behind the head.
  var STACK = [
    "Cape_Back_Main.png","Leg_Back_GRAFTED.png","Leg_Front.png",
    "Arm_Back.png","Arm_Front.png",
    "Pelvis.png","Cape_Collar.png","Torso_Chest.png","Belt_Overlay.png",
    "Neck.png","Head_Front.png","Head_Profile.png"
  ];
  // pivotX, pivotY as fractions of the bitmap (0,0 = top-left).
  var PIVOTS = {
    "Cape_Back_Main.png":[0.50,0.02], "Leg_Back.png":[0.50,0.08], "Leg_Front.png":[0.50,0.08],
    "Arm_Back.png":[0.50,0.08], "Arm_Front.png":[0.50,0.08],
    "Pelvis.png":[0.50,0.10], "Torso_Chest.png":[0.50,0.95], "Belt_Overlay.png":[0.50,0.50],
    "Neck.png":[0.50,0.50], "Head_Front.png":[0.50,0.95], "Head_Profile.png":[0.50,0.90], "Cape_Collar.png":[0.50,0.10]
  };
  // Clear default layer, then build bottom-to-top (Animate timeline lists top first).
  while (tl.layerCount > 0) { tl.deleteLayer(0); }
  for (var s = STACK.length - 1; s >= 0; s--) {
    var file = STACK[s];
    tl.addNewLayer(file.replace(".png",""), "normal", false);
    dom.importFile(folder + "/" + file, true);
    var el = dom.selection[0];
    if (el) {
      var w = el.width, h = el.height;
      dom.convertToSymbol("graphic", file.replace(".png",""), "top left");
      var sym = dom.selection[0];
      if (sym) {
        var p = PIVOTS[file];
        // Move registration to pivot: set x/y so the pivot lands at the
        // symbol origin used by the Free Transform tool (Q) for fine tuning.
        sym.setTransformationPoint({x: p[0]*w, y: p[1]*h});
      }
    }
  }
  // Swap symbols: hands (7 frames) and mouths (5 clean + Face_Angry as frame 6).
  function buildSwap(name, files) {
    var lib = dom.library;
    for (var i = 0; i < files.length; i++) {
      dom.importFile(folder + "/" + files[i], true);
      var e = dom.selection[0];
      if (e) { dom.convertToSymbol("graphic", name + "_" + files[i].replace(".png",""), "top left"); }
    }
    fl.trace("Swap pieces imported for " + name + ": " + files.join(", ") +
      " — nest them on successive frames of a Graphic symbol and set it to Single Frame.");
  }
  buildSwap("Hand_Swap", ["Hand_1_Fist.png","Hand_2_FistBack.png","Hand_3_Open.png","Hand_4_Point.png","Hand_5_Point2.png","Hand_6_Relaxed.png","Hand_7_Grip.png"]);
  buildSwap("Mouth_Swap", ["Mouth_Closed.png","Mouth_Smile.png","Mouth_Teeth.png","Mouth_Open.png","Mouth_Shout.png","Face_Angry.png"]);
  fl.trace("Done. Save as Cape_Jones_Master.fla, then check pivots with Q and parenting in Timeline Parenting view.");
}
