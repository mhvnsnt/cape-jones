# step 0 for build_cloth.py: run `blender -b RIG --python precompute_cape_islands_blender.py` (writes bco/bedges/bcol .npy
# to /workspace/cj3d/diag), then this (system python + scipy) -> $CJ_WORK/body_islands.npy ; copy bcol.npy to $CJ_WORK/body_texcol.npy
import numpy as np, scipy.sparse as sp, scipy.sparse.csgraph as cg, os, sys
d=sys.argv[1] if len(sys.argv)>1 else "/workspace/cj3d/diag"; w=os.environ.get("CJ_WORK","/workspace/cj3d/v2")
co=np.load(d+"/bco.npy"); e=np.load(d+"/bedges.npy")
n,lab=cg.connected_components(sp.coo_matrix((np.ones(len(e)),(e[:,0],e[:,1])),shape=(len(co),)*2),directed=False)
np.save(w+"/body_islands.npy",lab); print("islands",n)
