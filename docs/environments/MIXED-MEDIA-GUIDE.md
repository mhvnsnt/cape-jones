# Mixed-Media Environment Guide

How Cape Jones handles environments, stealing from the best.

## The Approach: Gumball-Style Mixed Media

Cape Jones uses **mixed media environments** — real photographic backgrounds with animated characters on top. This is the Gumball method.

### How Gumball Does It

From the production files in `mhvnsnt/cn-gigaleak-gumball`:
- Backgrounds are **real photographs** — shot on location, not drawn
- Characters are 2D (Flash/Toon Boom) composited on top
- The show bible specifies: "2D+3D in live-action setting"
- Key technique: **match the lighting direction** between photo and character, but keep the character flat and graphic against the photo's depth

### Our Pipeline for Mixed Media

1. **Background plate**: Real photo (shot on phone, pulled from the internet, or AI-generated)
2. **Character**: AI-matted with transparent alpha (rembg/RVM — never chroma key)
3. **Composite**: Character layered over photo in Natron or ffmpeg
4. **Grade**: Apply a `cj-*` or `outside-*` grade to unify the composite
5. **Rim light**: If the character needs separation from a busy photo background, the grade's contrast curve handles it

### The Flying Scene Precedent

The owner's flying scene already does this — Cape Jones (hand-drawn) flying in front of a **real photo of a brick building**. That wasn't a placeholder. That's the show's visual language.

## Expressive Color: Ed, Edd n Eddy Philosophy

Ed, Edd n Eddy doesn't use realistic colors. The show uses **emotional color** — the environment is colored by how the scene *feels*, not what it *looks like*.

### The Approach

- **Skies aren't blue.** They can be purple, green, orange — whatever the mood needs.
- **Grass isn't green.** It's whatever green the scene needs, pushed to an extreme.
- **Shadows are colored**, not black. Purple shadows, blue shadows, red shadows.
- **Saturation is a dial**, not a setting. Crank it for energy, drain it for dread.

### Our `outside-*` Grades

This is exactly what the `outside-acid`, `outside-dusk`, `outside-storm`, and `outside-noir` grades do. They're the Ed, Edd n Eddy color philosophy as ffmpeg filter chains:
- `outside-acid` = hyper-saturated emotional color
- `outside-storm` = drained, ominous, pre-fight dread
- `outside-dusk` = blue-hour melancholy with warm hope in the highlights
- `outside-noir` = stripped to almost nothing, violet ghost in a grey world

### Rule

When the owner says "you have the reins on the lighting/grading" for an exterior scene, the `outside-*` grades are the starting point. Pick the emotional tone, apply the grade, adjust from there.

## Texture: Chowder Pattern Technique

From `chowder-ref/GREENBLATT-PATTERN-TECHNIQUE.md` (Greenblatt's own explanation):

> The character has HOLES cut in it. The character moves OVER a static pattern.

The pattern doesn't move with the character — it's fixed in screen space. The character slides over it. This creates the signature Chowder look where clothing patterns stay put while the body moves.

### Application to Environments

- **Wallpaper patterns** in the house can use this — fixed pattern, camera/character moves over it
- **Trippy backgrounds** for the Wizard Gang-style scenes — the pattern stays fixed while Cape Jones moves through it
- Implementation: `pattern_fill_v2.py` + ffmpeg track-matte in `chowder-fx/`

### When to Use

- Interior walls with bold patterns (the ghost cave?)
- Trippy/multicolor dream sequences
- Anywhere you want that uncanny "the texture isn't attached to the object" feel

## ATHF House Reference

Aqua Teen Hunger Force: the house is **aggressively normal**. A basic suburban rental. The comedy comes from how mundane the setting is contrasted with how absurd the characters are.

Cape Jones's house follows this exactly — see `HOUSE-DESIGN.md`. The house is boring. The guy in the white suit with the purple cowl doing the cup-lift in the recliner is not.

## Putting It Together: Scene Recipe

For a typical Cape Jones scene:

1. **Pick the location**: House interior? Beach exterior? Ghost cave?
2. **Background**: Real photo (exterior) or simple drawn room (interior)
3. **Character**: Hand-drawn by owner on FlipaClip, or rigged cutout
4. **Lighting**:
   - In-house → LED controller preset (he hits the button)
   - Outside → `cj-*` or `outside-*` grade (owner's call or assistant's reins)
   - Ghost cave → `cj-ghost` or `ghost-mode` LED (locked)
5. **Composite**: Natron or ffmpeg overlay
6. **Grade**: `finish.py --grade <chosen>`
7. **Audio**: Nosferatu (intro), Ghost Surf Rock (action), Orbiting Nebulas (trippy)
8. **Deliver**: `finish.py` handles the final encode
