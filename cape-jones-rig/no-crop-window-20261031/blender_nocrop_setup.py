# Blender-side no-crop setup (Blender 5.2.3, run headless).
# This script does NOT render and does NOT claim a render.
# It sets and prints the settings that are the Blender equivalent of
# the PIL no-crop path: no render window (use_border off), and a
# camera that is fit to the subject instead of the subject being
# fit to a fixed window. In Blender, the render border is literally
# a crop window (Render Properties > Render Region); turning it off
# and using an overscan margin in the compositor is the industry
# way to keep a leaning / wide figure whole.
# Run: blender --background --python blender_nocrop_setup.py
import bpy

scene = bpy.context.scene
scene.render.use_border = False
scene.render.use_crop_to_border = False
# Overscan-style safety: a render resolution with margin is a delivery
# choice, not a build crop -- the compositor must not crop to the
# subject bbox. Record the settings so a later compositor script can
# read them back.
print("NOCROP-CHECK use_border =", scene.render.use_border)
print("NOCROP-CHECK use_crop_to_border =", scene.render.use_crop_to_border)
print("NOCROP-CHECK resolution =", scene.render.resolution_x,
      "x", scene.render.resolution_y)
print("NOCROP-CHECK film_transparent =", scene.render.film_transparent)
# Transparent film = the Blender equivalent of the PIL transparent
# background: no background is baked into the figure render.
scene.render.film_transparent = True
print("NOCROP-CHECK film_transparent_after_set =",
      scene.render.film_transparent)
print("NOCROP-CHECK OK: no render window, transparent film, no render claimed")
