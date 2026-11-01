import json, pathlib, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
root = pathlib.Path.home()/"workspace/cape-jones-rig/donor-fla-rig-pull-20261101"
work = root/"work"; work.mkdir(parents=True, exist_ok=True)
# --- inventory from verified audits, no new downloads ---
inv = [
 {"show":"Gumball (Amazing World of Gumball)","remote_repo":"mhvnsnt/cn-gigaleak-gumball","local_evidence":"gumball-full-leak-file-list-20261031.json (2259 entries, listing only, NOT binaries)","fla_rig":"YES - S2 Rigs zip 62 .fla puppets+scenes, CN-Leaks-001 71 .fla, full RAR5 2259 files incl 20 dance FLAs / 10 unique Darwin dance scenes","swf":"53 + 54 SWF exports","layer_slots":"head comp, L/R fin, L/R leg, body layers; puppet slot structure","timeline_scene":"YES - KeyAnim GB202REMOTE Sc144/147, GB218Flakers Sc002/117; fight DARWIN_HURT_BACK_KICK Sc159, GUMBALL_HURT_FACEKICK Sc155, HURT_FLOOR Sc160, HURT_HIMSELF Sc158/161","dance_verified":"YES - ONLY verified performed dance in whole audit: Darwin 'The Words' GB214 Sc057 198f + Sc059 twist 105f, 25fps, ~14f beat ~107BPM, on twos, twist 32 keyframes f43-97","audio_on_disc":"NO - no Gumball .swf/.fla audio file is on local disc; SWF audio streams NOT parsed, NOT downloaded, NOT used","template_use":"Darwin dance timing + puppet slot structure -> Cape Jones dance/strut/twist; fight timing -> Cape Jones kick timing (kick itself still owed, foreshortened leg first)"},
 {"show":"Foster's Home - Frankie rig","remote_repo":"mhvnsnt/cn-gigaleak-fosters-home, release frankie-rig-fla-v1","local_evidence":"SHOW-REPO audits, Frankie parse summary (430 part comps, 6 pages)","fla_rig":"YES - 1 binary FLA pds3hx.fla, 430 part comps, 6 pages, turnarounds 3/4:118 / side:82 / 3/4-back:30 / front:28 / back:16, chin+mouth expression pair","swf":"Foster's flash zip: 7 .fla + 15 .swf reels (separate from Frankie rig)","layer_slots":"turnaround-page structure, part comps, chin+mouth expression pair","timeline_scene":"NO for Frankie rig - rig only, no performed scene in this file","dance_verified":"NOT VERIFIED - reels are long character reels, no dance identified","audio_on_disc":"NO - SWF headers parsed for fps/frames only (Berry 1847f, Bloo 2190f, Cheese 1892f, Coco 1808f, Ivan 1618f, Uncle Pockets 2031f, Wilt 1892f, all 24fps); audio stream content NOT parsed, NOT downloaded","template_use":"Frankie turnaround structure -> Cape Jones viseme/expression pages; reel 24fps timing -> Cape Jones pose-swap/gesture timing"},
 {"show":"Foster's Home - web reels","remote_repo":"mhvnsnt/cn-gigaleak-fosters-home, fosters-flash-v1","local_evidence":"SWF header parse in animation audit (fps+frames, not audio)","fla_rig":"NO rig file in this zip (Frankie is separate)","swf":"15 .swf, 7 .fla, Berry_v20.fla confirmed OLE binary (6981106 compressed -> 19509760 bytes)","layer_slots":"reel timelines, binary-era FLA","timeline_scene":"YES - reels, 1618-2190f @24fps, not a single performed scene","dance_verified":"NOT VERIFIED","audio_on_disc":"NO - see Frankie row","template_use":"24fps reel timing -> Cape Jones gesture/pose-swap holds"},
 {"show":"Smiling Friends - Charlie + Pim","remote_repo":"mhvnsnt/cn-gigaleak-cartoon-vault, release tv-gigaleak-fla-v1","local_evidence":"SHOW-REPO audits + RIG-DISSECTION summary","fla_rig":"YES - 2 XFL FLAs, Animate 22, 1920x1080: Charlie 82390 B, PimRigUpdate 296483 B","swf":"0","layer_slots":"Charlie 9 layers: front_arm, body_move, body_mask, body_thingies, body, head, body_back, legs, back_arm; Pim 5 layers; head sub-symbols, pupil/brow/lid symbols, pupil PARENT wrapper, mask layers","timeline_scene":"NO - scene timelines EMPTY, rigs only","dance_verified":"NO","audio_on_disc":"NO - no audio verified in either rig FLA; timelines empty","template_use":"9/5-layer stack + frame-addressed swap libraries -> Cape Jones front order + mouth/leg swap timing; mouth 25 -> Cape Jones mouth 5 (see lip-sync section)"},
 {"show":"Randy Cunningham","remote_repo":"mhvnsnt/cn-gigaleak-cartoon-vault, randy-cunningham-v1","local_evidence":"animation audit central-directory listing (19 entries)","fla_rig":"YES - 6 .fla (ejq323, mi2y6f, pux9h5 88.8MB, sercad, 0xmvez, dulzh3; ejq323=0xmvez duplicate by size/CRC)","swf":"4 .swf RC118_SC001 L02/L03/L05/L06 + 1 After Effects project RC118_SC001_T1.aep + BG .ai","layer_slots":"saved scene, layered for compositing (Flash exports + BG + AE comp)","timeline_scene":"YES - saved scene RC118_SC001","dance_verified":"NOT VERIFIED","audio_on_disc":"UNKNOWN / NOT VERIFIED - no audio file on local disc, scene audio NOT parsed","template_use":"Scene layer structure -> Cape Jones scene assembly in Blender compositor; FLA XFL-vs-binary check still owed"},
 {"show":"Nick single-show (unidentified show in audit)","remote_repo":"Nick 2024 zip, 1610 entries (listing, not local binaries)","local_evidence":"animation audit listing","fla_rig":"YES, different format - 8 Maya .ma rigs (character v041, location v008, noodle-arm/hands/feet/noodle-wrap/catcher props)","swf":"0; 4 Alembic .abc baked caches f1-182, 183-244, 244-399, 400-586","layer_slots":"Maya rig hierarchy + baked cache frames","timeline_scene":"YES - baked caches, not a timeline; 1 dance video timing only, show unidentified","dance_verified":"TIMING ONLY, show unidentified - do NOT label it as a named show dance","audio_on_disc":"LISTED ONLY, NOT ON DISC - 1028 audio files listed in remote zip, content unknown, NOT downloaded, NOT used, NOT claimed as voice lines","template_use":"Baked-cache timing -> Cape Jones walk timing; .abc imports natively in Blender (free route, not tested here)"},
 {"show":"Cartoon Vault unsorted - ch_max / ch_ruby","remote_repo":"mhvnsnt/cn-gigaleak-cartoon-vault, tv-gigaleak-fla-v1","local_evidence":"animation audit XFL parse summaries","fla_rig":"YES - ch_max 57.4MB, 677 symbols (224 multi-keyframe / 453 single-frame); ch_ruby 44.1MB, 175 symbols (134 multi-keyframe)","swf":"0","layer_slots":"multi-view part-swap puppet + pose-library sheet; build-vs-reference layer separation, variant-as-layer-set","timeline_scene":"NO - ch_max stage = 46-frame HOLD pose-library sheet; ch_ruby all single holds; build files, not performances","dance_verified":"NO","audio_on_disc":"NO","template_use":"Pose-library sheet system -> Cape Jones pose library / variant layer sets"},
 {"show":"Cartoon Vault unsorted - other 7 FLAs","remote_repo":"same vault release","local_evidence":"format-level listing only","fla_rig":"FORMAT ONLY - alien/earth/BOSS/BG/poster FLAs, 9.4-57.4MB, content UNEXAMINED","swf":"unknown","layer_slots":"unknown","timeline_scene":"UNKNOWN","dance_verified":"UNKNOWN","audio_on_disc":"UNKNOWN - not on disc","template_use":"NONE until one file is parsed; do NOT assume a show from filename"},
 {"show":"Disney FLA rar","remote_repo":"mhvnsnt/cn-gigaleak-bonus-non-cn","local_evidence":"12-entry listing only","fla_rig":"1 .fla BY FILENAME ONLY: ww226_26s_016_final.fla (39.9MB unpacked), content NOT downloaded","swf":"0","layer_slots":"unknown","timeline_scene":"UNKNOWN","dance_verified":"NO evidence","audio_on_disc":"UNKNOWN - not on disc","template_use":"NONE until content check (XFL/binary) is done"},
 {"show":"Teen Titans, Powerpuff Girls, Scooby, Johnny Bravo, etc.","remote_repo":"multiple CN repos, listed in audits","local_evidence":"central-directory listings, 0 .fla/.swf in the archives checked","fla_rig":"NO - 0 .fla/.swf in Teen Titans x3, PPG original, Scooby (0 .fla), Johnny Bravo model sheets only","swf":"0 (Scooby ep607 animatic .mov is baked video only)","layer_slots":"model sheets / expression sheets / QTVR turnarounds only","timeline_scene":"NO - baked video / animatic timing only","dance_verified":"NO","audio_on_disc":"NO donor audio on disc","template_use":"Pose/expression reference + animatic timing only; do NOT invent a rig where none exists"},
]
(root/"INVENTORY-20261101.json").write_text(json.dumps(inv, indent=2))
# --- placeholder structure diagram (text, no donor art) ---
img = Image.new("RGB",(1200,900),"white"); d=ImageDraw.Draw(img)
try: font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",20)
except: font=None
d.text((20,20),"TEMPLATE-PLACEHOLDER ONLY - NO DONOR ART IN THIS IMAGE",fill=(200,0,0),font=font)
lines=[
 "Gumball puppet slots -> Cape Jones: head comp -> Head_Front, L/R fin -> Arm_Back/Front,",
 "  L/R leg -> Leg_Back/Front, body layers -> Torso_Chest/Pelvis",
 "Frankie 430 comps / turnarounds -> Cape Jones viseme pages + front/side/3-4/back views",
 "Charlie 9 layers -> Cape Jones front order: Cape_Back, Leg_Back, Leg_Front, Arm_Back,",
 "  Pelvis, Torso, Neck, Head, Arm_Front  |  Pim 5 layers -> simplified Cape Jones stack",
 "Randy scene -> Flash exports + BG + AE comp -> Blender compositor scene assembly",
 "Nick Maya/.abc -> baked cache frames -> Blender .abc import (not tested here)",
 "ch_max/ch_ruby -> pose-library sheet, variant-as-layer-set",
 "RESKIN PATH (every character): TEMPLATE-PLACEHOLDER -> kitbash -> reskin ->",
 "  redesign -> COMPLETELY DIFFERENT ORIGINAL, new name, no donor name/logo/dialogue/voice",
 "RELEASE GATE: final deliverable containing donor art/voice/lines = FAIL, do not ship.",
]
y=70
for ln in lines:
    d.text((20,y),ln,fill=(0,0,0),font=font); y+=32
img.save(root/"PLACEHOLDER-STRUCTURE-20261101.png")
# --- lip-sync timing table, Cape Jones 5 mouths, 24fps, no donor lines ---
# syllable grid: 5.58s clip04 base, but talking test will be 4.0s @24fps = 96f
mouths=["Closed","Open","Teeth","Shout","Smile"]
# pattern: rest, vowel, fricative, stressed, hold, repeat - no words, no donor lines
seq=[]
for i in range(96):
    # 12-frame syllable blocks: Closed 2, Open 4, Teeth 2, Shout 2, Smile 2
    pos=i%12
    m = "Closed" if pos<2 else "Open" if pos<6 else "Teeth" if pos<8 else "Shout" if pos<10 else "Smile"
    seq.append((i, round(i/24,3), m))
with open(root/"LIPSYNC-TIMING-20261101.csv","w") as f:
    f.write("frame,time_s,cape_jones_mouth_piece,phoneme_class,note\n")
    for i,t,m in seq:
        pc = {"Closed":"rest/closure","Open":"vowel","Teeth":"fricative","Shout":"stressed vowel","Smile":"hold"}[m]
        f.write(f"{i},{t},{m},{pc},TEMPLATE ONLY - no donor line, no donor voice\n")
# --- talking test: base clip04 + synthesized syllable beeps + burned label ---
base = pathlib.Path.home()/"workspace/cape-jones-rig/movement-library-clips-20261101/04-smiling-friends-pose-swap-head.mp4"
sr=44100; dur=4.0; t=np.arange(int(sr*dur))/sr; audio=np.zeros_like(t)
freq={"Closed":0,"Open":440,"Teeth":880,"Shout":220,"Smile":330}
for i,tt,m in seq:
    if m=="Closed": continue
    s=int(tt*sr); e=min(len(audio), s+int(0.12*sr))
    audio[s:e]=0.3*np.sin(2*np.pi*freq[m]*t[s:e])*np.hanning(e-s)
audio=np.clip(audio,-0.9,0.9)
# write wav via ffmpeg raw
import subprocess, struct
raw=(audio*32767).astype(np.int16).tobytes()
subprocess.run(["ffmpeg","-y","-v","error","-f","s16le","-ar","44100","-ac","1","-i","-","-c:a","aac","-b:a","128k",str(work/"template_beeps.m4a")], input=raw, check=True)
# video: first 4.0s of clip04, drawtext label, replace audio with beeps
subprocess.run(["ffmpeg","-y","-v","error","-i",str(base),"-i",str(work/"template_beeps.m4a"),
 "-t","4.0","-vf","drawtext=text='TEMPLATE-AUDIO TEST ONLY - NOT DONOR VOICE - NOT FINAL LINES':fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:fontsize=28:fontcolor=red:box=1:boxcolor=white@0.8:x=10:y=10",
 "-map","0:v:0","-map","1:a:0","-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac","-shortest",
 str(root/"TALKING-TEST-TEMPLATE-AUDIO-20261101.mp4")], check=True)
subprocess.run(["ffmpeg","-y","-v","error","-i",str(root/"TALKING-TEST-TEMPLATE-AUDIO-20261101.mp4"),
 "-vf","scale=550:-1","-an",str(root/"TALKING-TEST-TEMPLATE-AUDIO-20261101.gif")], check=True)
# probes
def probe(p):
    out=subprocess.run(["ffprobe","-v","error","-show_entries","stream=codec_name,width,height,duration","-of","csv=p=0",str(p)],capture_output=True,text=True).stdout.strip()
    return out
print("talking mp4:", probe(root/"TALKING-TEST-TEMPLATE-AUDIO-20261101.mp4"))
print("inventory rows:", len(inv))
print("mouth seq first 12:", seq[:12])
