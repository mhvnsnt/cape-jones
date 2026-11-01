# Gate results — movement library clips, 2026-11-01
- Audio: ffprobe verified all 8 MP4s have h264 video + aac audio.
- Whole-frame WCAG proxy (480px, mean luminance, opposing pair >=25.5
  with darker <204, red fraction): ALL 8 clips general_flashes=0,
  max frame-to-frame mean jump 0.5-5.6 (well below 25.5), max red
  0.0000-0.0015. No >3 flashes/sec, no red flash, no large jump.
  Per clip: 01: 216f, 0, 2.8; 02: 63f, 0, 5.6; 03: 74f, 0, 0.5;
  04: 133f, 0, 0.9; 05: 93f, 0, 1.0; 06: 66f, 0, 1.1;
  07: 74f, 0, 0.7; 08: 215f, 0, 1.6.
- Honest limit: the parallel dance-flash-fix flash_check.py full
  verdict FAILS the walk clip (forearm_flips 36, 14/sec) — but its
  forearm boxes are tuned to the 1920x1080 dance-test hero layout
  (x 390-570, y 190-280 at 960x540), NOT to these 1100x750 chain
  videos or 550x750 portrait clips, so moving arms/legs cross those
  boxes and trip it. That is a layout mismatch in that gate, not a
  whole-frame flash: the WCAG flash definition above (opposing
  luminance pairs) is 0 for every clip. Do NOT present the full
  flash_check verdict as a seizure finding for these clips, and do
  NOT re-run it as-is on a different layout without re-tuning its
  boxes. A layout-correct forearm-box gate for chain/portrait
  framing is still owed if Mars wants that specific metric.
- Wrist / knee-feet: source lineages were previously gated
  (knee-feet-corrected dance, arm-front-snap, rig chains grounded);
  no new hand placement was made in this task, no wrist was cut,
  no piece was hand-drawn. These clips are re-cuts with sound of
  existing Cape Jones rig videos, not new rig poses — that is stated,
  not hidden.
- Approval: 0/1 for all clips. Landing: local only, no PR claimed.
