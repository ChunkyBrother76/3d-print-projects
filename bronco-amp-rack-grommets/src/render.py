import trimesh, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
m = trimesh.load("amp_rack_grommets.stl")
fig = plt.figure(figsize=(14,6))
for k,(el,az) in enumerate([(35,-60),(-35,-60)]):
    ax = fig.add_subplot(1,2,k+1,projection="3d")
    tris = m.vertices[m.faces]
    n = m.face_normals; light = np.array([0.4,-0.5,0.8]); light/=np.linalg.norm(light)
    shade = 0.35+0.65*np.clip(np.abs(n@light),0,1)
    col = np.c_[shade*0.25, shade*0.45, shade*0.85, np.ones_like(shade)]
    pc = Poly3DCollection(tris, facecolors=col, edgecolor="none"); ax.add_collection3d(pc)
    lo,hi = m.bounds; c=(lo+hi)/2; r=(hi-lo).max()/2
    ax.set_xlim(c[0]-r,c[0]+r); ax.set_ylim(c[1]-r,c[1]+r); ax.set_zlim(c[2]-r/3,c[2]+r/3)
    ax.set_box_aspect((1,1,1/3)); ax.view_init(el,az); ax.axis("off")
    ax.set_title("top (barrel side up)" if k==0 else "underside (flange face, on bed)")
plt.tight_layout(); plt.savefig("preview.png",dpi=110)
