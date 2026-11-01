"""Tool 1: anatomy / facing / elbow-flexion check.
facing = +1 for right, -1 for left. Flexion requires forearm vector dot facing > 0.
Returns exit 0 PASS, 1 FAIL, prints each check."""
import sys, json
def check(manifest):
    fails=[]
    f = manifest['facing']  # +1 right
    # head, torso, toes must agree with facing
    for name, vec in [('head_face', manifest['head_face_vec']), ('torso_front', manifest['torso_front_vec']), ('boot_toe', manifest['boot_toe_vec'])]:
        if vec[0]*f <= 0: fails.append(f"{name} vector {vec} disagrees with facing {f}")
    for arm in manifest.get('arms',[]):
        elbow, hand = arm['elbow_xy'], arm['hand_xy']
        vec = (hand[0]-elbow[0], hand[1]-elbow[1])
        if arm['pose']=='bent' and vec[0]*f <= 0:
            fails.append(f"{arm['name']}: bent forearm vector {vec} is backward (extension), facing {f} — FLIPPED, FAIL")
        if arm['pose']=='idle_down' and vec[1] <= 0:
            fails.append(f"{arm['name']}: idle forearm should point down (+y), got {vec}")
    print('PASS' if not fails else 'FAIL')
    for x in fails: print(' -',x)
    return 0 if not fails else 1
if __name__=='__main__':
    sys.exit(check(json.load(open(sys.argv[1]))))
