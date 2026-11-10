// cape_jones_import_stub.js — Harmony QtScript stub, UNTESTED until activation.
// Run inside Toon Boom Harmony 27 Premium only, after activation, from the
// scripting interface. It does NOT copy Toon Boom code; it uses only the
// public scripting pattern documented in Harmony docs:
//   node.getAttr("Top/Drawing-P", 1, "position.x").doubleValue()
// and node creation / linking as described in the Harmony scripting docs.
// BEFORE RUNNING: import the pieces in nodes.csv as bitmap drawings and
// verify cape/pelvis/head pivots (assumed centre in the CSV) via
// Node View > Show Attribute Information. If a node name differs, edit
// the CSV, not this stub's logic, and re-run.
// This stub logs every step with MessageLog.trace so the in-app log can
// be checked against nodes.csv. It does not bypass activation, does not
// touch licenses, and does not render anything on its own.
//
// Node list (z-order, DEFS-stable; ties by DEFS order, e.g. forearmL
// before pelvis before kneeL at z=4):
//   Cape, Arm1-Upper, Leg2-Thigh, Leg1-Thigh, Arm1-Forearm, Pelvis,
//   Leg1-Knee, Arm1-ElbowCap, Leg1-Shin, Leg2-Shin, Leg2-Knee, Torso,
//   Neck, Head, Arm2-Upper, Arm2-Forearm, Arm2-ElbowCap, Arm1-Hand, Arm2-Hand
//
// Usage in Harmony (after activation):
//   1. Open the CapeJones_Sitting scene.
//   2. Run this script from the scripting interface.
//   3. Check the MessageLog: every peg should report its position.x,
//      position.y and rotation.anglez, matching nodes.csv saved_x /
//      saved_y / saved_rotation. Any mismatch = stop, fix the peg, re-run.
//   4. Save the rig as a Template (.tpl) in the CapeJones library.

function checkPeg(pegPath) {
    // Public pattern only: read, do not write blindly.
    var x = node.getAttr(pegPath, 1, "position.x").doubleValue();
    var y = node.getAttr(pegPath, 1, "position.y").doubleValue();
    var r = node.getAttr(pegPath, 1, "rotation.anglez").doubleValue();
    MessageLog.trace("PEG " + pegPath + " x=" + x + " y=" + y + " rot=" + r);
    return {x: x, y: y, rot: r};
}

function main() {
    MessageLog.trace("Cape Jones import stub — UNTESTED until activation, check log vs nodes.csv");
    var pegs = [
        "Top/Cape-P", "Top/Arm1-Upper-P", "Top/Leg2-Thigh-P", "Top/Leg1-Thigh-P",
        "Top/Arm1-Forearm-P", "Top/Pelvis-P", "Top/Leg1-Knee-P",
        "Top/Arm1-ElbowCap-P", "Top/Leg1-Shin-P", "Top/Leg2-Shin-P",
        "Top/Leg2-Knee-P", "Top/Torso-P", "Top/Neck-P", "Top/Head-P",
        "Top/Arm2-Upper-P", "Top/Arm2-Forearm-P", "Top/Arm2-ElbowCap-P",
        "Top/Arm1-Hand-P", "Top/Arm2-Hand-P"
    ];
    for (var i = 0; i < pegs.length; i++) {
        try { checkPeg(pegs[i]); }
        catch (e) { MessageLog.trace("MISSING PEG (expected before import): " + pegs[i]); }
    }
    MessageLog.trace("Stub done. If pegs were missing, import nodes.csv first, then re-run.");
}

// Harmony scripting entry point: uncomment in-app if your version requires it.
// main();
