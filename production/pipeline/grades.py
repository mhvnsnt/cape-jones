#!/usr/bin/env python3
"""
grades.py — Cape Jones color grade library.

Every grade is an ffmpeg filter chain. Built from the 14 model sheets,
tuned for the locked palette:
  - Suit #FFFFFF (pure white) — protected in signature grades, stays blown out
  - Cowl #3E1473 (deep violet) — saturation punched
  - Skin #E5B28C — kept warm and natural
  - Cape #000000 (absolute black) — deepened, not crushed
  - Rim light: cyan 2-4px, environment-matched
  - Energy: core #FFFFFF, outer glow #FFB300 (color dodge/add)

Model-sheet law: environment color applies to RIM LIGHTS only, never tints
the suit. Signature/outside grades protect whites via curves. LED presets
(in-house) intentionally tint the whole frame — that's what RGB LED strips
do to a real room.

Grade families:
  cj-*        Signature grades (whites protected)
  led-*       Static LED looks (for reference frames / thumbnails)
  outside-*   Creative exterior grades (assistant has creative control)
"""

# ---------------------------------------------------------------------------
# SIGNATURE GRADES (whites protected — suit never tints)
# ---------------------------------------------------------------------------

CJ_DAY = (
    # Punch violet/magenta (cowl #3E1473) without touching whites
    "colorchannelmixer="
    "rr=1.05:rg=0.0:rb=0.05:"
    "gr=0.0:gg=1.0:gb=0.05:"
    "br=0.08:bg=0.0:bb=1.10,"
    "eq=saturation=1.35:contrast=1.08:brightness=0.005,"
    # Curve: deepen blacks slightly, lift midtones, protect pure white
    "curves=all='0/0.015 0.25/0.23 0.5/0.52 0.75/0.78 0.98/0.99 1/1',"
    "unsharp=5:5:0.4"
)

CJ_NIGHT = (
    # Darker variant for night / ghost-cave scenes
    "colorchannelmixer="
    "rr=1.0:rg=0.0:rb=0.08:"
    "gr=0.0:gg=0.95:gb=0.08:"
    "br=0.10:bg=0.0:bb=1.15,"
    "eq=saturation=1.25:contrast=1.15:brightness=-0.02,"
    "curves=all='0/0.0 0.25/0.20 0.5/0.48 0.75/0.75 1/0.98',"
    "unsharp=5:5:0.4"
)

CJ_TRIPPY = (
    # Wizard Gang-style trippy graffiti background scenes
    "colorchannelmixer="
    "rr=1.10:rg=0.05:rb=0.10:"
    "gr=0.05:gg=1.05:gb=0.10:"
    "br=0.10:bg=0.05:bb=1.15,"
    "eq=saturation=1.60:contrast=1.10:brightness=0.01,"
    "curves=all='0/0.02 0.5/0.55 1/1',"
    "unsharp=5:5:0.5"
)

# ---------------------------------------------------------------------------
# MODEL-SHEET COLOR FAMILIES (owner's favorites: blues, reds, purples, yellows)
# ---------------------------------------------------------------------------

CJ_ROYAL = (
    # Deep violet wash — cowl color #3E1473 as the environment.
    # Cape Jones in his element. Whites protected.
    "colorchannelmixer="
    "rr=1.08:rg=0.02:rb=0.12:"
    "gr=0.0:gg=0.95:gb=0.08:"
    "br=0.15:bg=0.02:bb=1.20,"
    "eq=saturation=1.45:contrast=1.10:brightness=0.0,"
    "curves=all='0/0.01 0.3/0.28 0.6/0.60 0.9/0.92 1/1',"
    "unsharp=5:5:0.4"
)

CJ_OCEAN = (
    # Cyan/blue environment — beach vibe, rim-light cyan pushed.
    # "Halloween on the beach" daytime water feel.
    "colorchannelmixer="
    "rr=0.95:rg=0.0:rb=0.05:"
    "gr=0.0:gg=1.05:gb=0.10:"
    "br=0.05:bg=0.10:bb=1.15,"
    "eq=saturation=1.40:contrast=1.08:brightness=0.01,"
    "curves=all='0/0.015 0.5/0.52 1/1',"
    "unsharp=5:5:0.4"
)

CJ_EMBER = (
    # Red/orange wash — matches the model sheet's environment-bleed panel
    # (red nebula background). Action / intensity scenes.
    "colorchannelmixer="
    "rr=1.15:rg=0.05:rb=0.0:"
    "gr=0.05:gg=0.95:gb=0.0:"
    "br=0.0:bg=0.0:bb=1.0,"
    "eq=saturation=1.40:contrast=1.12:brightness=0.0,"
    "curves=all='0/0.01 0.3/0.27 0.7/0.70 1/0.99',"
    "unsharp=5:5:0.4"
)

CJ_GOLD = (
    # Warm yellow/gold — #FFB300 energy-glow feel across the frame.
    # Victory moments, power-up scenes, warm interiors.
    "colorchannelmixer="
    "rr=1.10:rg=0.08:rb=0.0:"
    "gr=0.05:gg=1.05:gb=0.0:"
    "br=0.0:bg=0.05:bb=0.95,"
    "eq=saturation=1.35:contrast=1.08:brightness=0.015,"
    "curves=all='0/0.02 0.5/0.53 1/1',"
    "unsharp=5:5:0.4"
)

CJ_GHOST = (
    # Spooky green-teal — ghost cave, supernatural scenes.
    # Eerie but the cowl violet still reads through.
    "colorchannelmixer="
    "rr=0.90:rg=0.05:rb=0.0:"
    "gr=0.05:gg=1.10:gb=0.10:"
    "br=0.0:bg=0.12:bb=1.05,"
    "eq=saturation=1.35:contrast=1.12:brightness=-0.01,"
    "curves=all='0/0.0 0.3/0.26 0.7/0.68 1/0.98',"
    "unsharp=5:5:0.4"
)

CJ_BEACH_DAY = (
    # Bright, warm, saturated — Halloween-on-the-beach daytime.
    # High key, playful, saturated sky colors.
    "colorchannelmixer="
    "rr=1.08:rg=0.03:rb=0.02:"
    "gr=0.02:gg=1.05:gb=0.05:"
    "br=0.02:bg=0.05:bb=1.08,"
    "eq=saturation=1.50:contrast=1.05:brightness=0.02,"
    "curves=all='0/0.03 0.5/0.54 1/1',"
    "unsharp=5:5:0.4"
)

CJ_BEACH_SUNSET = (
    # Orange/pink sky — golden hour on the beach.
    # Warm wash, long-shadow feel, romantic action lighting.
    "colorchannelmixer="
    "rr=1.18:rg=0.06:rb=0.02:"
    "gr=0.04:gg=1.0:gb=0.04:"
    "br=0.02:bg=0.02:bb=1.05,"
    "eq=saturation=1.45:contrast=1.10:brightness=0.01,"
    "curves=all='0/0.015 0.4/0.40 0.8/0.82 1/1',"
    "unsharp=5:5:0.4"
)

# ---------------------------------------------------------------------------
# OUTSIDE / CREATIVE GRADES (assistant has creative control per owner)
# These push harder — expressive, non-naturalistic color.
# ---------------------------------------------------------------------------

OUTSIDE_NOIR = (
    # High-contrast black-and-white with violet retention.
    # Cape Jones as a ghost in a noir film.
    "colorchannelmixer="
    "rr=0.9:rg=0.1:rb=0.3:"
    "gr=0.1:gg=0.8:gb=0.3:"
    "br=0.2:bg=0.2:bb=1.0,"
    "eq=saturation=0.35:contrast=1.30:brightness=-0.03,"
    "curves=all='0/0.0 0.25/0.18 0.75/0.78 1/0.97',"
    "unsharp=5:5:0.5"
)

OUTSIDE_ACID = (
    # Hyper-saturated candy — Ed, Edd n Eddy energy.
    # Non-realistic, emotional color. Skies go weird.
    "eq=saturation=2.0:contrast=1.15:brightness=0.01,"
    "colorchannelmixer="
    "rr=1.12:rg=0.0:rb=0.08:"
    "gr=0.0:gg=1.08:gb=0.08:"
    "br=0.08:bg=0.0:bb=1.12,"
    "curves=all='0/0.02 0.5/0.53 1/1',"
    "unsharp=5:5:0.5"
)

OUTSIDE_DUSK = (
    # Blue-hour exterior — deep blue shadows, warm highlights.
    # Flying-into-the-sunset scenes.
    "colorchannelmixer="
    "rr=1.0:rg=0.0:rb=0.10:"
    "gr=0.0:gg=0.95:gb=0.12:"
    "br=0.08:bg=0.05:bb=1.18,"
    "eq=saturation=1.30:contrast=1.15:brightness=-0.015,"
    "curves=all='0/0.0 0.35/0.30 0.7/0.70 1/0.99',"
    "unsharp=5:5:0.4"
)

OUTSIDE_STORM = (
    # Desaturated teal-grey — ominous, heavy sky.
    # Before-the-fight tension.
    "colorchannelmixer="
    "rr=0.92:rg=0.03:rb=0.03:"
    "gr=0.03:gg=1.02:gb=0.08:"
    "br=0.03:bg=0.08:bb=1.08,"
    "eq=saturation=0.85:contrast=1.20:brightness=-0.02,"
    "curves=all='0/0.0 0.4/0.35 0.8/0.78 1/0.97',"
    "unsharp=5:5:0.4"
)

# ---------------------------------------------------------------------------
# STATIC LED LOOKS (single-frame reference for each LED preset)
# ---------------------------------------------------------------------------

LED_CHILL_BLUE = (
    "colorchannelmixer=rr=0.85:rg=0.0:rb=0.15:gr=0.0:gg=0.95:gb=0.20:"
    "br=0.10:bg=0.15:bb=1.25,"
    "eq=saturation=1.30:contrast=1.05:brightness=0.0,"
    "curves=all='0/0.02 0.5/0.50 1/0.98'"
)

LED_DEEP_PURPLE = (
    "colorchannelmixer=rr=1.0:rg=0.0:rb=0.25:gr=0.0:gg=0.80:gb=0.15:"
    "br=0.20:bg=0.05:bb=1.30,"
    "eq=saturation=1.40:contrast=1.10:brightness=-0.01,"
    "curves=all='0/0.01 0.5/0.48 1/0.97'"
)

LED_SUNSET = (
    "colorchannelmixer=rr=1.25:rg=0.10:rb=0.0:gr=0.08:gg=0.95:gb=0.05:"
    "br=0.05:bg=0.05:bb=1.10,"
    "eq=saturation=1.45:contrast=1.08:brightness=0.01,"
    "curves=all='0/0.02 0.5/0.52 1/0.99'"
)

LED_PARTY = (
    "eq=saturation=1.80:contrast=1.12:brightness=0.02,"
    "colorchannelmixer=rr=1.15:rg=0.05:rb=0.10:gr=0.05:gg=1.05:gb=0.10:"
    "br=0.10:bg=0.05:bb=1.15,"
    "curves=all='0/0.02 0.5/0.53 1/1'"
)

LED_GHOST_TEAL = (
    "colorchannelmixer=rr=0.80:rg=0.08:rb=0.05:gr=0.08:gg=1.15:gb=0.15:"
    "br=0.05:bg=0.18:bb=1.10,"
    "eq=saturation=1.35:contrast=1.10:brightness=-0.01,"
    "curves=all='0/0.01 0.5/0.48 1/0.97'"
)

LED_EMBER = (
    "colorchannelmixer=rr=1.30:rg=0.12:rb=0.0:gr=0.10:gg=0.90:gb=0.0:"
    "br=0.0:bg=0.02:bb=0.95,"
    "eq=saturation=1.40:contrast=1.10:brightness=0.0,"
    "curves=all='0/0.015 0.5/0.50 1/0.98'"
)


# ---------------------------------------------------------------------------
# REGISTRY
# ---------------------------------------------------------------------------
GRADES = {
    # Signature (whites protected)
    "cj-day":      CJ_DAY,
    "cj-night":    CJ_NIGHT,
    "cj-trippy":   CJ_TRIPPY,
    # Backwards compat with finish.py v1 names
    "cape-jones":       CJ_DAY,
    "cape-jones-night": CJ_NIGHT,
    "cape-jones-trippy": CJ_TRIPPY,
    # Model-sheet color families
    "cj-royal":        CJ_ROYAL,
    "cj-ocean":        CJ_OCEAN,
    "cj-ember":        CJ_EMBER,
    "cj-gold":         CJ_GOLD,
    "cj-ghost":        CJ_GHOST,
    "cj-beach-day":    CJ_BEACH_DAY,
    "cj-beach-sunset": CJ_BEACH_SUNSET,
    # Outside / creative (assistant's playground)
    "outside-noir":  OUTSIDE_NOIR,
    "outside-acid":  OUTSIDE_ACID,
    "outside-dusk":  OUTSIDE_DUSK,
    "outside-storm": OUTSIDE_STORM,
    # Static LED looks
    "led-chill-blue":  LED_CHILL_BLUE,
    "led-deep-purple": LED_DEEP_PURPLE,
    "led-sunset":      LED_SUNSET,
    "led-party":       LED_PARTY,
    "led-ghost-teal":  LED_GHOST_TEAL,
    "led-ember":       LED_EMBER,
    # Bypass
    "none": "",
}

# Human-readable metadata for docs and UI
GRADE_INFO = {
    "cj-day": ("Signature Day", "Default grade. Punchy cartoon, violet cowl pop, whites protected.", "indoor/outdoor neutral"),
    "cj-night": ("Signature Night", "Dark variant for night scenes and ghost cave.", "night / ghost cave"),
    "cj-trippy": ("Signature Trippy", "Saturated for Wizard Gang-style trippy backgrounds.", "trippy scenes"),
    "cj-royal": ("Royal Violet", "Deep violet wash from the cowl color. Cape Jones in his element.", "hero moments"),
    "cj-ocean": ("Ocean Blue", "Cyan/blue beach vibe. Rim-light cyan pushed.", "beach / water"),
    "cj-ember": ("Ember Red", "Red/orange like the model sheet nebula panel. Intensity.", "action / fight"),
    "cj-gold": ("Gold Hour", "Warm #FFB300 energy-glow feel. Victory, power-up.", "power moments"),
    "cj-ghost": ("Ghost Teal", "Spooky green-teal. Supernatural scenes.", "ghost cave / spooky"),
    "cj-beach-day": ("Beach Day", "Bright saturated Halloween-on-the-beach daytime.", "beach day exterior"),
    "cj-beach-sunset": ("Beach Sunset", "Orange/pink golden hour.", "sunset exterior"),
    "outside-noir": ("Noir", "Near-B&W with violet retention. Ghost in a noir film.", "creative exterior"),
    "outside-acid": ("Acid Candy", "Hyper-saturated, Ed Edd n Eddy energy. Non-realistic.", "creative exterior"),
    "outside-dusk": ("Dusk", "Blue-hour exterior, warm highlights. Flying at sunset.", "creative exterior"),
    "outside-storm": ("Storm", "Desaturated teal-grey. Pre-fight tension.", "creative exterior"),
    "led-chill-blue": ("LED: Chill Blue", "Static reference for the chill-blue LED preset.", "LED reference"),
    "led-deep-purple": ("LED: Deep Purple", "Static reference for the purple-pulse LED preset.", "LED reference"),
    "led-sunset": ("LED: Sunset", "Static reference for the sunset-cycle LED preset.", "LED reference"),
    "led-party": ("LED: Party", "Static reference for the party-strobe LED preset.", "LED reference"),
    "led-ghost-teal": ("LED: Ghost Teal", "Static reference for the ghost-mode LED preset.", "LED reference"),
    "led-ember": ("LED: Ember", "Static reference for the ember-glow LED preset.", "LED reference"),
}


def get_grade(name):
    """Return the ffmpeg filter chain for a grade name. Falls back to cj-day."""
    if name not in GRADES:
        return GRADES["cj-day"]
    return GRADES[name]


def list_grades():
    """Return all grade names."""
    return sorted(GRADES.keys())
