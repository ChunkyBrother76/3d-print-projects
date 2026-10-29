import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, numpy as np
import grommets as g3, grommets_v4 as g4
from manifold3d import Manifold
fig, axs = plt.subplots(2,2, figsize=(11,5))
for col,(name,d,spec) in enumerate([g4.SIZES[1], g4.SIZES[3]]):
    for row,(lab,mod) in enumerate([("v3",g3),("v4",g4)]):
        p,_ = mod.grommet(d,spec)
        sec = p.rotate((90,0,0)).slice(0.0)  # XZ plane through center
        ax = axs[row][col]
        for poly in sec.to_polygons():
            poly = np.asarray(poly); ax.fill(poly[:,0], poly[:,1], color="#2f5fb0")
        ax.set_aspect("equal"); ax.set_xlim(-12,12); ax.set_ylim(-9.5,0.5); ax.set_title(f"{name} {lab} section", fontsize=10)
        ax.grid(alpha=.3)
plt.tight_layout(); plt.savefig("section_v4.png", dpi=100)
