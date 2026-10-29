import numpy as np, trimesh
from manifold3d import Manifold
from grommets import grommet, IN
SIZES = [("0ga",7/8*IN,("round",17.5)),("4ga",5/8*IN,("round",12.8)),("RCA",3/4*IN,("round",14.0)),
         ("12ga",5/8*IN,("slot",5.6,10.6)),("14ga",1/2*IN,("slot",5.0,9.2))]
for name,drill,spec in SIZES:
    p,r = grommet(drill,spec); cell = 2*r+4
    plate = Manifold()
    for i in range(12): plate += p.translate(((i%4)*cell, -(i//4)*cell, 0))
    m = plate.to_mesh()
    mesh = trimesh.Trimesh(np.asarray(m.vert_properties)[:,:3], np.asarray(m.tri_verts))
    mesh.apply_translation(-mesh.bounds[0]); f=f"plates/grommets_{name}_x12.stl"; mesh.export(f)
    print(f, mesh.is_watertight, len(mesh.split()), np.round(mesh.extents[:2],1))
