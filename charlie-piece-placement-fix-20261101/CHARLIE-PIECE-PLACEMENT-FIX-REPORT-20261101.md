# Charlie piece-placement fix v3 — 2026-11-01
Approval: 0/1 — Mars has not seen v3 yet. Local only at build time, no reskin/recolor. Original Charlie fix untouched.

Strings on mouth: body_thingies, 0/285 points inside body_mask, so v3 omits them, does not move them. Not neck hairs (Head>pubes, stay in head), not drawstrings (no such symbol in Charlie's 18-symbol library).
Arms: Front (+214,+287) pivot to right shoulder (860,887). Back (+32,+336) to left shoulder (402,948).
Head: no neck, offset (+17,+435), hood (+42,+361). Assembled 56-972, 475-1696, 916x1221.
MP4: 1920x1080, 24fps, 96f, 4.0s, 392,732 B, md5 6d5b976ac429da544f01e96537c3fe2b. GIF md5 94153bd2d8adcaf997e505fc7a820576. SFX same synthesized md5 687c6e8e3a03bbd89bff0569cd8a6c46.
Still off: hat white strip, mouth frame 0/25 only, back hoodie mostly hidden, wave hand edge touch, head edge sticks out. True Animate render still needed.
Charlie-level count corrected in v3: 8, not 9 — Charlie, Pim, Gumball, Darwin, Anais, Dad, Mom, Max. Ruby excluded (build file, size ref only).
