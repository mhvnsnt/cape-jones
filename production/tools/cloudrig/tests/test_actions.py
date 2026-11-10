import bpy
from bpy.types import Object


def has_log_entry(metarig: Object, log_description_short: str) -> bool:
    for log_entry in metarig.cloudrig.generator.logs:
        if log_entry.description_short == log_description_short:
            return True
    return False


def test_actions(context_actions):
    metarig = bpy.data.objects["META-Suzanne"]
    action_setup = metarig.cloudrig.generator.action_setups[0]

    # Action set-up should be un-initialized so we can test that parameters auto-initialize correctly.
    assert action_setup.transform_channel == "LOCATION_X", (
        "This test file should be saved with the Action set-up un-initialized!"
    )

    # Generate as-is, make sure we get the expected warnings.
    assert bpy.ops.pose.cloudrig_generate() == {"FINISHED"}
    assert has_log_entry(metarig, "No control specified")

    # Assign a subtarget, but avoid auto-initialization by dodging the setter,
    # and make sure we get the expected warnings.
    action_setup["subtarget"] = "Eye.L"
    assert bpy.ops.pose.cloudrig_generate() == {"FINISHED"}
    assert has_log_entry(metarig, "Action default frame must be whole")
    assert has_log_entry(metarig, "Action with 1-key curves")
    assert has_log_entry(metarig, "Action affects rest pose")

    # Set ranges to all 0
    action_setup.frame_start = action_setup.frame_end = action_setup.trans_min = (
        action_setup.trans_max
    ) = 0
    assert bpy.ops.pose.cloudrig_generate() == {"FINISHED"}
    assert has_log_entry(metarig, "Action has no transform range")
    assert has_log_entry(metarig, "Action has no frame range")

    # Now assign it properly.
    action_setup.subtarget = "Eye.L"
    assert bpy.ops.pose.cloudrig_generate() == {"FINISHED"}

    # Test shape key drivers with non-0/1 range.
    suzanne = bpy.data.objects["Suzanne"]
    assert suzanne.data.shape_keys.key_blocks["Blink.L"].value == 3.0
    assert suzanne.data.shape_keys.key_blocks["Blink.R"].value == -1.0

    # We have an assert for disabled actions, let's prod it.
    action_setup.enabled = False
    assert bpy.ops.pose.cloudrig_generate() == {"FINISHED"}
    assert not has_log_entry(metarig, "Generation Failed!")
