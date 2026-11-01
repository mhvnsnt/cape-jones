import os, json
from PIL import Image
BASE=os.path.expanduser('~/workspace/cape-jones-rig/side-pack-new-20261101')
OUT=os.path.expanduser('~/workspace/cape-jones-rig/side-bent-layer-fix-20261101')
TOOLS=os.path.expanduser('~/workspace/cape-jones-rig/side-rig-fixed-20261101/tools')
def load(name, scale):
    im=Image.open(os.path.join(BASE,name)).convert('RGBA')
    if scale!=1.0: im=im.resize((round(im.width*scale), round(im.height*scale)), Image.LANCZOS)
    return im
KINDS={'cape_long':'cape','cape_drape':'cape','thigh_far':'thigh','shin_far':'shin','boot_far':'boot',
 'thigh_near':'thigh','shin_boot_near':'shin','pelvis':'pelvis','torso':'torso','neck':'neck','head':'head',
 'upper_arm_far':'upper_arm','forearm_far':'forearm','fist_far':'fist','bent_arm_near':'bent_arm'}
def build():
    m={'facing':1,'head_face_vec':(1,0),'torso_front_vec':(1,0),'boot_toe_vec':(1,0),'ground':1450,'pieces':[],'arms':[]}
    canvas=Image.new('RGBA',(1400,1600),(0,0,0,0))
    def paste(im,x,y,name):
        canvas.alpha_composite(im,(x,y))
        m['pieces'].append({'name':name,'x':x,'y':y,'w':im.width,'h':im.height,'kind':KINDS[name],'flipped':False})
    # BACK layer first: the former top-layer bent arm (bicep/upper + forearm + open hand).
    # NOT deleted. Pasted before everything else, so torso/cape cover its shoulder/bicep;
    # its forearm + open hand extend past the torso's right edge and remain visible as a far arm.
    bent = load('side_arm_bent_forearm_hand_open.png',1.0)
    paste(bent,660,420,'bent_arm_near')
    # Body, in order
    paste(load('side_cape_long.png',1.15),410,380,'cape_long')
    paste(load('side_cape_drape.png',0.9),430,350,'cape_drape')
    paste(load('side_thigh_right.png',1.0),610,930,'thigh_far')
    paste(load('side_shin_right.png',1.0),610,1130,'shin_far')
    paste(load('side_boot_right.png',1.0),540,1248,'boot_far')
    paste(load('side_thigh_left.png',1.0),560,930,'thigh_near')
    paste(load('side_shin_boot_left.png',1.0),560,1092,'shin_boot_near')
    paste(load('side_pelvis_hip.png',1.25),570,790,'pelvis')
    paste(load('side_torso_belt.png',1.3),560,360,'torso')
    paste(load('side_cowl_neck.png',1.3),600,280,'neck')
    paste(load('side_head_profile.png',1.3),600,120,'head')
    # NEAR arm on top: the former lower arm (upper + forearm + fist), unchanged coords, no flips.
    paste(load('side_upper_arm_right.png',1.15),570,410,'upper_arm_far')
    paste(load('side_forearm_gauntlet_right.png',1.1),640,680,'forearm_far')
    paste(load('side_fist_right.png',1.1),890,680,'fist_far')
    m['arms']=[
        {'name':'far_bent_back_layer','pose':'bent','elbow_xy':(800,600),'hand_xy':(1060,610),
         'note':'bent_arm_near moved to back layer; shoulder/bicep hidden behind torso, forearm+open hand visible past torso right edge'},
        {'name':'near_bent','pose':'bent','elbow_xy':(660,720),'hand_xy':(960,735)},
    ]
    m['layer_order']=[p['name'] for p in m['pieces']]
    m['joints']=[['torso','bent_arm_near'],['torso','upper_arm_far'],['upper_arm_far','forearm_far'],['forearm_far','fist_far'],
                 ['pelvis','thigh_near'],['thigh_near','shin_boot_near'],['pelvis','thigh_far'],['thigh_far','shin_far']]
    canvas.save(os.path.join(OUT,'side-bent-layer-fix-20261101.png'))
    grey=Image.new('RGBA',(1400,1600),(128,128,128,255)); grey.alpha_composite(canvas); grey.convert('RGB').save(os.path.join(OUT,'side-bent-layer-fix-grey-20261101.png'))
    # Visibility measurement for the back-layer bent arm: bent alone vs all other pieces covering it.
    bent_only=Image.new('RGBA',(1400,1600),(0,0,0,0)); bent_only.alpha_composite(bent,(660,420))
    others=Image.new('RGBA',(1400,1600),(0,0,0,0))
    # rebuild others in same order, without bent
    for name,fn,sc,x,y in [
        ('cape_long','side_cape_long.png',1.15,410,380),('cape_drape','side_cape_drape.png',0.9,430,350),
        ('thigh_far','side_thigh_right.png',1.0,610,930),('shin_far','side_shin_right.png',1.0,610,1130),
        ('boot_far','side_boot_right.png',1.0,540,1248),('thigh_near','side_thigh_left.png',1.0,560,930),
        ('shin_boot_near','side_shin_boot_left.png',1.0,560,1092),('pelvis','side_pelvis_hip.png',1.25,570,790),
        ('torso','side_torso_belt.png',1.3,560,360),('neck','side_cowl_neck.png',1.3,600,280),
        ('head','side_head_profile.png',1.3,600,120),('upper_arm_far','side_upper_arm_right.png',1.15,570,410),
        ('forearm_far','side_forearm_gauntlet_right.png',1.1,640,680),('fist_far','side_fist_right.png',1.1,890,680)]:
        others.alpha_composite(load(fn,sc),(x,y))
    ba=bent_only.getchannel('A'); oa=others.getchannel('A')
    total=sum(1 for v in ba.getdata() if v>10)
    visible=sum(1 for b,o in zip(ba.getdata(),oa.getdata()) if b>10 and o<=10)
    m['bent_arm_visibility']={'bent_total_opaque_px':total,'bent_visible_px_after_back_layer':visible,
        'bent_hidden_px_behind_torso_etc':total-visible,
        'note':'visible portion is forearm+open hand past torso right edge (x>893); shoulder/bicep hidden behind torso, as a far arm should be; NOT deleted, NOT fully hidden'}
    json.dump(m, open(os.path.join(OUT,'side-bent-layer-fix-manifest.json'),'w'), indent=2)
    print('built', m['bent_arm_visibility'])
    print('bbox', canvas.getchannel('A').getbbox())
build()
