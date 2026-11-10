import os, json, sys
sys.path.insert(0, os.path.expanduser('~/workspace/cape-jones-rig/side-rig-fixed-20261101/tools'))
from PIL import Image
from fk_pivot_rotate import rotate_about_pivot
BASE=os.path.expanduser('~/workspace/cape-jones-rig/side-pack-new-20261101')
OUT=os.path.expanduser('~/workspace/cape-jones-rig/side-rig-fixed-20261101')
def load(name, scale, flip=False):
    im=Image.open(os.path.join(BASE,name)).convert('RGBA')
    if flip: im=im.transpose(Image.FLIP_LEFT_RIGHT)
    if scale!=1.0: im=im.resize((round(im.width*scale), round(im.height*scale)), Image.LANCZOS)
    return im
def paste(canvas, im, x, y, name, manifest):
    canvas.alpha_composite(im, (x,y))
    manifest['pieces'].append({'name':name,'x':x,'y':y,'w':im.width,'h':im.height,
        'kind':manifest.get('_kind',{}).get(name,''),'flipped':False})
    return (x,y,im.width,im.height)

def body(canvas, m):
    # back to front: cape, far leg, near leg, far arm handled by caller, pelvis, torso, neck, head
    paste(canvas, load('side_cape_long.png',1.15), 410, 380, 'cape_long', m)
    paste(canvas, load('side_cape_drape.png',0.9), 430, 350, 'cape_drape', m)
    # far leg (right pieces, slightly back/left)
    paste(canvas, load('side_thigh_right.png',1.0), 610, 930, 'thigh_far', m)
    paste(canvas, load('side_shin_right.png',1.0), 610, 1130, 'shin_far', m)
    paste(canvas, load('side_boot_right.png',1.0), 540, 1248, 'boot_far', m)
    # near leg
    paste(canvas, load('side_thigh_left.png',1.0), 560, 930, 'thigh_near', m)
    paste(canvas, load('side_shin_boot_left.png',1.0), 560, 1092, 'shin_boot_near', m)
    paste(canvas, load('side_pelvis_hip.png',1.25), 570, 790, 'pelvis', m)
    paste(canvas, load('side_torso_belt.png',1.3), 560, 360, 'torso', m)
    paste(canvas, load('side_cowl_neck.png',1.3), 600, 280, 'neck', m)
    paste(canvas, load('side_head_profile.png',1.3), 600, 120, 'head', m)

def make_idle():
    m={'facing':1,'head_face_vec':(1,0),'torso_front_vec':(1,0),'boot_toe_vec':(1,0),'ground':1450,'pieces':[],'arms':[]}
    canvas=Image.new('RGBA',(1400,1600),(0,0,0,0))
    # far arm behind torso? place far upper first, then body, then near arm on top; far forearm/fist also behind torso layer is wrong for visibility, so place far arm fully before body but offset left so it shows beside back edge
    # Instead: body first without far arm, then far arm at back-left offset, then near arm front. Layer order list will reflect this.
    body(canvas,m)
    # far idle arm: upper vertical, forearm rotated down about elbow
    paste(canvas, load('side_upper_arm_right.png',1.15), 570, 410, 'upper_arm_far', m)
    fore,_ = rotate_about_pivot(load('side_forearm_gauntlet_right.png',1.1), (15,53), -90)  # east -> south
    # rotated forearm: elbow pivot at top of trimmed image
    paste(canvas, fore, 600, 690, 'forearm_far_idle', m)
    fist,_ = rotate_about_pivot(load('side_fist_right.png',1.1), (10,55), -90)
    paste(canvas, fist, 600, 870, 'fist_far_idle', m)
    m['arms'].append({'name':'far_idle','pose':'idle_down','elbow_xy':(660,720),'hand_xy':(660,990)})
    # near idle arm, in front
    paste(canvas, load('side_upper_arm_left.png',1.2), 640, 400, 'upper_arm_near', m)
    fore2,_ = rotate_about_pivot(load('side_forearm_gauntlet_right.png',1.1), (15,53), -90)
    paste(canvas, fore2, 670, 690, 'forearm_near_idle', m)
    fist2,_ = rotate_about_pivot(load('side_fist_right.png',1.1), (10,55), -90)
    paste(canvas, fist2, 670, 870, 'fist_near_idle', m)
    m['arms'].append({'name':'near_idle','pose':'idle_down','elbow_xy':(730,720),'hand_xy':(730,990)})
    m['layer_order']=[p['name'] for p in m['pieces']]
    m['joints']=[['torso','upper_arm_near'],['upper_arm_near','forearm_near_idle'],['forearm_near_idle','fist_near_idle'],['torso','upper_arm_far'],['pelvis','thigh_near'],['thigh_near','shin_boot_near'],['pelvis','thigh_far'],['thigh_far','shin_far']]
    canvas.save(os.path.join(OUT,'side-idle-arms-down-fixed-20261101.png'))
    grey=Image.new('RGBA',(1400,1600),(128,128,128,255)); grey.alpha_composite(canvas); grey.convert('RGB').save(os.path.join(OUT,'side-idle-arms-down-fixed-grey-20261101.png'))
    json.dump(m, open(os.path.join(OUT,'side-idle-manifest.json'),'w'), indent=2)
    return m

def make_bent():
    m={'facing':1,'head_face_vec':(1,0),'torso_front_vec':(1,0),'boot_toe_vec':(1,0),'ground':1450,'pieces':[],'arms':[]}
    canvas=Image.new('RGBA',(1400,1600),(0,0,0,0))
    body(canvas,m)
    # far bent arm: upper vertical + forearm horizontal UNFLIPPED + fist UNFLIPPED, hand forward-right
    paste(canvas, load('side_upper_arm_right.png',1.15), 570, 410, 'upper_arm_far', m)
    paste(canvas, load('side_forearm_gauntlet_right.png',1.1), 640, 680, 'forearm_far', m)
    paste(canvas, load('side_fist_right.png',1.1), 890, 680, 'fist_far', m)
    m['arms'].append({'name':'far_bent','pose':'bent','elbow_xy':(660,720),'hand_xy':(960,735)})
    # near bent arm: bent assembly ONLY, UNFLIPPED, forearm to the right, hand in front of chest
    bent=load('side_arm_bent_forearm_hand_open.png',1.0)
    paste(canvas, bent, 660, 420, 'bent_arm_near', m)
    # bent native: shoulder ~ (40,25), elbow ~(140,180), hand centre ~(400,190) in native coords
    m['arms'].append({'name':'near_bent','pose':'bent','elbow_xy':(800,600),'hand_xy':(1060,610)})
    m['layer_order']=[p['name'] for p in m['pieces']]
    m['joints']=[['torso','upper_arm_far'],['upper_arm_far','forearm_far'],['forearm_far','fist_far'],['torso','bent_arm_near'],['pelvis','thigh_near'],['thigh_near','shin_boot_near'],['pelvis','thigh_far'],['thigh_far','shin_far']]
    canvas.save(os.path.join(OUT,'side-bent-correct-20261101.png'))
    grey=Image.new('RGBA',(1400,1600),(128,128,128,255)); grey.alpha_composite(canvas); grey.convert('RGB').save(os.path.join(OUT,'side-bent-correct-grey-20261101.png'))
    json.dump(m, open(os.path.join(OUT,'side-bent-manifest.json'),'w'), indent=2)
    return m
make_idle(); make_bent(); print('built')
