"""I3 Scene graph / object inventory — one record per image, objects with presence + position.
Vocabulary (canonical room only): tv_crt, tv_stand_oak, poster_pet_om_up, blue_mask, poster_pink_creature,
chair_pink_wingback, rug_round_pink, floor_lamp, side_table_blue, mug_steaming, window_sunset_4pane,
coffee_table_pink, table_lamp, neon_tube, ceiling_purple, floor_pink, doorway_frame, person.
Presence is eye-verified per image in this job (see corrected-labels-20261101.json), not guessed
from the filename. Absent = out of frame / not drawn, not 'missing from the room'.
"""
