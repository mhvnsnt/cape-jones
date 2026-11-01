"""Tool 3: layer order + joint overlap check, from a placement manifest.
Each joint lists two piece names; their placed rects must overlap (joint ball area),
and layer order must match the declared order list."""
import sys, json
def rect(p): return (p['x'], p['y'], p['x']+p['w'], p['y']+p['h'])
def overlap(a,b):
    return not (a[2]<=b[0] or b[2]<=a[0] or a[3]<=b[1] or b[3]<=a[1])
def check(m):
    fails=[]
    by={p['name']:p for p in m['pieces']}
    if [p['name'] for p in m['pieces']] != m['layer_order']:
        fails.append('layer order does not match declared layer_order')
    for j in m.get('joints',[]):
        if not overlap(rect(by[j[0]]), rect(by[j[1]])):
            fails.append(f"joint {j[0]} / {j[1]} rects do not overlap")
    print('PASS' if not fails else 'FAIL')
    for x in fails: print(' -',x)
    return 0 if not fails else 1
if __name__=='__main__': sys.exit(check(json.load(open(sys.argv[1]))))
