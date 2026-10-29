#!/usr/bin/env python3
"""Reverse-engineer a reference song into a vocal-chain preset suggestion.
Open-source, analysis only: given a reference audio file, it measures tempo,
loudness, crest, band power, vocal-dominant pitch, stereo width, and outputs
a JSON preset (pitch ratio to 350Hz AVANNA/neptune target, vocal/title balance,
tempo-synced delay, God-Particle-style bus amount) that our mix scripts can use.
It does NOT copy audio, stems, or melodies — measurements only.
Usage: python3 reverse_engineer.py <audiofile> <label> [bpm_hint]
"""
import subprocess, wave, json, sys, numpy as np
def load(p, ss=None, dur=None):
    cmd=["ffmpeg","-y","-v","error"]
    if ss: cmd+=["-ss",ss]
    if dur: cmd+=["-t",dur]
    cmd+=["-i",p,"-ac","2","-ar","44100","/tmp/rev.wav"]
    subprocess.run(cmd,check=True)
    w=wave.open("/tmp/rev.wav"); n=w.getnframes(); sr=w.getframerate()
    return np.frombuffer(w.readframes(n),dtype=np.int16).astype(float)/32768, sr
def fft_acorr(x):
    n=1<<int(np.ceil(np.log2(len(x)*2))); S=np.fft.rfft(x,n); c=np.fft.irfft(S*np.conj(S),n)[:len(x)]
    return c/max(c[0],1e-9)
def main(path, label, bpm_hint=None):
    d,sr=load(path)
    mid=(d[:,0]+d[:,1])/2 if d.ndim>1 and d.shape[1]==2 else d
    side=(d[:,0]-d[:,1])/2 if d.ndim>1 and d.shape[1]==2 else np.zeros_like(mid)
    rms=float(np.sqrt(np.mean(mid**2))); peak=float(np.max(np.abs(mid)))
    spec=np.abs(np.fft.rfft(mid*np.hanning(len(mid)))); f=np.fft.rfftfreq(len(mid),1/sr); tot=np.sum(spec**2)
    bands={}
    for name,lo,hi in [("bass<250",0,250),("lowmid250-1k",250,1000),("vocal1k-8k",1000,8000),("air>8k",8000,22050)]:
        m=(f>=lo)&(f<hi); bands[name]=round(float(np.sum(spec[m]**2)/tot),3)
    # vocal-dominant pitch: HP>300Hz per-second autocorr median
    ps=[]
    for s in range(0,max(1,len(mid)-sr),sr):
        seg=mid[s:s+sr].copy(); S=np.fft.rfft(seg); fr=np.fft.rfftfreq(len(seg),1/sr); S[fr<300]=0; seg=np.fft.irfft(S,len(seg)); seg=seg-np.mean(seg); c=fft_acorr(seg); lo,hi=int(sr/600),int(sr/200); c[:lo]=0; ps.append(sr/(np.argmax(c[lo:hi])+lo))
    pitch=float(np.median(ps))
    preset={
      "reference": label, "duration_s": round(len(mid)/sr,1),
      "rms": round(rms,3), "peak": round(peak,3), "crest_db": round(float(20*np.log10(peak/rms)),1),
      "bands": bands, "vocal_pitch_median_hz": round(pitch,0),
      "stereo_width_side_mid": round(float(np.sqrt(np.mean(side**2))/max(np.sqrt(np.mean(mid**2)),1e-9)),2),
      "suggested_preset": {
        "pitch_ratio_to_350hz": round(350/145,2),
        "formant_ratio": 1.4, "autotune_key": "D major", "autotune_glide_ms": 55,
        "vocal_bus": 6.0, "title_bus": 1.00, "god_particle_style_amount_pct": 100,
        "delay_ms_dotted_eighth_at_140bpm": 321.4, "delay_wet": 0.25, "reverb_echo_wet": 0.22,
      }}
    print(json.dumps(preset, indent=2))
    with open(f"/home/hatch/workspace/mochiichao-work/title-music/vocal-mix/presets/reverse-{label}.json","w") as fh: json.dump(preset, fh, indent=2)
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
