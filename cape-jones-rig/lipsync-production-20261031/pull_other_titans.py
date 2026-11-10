"""Pull other-Titans COLOR expression EPS from teen-titans-complete-v1 via range reads.
Same method as robin-eyes-100 extract.py (GitHub API range + signed-URL curl).
Robin SG01 already local, skipped. B&W duplicates skipped (same art, no new mouths).
Writes raw/ + pull-manifest-20261031.json in this folder only."""
import sys, urllib.request, urllib.error, struct, json, zlib, os, hashlib, subprocess, time
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request
W='/home/hatch/workspace/cape-jones-rig/lipsync-production-20261031'
PART_AA=508559360
def api_range(asset, a, b):
    url=f"https://api.github.com/repos/mhvnsnt/cn-gigaleak-teen-titans/releases/assets/{asset}"
    r=urllib.request.Request(url, method="GET")
    r.add_header("Accept","application/octet-stream"); r.add_header("User-Agent","Muse-GitHub-Api")
    r.add_header("Range", f"bytes={a}-{b}")
    add_surrogate_to_request(r, "custom.github-api", allowed_hosts=["api.github.com"])
    with urllib.request.build_opener().open(r, timeout=180) as resp: return resp.read()
class NoRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args): return None
def signed_url(asset):
    url=f"https://api.github.com/repos/mhvnsnt/cn-gigaleak-teen-titans/releases/assets/{asset}"
    r=urllib.request.Request(url, method="GET")
    r.add_header("Accept","application/octet-stream"); r.add_header("User-Agent","Muse-GitHub-Api")
    try: urllib.request.build_opener(NoRedir()).open(r, timeout=60)
    except urllib.error.HTTPError as e: return e.headers.get("Location")
    raise RuntimeError("no redirect")
entries=json.load(open('/home/hatch/workspace/cape-jones-rig/robin-eyes-100-20261031/tt-entries.json'))
targets=[]
for e in entries:
    n=e['name']
    if 'Character Expressions' in n and n.endswith('.EPS') and '/Color/' in n and '/Robin/' not in n and 'RBNEXPRES' not in n:
        targets.append(e)
print("targets", len(targets), flush=True)
def signed_url_retry(asset):
    for a in range(4):
        u=signed_url(asset)
        if u: return u
        time.sleep(5)
    raise RuntimeError(f"signed url empty for {asset}")
URLS={0: signed_url_retry(639834989), 1: signed_url_retry(639834966)}
print("signed urls ok", len(URLS[0]), len(URLS[1]), flush=True)
def get_range(asset, a, b):
    for attempt in range(6):
        p=subprocess.run(['curl','-s','-f','-r',f'{a}-{b}', URLS[asset], '-o', f'{W}/_chunk.bin'], capture_output=True, text=True, timeout=180)
        if p.returncode==0: return open(f'{W}/_chunk.bin','rb').read()
        time.sleep(8*(attempt+1))
    raise RuntimeError(f"curl failed {asset} {a}-{b}")
def stream_range(start, length):
    out=b""; pos=start
    while len(out)<length:
        if pos<PART_AA: asset=0; base=0; avail=PART_AA-pos
        else: asset=1; base=PART_AA; avail=10**18
        take=min(length-len(out), avail); out+=get_range(asset, pos-base, pos-base+take-1); pos+=take
    return out
os.makedirs(f'{W}/raw', exist_ok=True)
manifest=[]
for e in targets:
    hdr=stream_range(e['lho'], 30); assert hdr[:4]==b'PK\x03\x04', e['name']
    nlen, elen = struct.unpack('<HH', hdr[26:30])
    data=stream_range(e['lho']+30+nlen+elen, e['csize'])
    raw=zlib.decompress(data, -15) if e['method']==8 else data
    assert len(raw)==e['usize'], (e['name'], len(raw), e['usize'])
    safe=e['name'].rsplit('/',1)[-1].replace(' ','_')
    open(f'{W}/raw/{safe}','wb').write(raw)
    manifest.append(dict(name=e['name'], file=safe, usize=e['usize'], sha256=hashlib.sha256(raw).hexdigest()))
    print("OK", safe, e['usize'], flush=True)
json.dump(manifest, open(f'{W}/pull-manifest-20261031.json','w'), indent=1)
print("DONE", len(manifest), flush=True)
