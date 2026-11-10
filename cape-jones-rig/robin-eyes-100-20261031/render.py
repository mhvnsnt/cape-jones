import json, subprocess, os
W='/home/hatch/workspace/cape-jones-rig/robin-eyes-100-20261031'
GS=f'{W}/gsroot/root/usr/bin/gs'
env=dict(os.environ, LD_LIBRARY_PATH=f'{W}/gsroot/root/usr/lib/x86_64-linux-gnu')
ARGS=['-dBATCH','-dNOPAUSE','-sDEVICE=pngalpha','-r144',
      f'-I{W}/gsroot/share/ghostscript/10.02/lib',
      f'-I{W}/gsroot/share/ghostscript/10.02/Resource/Init',
      f'-sGenericResourceDir={W}/gsroot/share/ghostscript/10.02/Resource/']
m=json.load(open(f'{W}/manifest.json'))
seen=set(); todo=[]
for x in m:
    if x['usize']==0 or x['sha256'] in seen: continue
    seen.add(x['sha256'])
    if x['file'].lower().endswith(('.eps','.ai')): todo.append(x)
os.makedirs(f'{W}/render', exist_ok=True)
print("unique vector:", len(todo), flush=True)
for x in todo:
    out=f"{W}/render/{x['file'].rsplit('.',1)[0]}.png"
    p=subprocess.run([GS]+ARGS+[f'-o{out}', f"{W}/raw/{x['file']}"],
                     capture_output=True, text=True, timeout=300, env=env)
    print(("OK " if os.path.exists(out) and os.path.getsize(out)>0 else "FAIL ")+x['file'], flush=True)
print("RENDER DONE", flush=True)
