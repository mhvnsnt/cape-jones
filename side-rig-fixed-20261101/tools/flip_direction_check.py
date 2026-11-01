"""Tool 4: flip-direction check. For this pack (facing right), native arm pieces
must NOT be horizontally flipped. A flipped flag on any arm piece = FAIL."""
import sys, json
def check(manifest):
    bad=[p for p in manifest.get('pieces',[]) if p.get('kind') in ('upper_arm','forearm','fist','bent_arm') and p.get('flipped')]
    print('FAIL flipped arm pieces:', bad) if bad else print('PASS no arm pieces flipped')
    return 1 if bad else 0
if __name__=='__main__': sys.exit(check(json.load(open(sys.argv[1]))))
