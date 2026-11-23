#!/usr/bin/env python3
"""Speech card PNG for the BROTHERMAN scene test (transparent, 1280x170).
Shown f61-144 while he points and delivers the line. SILENT — the card
carries the line because voice is owner-gated. No synthesized voice."""
from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
card = Image.new("RGBA", (1280, 170), (0, 0, 0, 0))
d = ImageDraw.Draw(card)
# box: top strip, near-black with teal left bar
d.rounded_rectangle([30, 12, 1250, 158], radius=18,
                    fill=(10, 10, 14, 215), outline=(15, 118, 110, 255), width=5)
d.rectangle([30, 12, 52, 158], fill=(15, 118, 110, 255))
f1 = ImageFont.truetype(FONT, 34)
f2 = ImageFont.truetype(FONT, 40)
d.text((78, 26), "BROTHERMAN:", font=f1, fill=(15, 200, 185, 255))
d.text((78, 70), "\u201cYou just gotta motherfucking", font=f2, fill=(255, 255, 255, 255))
d.text((78, 116), "keep up with the Joneses, brother.\u201d", font=f2, fill=(255, 255, 255, 255))
card.save("/home/hatch/workspace/_cape-jones-parking-lot-2d/brotheman/speechcard.png")
print("speechcard.png saved")
