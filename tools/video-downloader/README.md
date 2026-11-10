# Video Downloader + AI-Eyes (frame-stream analysis)

OUR OWN tool, written from scratch 2026-11-02. Not copied from facebooksave.com
or any other downloader site. It wraps yt-dlp (public, general-purpose)
and ffmpeg/ffprobe + Pillow. Public links only; no login bypass, no
paywall/DRM bypass, no private content, nothing re-uploaded.

## Download
```
python3 download_video.py <facebook|tiktok|youtube public url> [--out-dir DIR]
# -> <id>.mp4 + <id>.info.json (title, uploader, duration, fps, size)
```
YouTube currently bot-checks this VM without browser cookies
("Sign in to confirm you're not a bot") — that is a YouTube-side limit,
not a code bug; TikTok and Facebook public links are the working path
until a cookie export is supplied by the owner. No cookies are stored here.

## Watch (AI-Eyes = frame-stream analysis, NOT human eyes)
```
python3 watch_video.py <video.mp4> [--out-dir DIR]
# -> watch-report.json + contact-sheet.png
# streams at NATIVE fps, capped at 60 (never invents frames)
# motion per second, scene-change seconds, top-10 key-moment seconds
```

## Test, 2026-11-02
- YouTube "Me at the zoo" (jNQXAC9IVRw): BLOCKED by YouTube bot check.
- TikTok public sample 7383414354852465966: DOWNLOADED OK —
  404,672 bytes, 14.1 s, 720x1280, native 30 fps (streamed 30, not 60),
  423 frames extracted, median motion 1.169, top motion second 2 (1.993),
  0 scene changes. Test video itself is NOT in the repo (not our work);
  only its watch-report + contact sheet are kept, in test-watch/.
- Approval 0/1. Originals untouched.
