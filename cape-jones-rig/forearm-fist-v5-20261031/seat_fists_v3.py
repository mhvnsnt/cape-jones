from PIL import Image
base_dir='/home/hatch/workspace/cape-jones-rig/'
out_dir=base_dir+'forearm-fist-v5-20261031/'
def seat(forearm_path, fist_path, forearm_offset, fist_centre_x, fist_top_y, out_name, fist_w=170, cut_y=88):
    fore=Image.open(base_dir+forearm_path).convert('RGBA')
    px=fore.load()
    for y in range(cut_y, fore.size[1]):
        for x in range(fore.size[0]):
            px[x,y]=(0,0,0,0)
    fist=Image.open(out_dir+fist_path).convert('RGBA')
    fist_rot=fist.rotate(180, expand=True)
    fh=int(fist_rot.size[1]*fist_w/fist_rot.size[0])
    fist_rot=fist_rot.resize((fist_w,fh), Image.LANCZOS)
    canvas=Image.new('RGBA',(320,300),(0,0,0,0))
    canvas.alpha_composite(fore, forearm_offset)
    canvas.alpha_composite(fist_rot, (fist_centre_x-fist_w//2, fist_top_y))
    canvas.save(out_dir+out_name)
    print(out_name, 'fist', fist_rot.size, 'top', fist_top_y, 'bottom', fist_top_y+fh)
seat('forearm-fist-v3-20261031/forearm-v3-arm2-standard-clean-20261031.png',
     'fist-left-v5-20261031.png', (35,0), 205, 65, 'forearm-v5-arm2-front-punch-fist-20261031.png')
seat('forearm-fist-v3-20261031/forearm-v3-arm1-clean-20261031.png',
     'fist-right-v5-20261031.png', (40,0), 165, 65, 'forearm-v5-arm1-front-punch-fist-20261031.png')
