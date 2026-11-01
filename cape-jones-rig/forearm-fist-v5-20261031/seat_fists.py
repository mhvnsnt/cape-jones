from PIL import Image
base_dir='/home/hatch/workspace/cape-jones-rig/'
out_dir=base_dir+'forearm-fist-v5-20261031/'
def seat(forearm_path, fist_path, forearm_offset, fist_centre_x, fist_top_y, out_name, fist_w=165):
    fore=Image.open(base_dir+forearm_path).convert('RGBA')
    fist=Image.open(out_dir+fist_path).convert('RGBA')
    # rotate 180: knuckles -> strike edge (bottom), wrist -> forearm (top), facing preserved
    fist_rot=fist.rotate(180, expand=True)
    fh=int(fist_rot.size[1]*fist_w/fist_rot.size[0])
    fist_rot=fist_rot.resize((fist_w,fh), Image.LANCZOS)
    canvas=Image.new('RGBA',(320,300),(0,0,0,0))
    canvas.alpha_composite(fore, forearm_offset)
    canvas.alpha_composite(fist_rot, (fist_centre_x-fist_w//2, fist_top_y))
    canvas.save(out_dir+out_name)
    print(out_name, canvas.size, 'fist', fist_rot.size, 'top', fist_top_y, 'bottom', fist_top_y+fh)
# Arm2: left source fist (thumb bottom-right -> after 180 thumb top-left = Arm2 thumb left)
seat('forearm-fist-v3-20261031/forearm-v3-arm2-standard-clean-20261031.png',
     'fist-left-v5-20261031.png', (35,0), 220, 95, 'forearm-v5-arm2-front-punch-fist-20261031.png')
# Arm1: right source fist (thumb bottom-left -> after 180 thumb top-right)
seat('forearm-fist-v3-20261031/forearm-v3-arm1-clean-20261031.png',
     'fist-right-v5-20261031.png', (40,0), 160, 95, 'forearm-v5-arm1-front-punch-fist-20261031.png')
