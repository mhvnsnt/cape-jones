import sys, urllib.request, urllib.error, struct, json, zlib, os, hashlib, subprocess, time
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request
W='/home/hatch/workspace/cape-jones-rig/robin-eyes-100-20261031'
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
    add_surrogate_to_request(r, "custom.github-api", allowed_hosts=["api.github.com"])
    try: urllib.request.build_opener(NoRedir()).open(r, timeout=60)
    except urllib.error.HTTPError as e: return e.headers.get("Location")
    raise RuntimeError("no redirect")
# 1. central directory
tail=api_range(639834966, 227400000, 227413774)
i=tail.rfind(b'PK\x05\x06')
sig, disk, cddisk, n, total, cdsize, cdoff, clen = struct.unpack('<IHHHHIIH', tail[i:i+22])
print("entries", total, "cdoff", cdoff, "cdsize", cdsize, flush=True)
cd=api_range(639834966, cdoff-PART_AA, cdoff-PART_AA+cdsize-1)
entries=[]; off=0
while off < len(cd) and cd[off:off+4]==b'PK\x01\x02':
    (ver, vmade, flag, method, mtime, mdate, crc, csize, usize, nlen, elen, clen2, dsk, iattr, eattr, lho) = struct.unpack('<HHHHHHIIIHHHHHII', cd[off+4:off+46])
    name=cd[off+46:off+46+nlen].decode('utf-8', errors='replace')
    entries.append(dict(name=name, method=method, csize=csize, usize=usize, lho=lho, flag=flag))
    off+=46+nlen+elen+clen2
json.dump(entries, open(f'{W}/tt-entries.json','w'), indent=1)
print("parsed", len(entries), flush=True)
# 2. signed urls (in memory only, never written to disk)
URLS={0: signed_url(639834989), 1: signed_url(639834966)}
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
robin=[e for e in entries if 'robin' in e['name'].lower() or 'RBNEXPRES' in e['name']]
manifest=[]
for idx,e in enumerate(robin):
    hdr=stream_range(e['lho'], 30); assert hdr[:4]==b'PK\x03\x04', e['name']
    nlen, elen = struct.unpack('<HH', hdr[26:30])
    data=stream_range(e['lho']+30+nlen+elen, e['csize'])
    raw=zlib.decompress(data, -15) if e['method']==8 else data
    assert len(raw)==e['usize'], (e['name'], len(raw), e['usize'])
    safe=f"{idx:02d}_"+e['name'].rsplit('/',1)[-1].replace(' ','_')
    open(f'{W}/raw/{safe}','wb').write(raw)
    manifest.append(dict(idx=idx, name=e['name'], file=safe, usize=e['usize'], sha256=hashlib.sha256(raw).hexdigest()))
    print(idx, safe, e['usize'], flush=True)
json.dump(manifest, open(f'{W}/manifest.json','w'), indent=1)
print("DONE", len(manifest), flush=True)
