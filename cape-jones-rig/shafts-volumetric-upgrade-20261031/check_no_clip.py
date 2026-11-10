# Gate, run after composite: FAIL if figure alpha touches canvas edge.
from PIL import Image
import numpy as np, sys
fig = np.array(Image.open('/home/hatch/workspace/cape-jones-rig/dual-light-variants-20261031/base-arms-up-transparent-20261031.png'))
edge = np.concatenate([fig[0,:,3], fig[-1,:,3], fig[:,0,3], fig[:,-1,3]])
print("edge_alpha_max", int(edge.max()))
sys.exit(0 if int(edge.max())==0 else 1)
