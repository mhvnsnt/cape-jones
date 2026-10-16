# Cape Jones Color Grades

All grades built from the 14 model sheets. Tuned for the locked palette:
- **Suit #FFFFFF** — protected in signature grades, stays blown out
- **Cowl #3E1473** — saturation punched
- **Skin #E5B28C** — kept warm and natural
- **Cape #000000** — deepened, not crushed

Model-sheet law: environment color applies to rim lights only, never tints the suit (signature grades). LED presets intentionally tint everything — that's what real RGB strips do.

## Signature Grades

| Grade | Name | Description | Use When |
|-------|------|-------------|----------|
| `cj-day` | Signature Day | Default. Punchy cartoon, violet cowl pop, whites protected. | Neutral indoor/outdoor |
| `cj-night` | Signature Night | Dark variant. | Night scenes, ghost cave |
| `cj-trippy` | Signature Trippy | Saturated for trippy backgrounds. | Wizard Gang-style scenes |

## Model-Sheet Color Families

Built from the colors the owner loves in the sheets — blues, reds, purples, yellows.

| Grade | Name | Description | Use When |
|-------|------|-------------|----------|
| `cj-royal` | Royal Violet | Deep violet wash from the cowl color #3E1473. | Hero moments, Cape Jones in his element |
| `cj-ocean` | Ocean Blue | Cyan/blue, rim-light cyan pushed. Beach vibe. | Beach, water scenes |
| `cj-ember` | Ember Red | Red/orange like the model sheet nebula panel. | Action, fight, intensity |
| `cj-gold` | Gold Hour | Warm #FFB300 energy-glow feel. | Victory, power-up moments |
| `cj-ghost` | Ghost Teal | Spooky green-teal. Cowl violet reads through. | Supernatural, spooky |
| `cj-beach-day` | Beach Day | Bright saturated Halloween-on-the-beach. | Beach daytime exterior |
| `cj-beach-sunset` | Beach Sunset | Orange/pink golden hour. | Sunset exterior |

## Outside / Creative Grades

For exterior scenes where the owner gives creative control. These push harder — expressive, non-naturalistic color in the Ed, Edd n Eddy spirit.

| Grade | Name | Description | Use When |
|-------|------|-------------|----------|
| `outside-noir` | Noir | Near-B&W with violet retention. Ghost in a noir film. | Dramatic exterior |
| `outside-acid` | Acid Candy | Hyper-saturated. Non-realistic emotional color. | High-energy exterior |
| `outside-dusk` | Dusk | Blue-hour, warm highlights. | Flying at sunset |
| `outside-storm` | Storm | Desaturated teal-grey. Pre-fight tension. | Ominous exterior |

## Static LED Reference Looks

Single-frame references for each animated LED preset. Used for thumbnails, storyboards, and when you need the "starting frame" of a preset.

| Grade | Matches Preset |
|-------|---------------|
| `led-chill-blue` | `chill-blue` |
| `led-deep-purple` | `purple-pulse` |
| `led-sunset` | `sunset-cycle` |
| `led-party` | `party-strobe` / `rainbow-smooth` |
| `led-ghost-teal` | `ghost-mode` |
| `led-ember` | `ember-glow` |

## Usage

```bash
# Apply a grade in the finishing stage
python3 ~/workspace/tools/post-pipeline/finish.py input.mp4 output.mp4 --grade cj-royal

# With audio
python3 ~/workspace/tools/post-pipeline/finish.py input.mp4 output.mp4 --grade cj-ember --audio music.mp3

# List all grades
python3 ~/workspace/tools/post-pipeline/finish.py --list-grades

# Skip grading
python3 ~/workspace/tools/post-pipeline/finish.py input.mp4 output.mp4 --grade none
```

## Preview Frames

Preview renders for each grade are in `lighting/previews/` — generated from a real frame of the expressions video so you can see exactly what each grade does to the character.

## Adding New Grades

1. Add the filter chain to `~/workspace/tools/post-pipeline/grades.py`
2. Register it in `GRADES` dict and `GRADE_INFO` for docs
3. Generate a preview: extract a frame, run through the grade
4. Document it here
5. Push to repo (branch → PR → merge)
