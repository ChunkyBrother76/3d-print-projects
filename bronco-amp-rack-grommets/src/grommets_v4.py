"""v4: minimal flange + hollow thin-wall barrel. Same fit (ribs/barrel OD) and wire openings as v3."""
import numpy as np, trimesh, sys
from manifold3d import Manifold, CrossSection
import grommets as g3
from grommets import SEG, BARREL_L, RIB_COUNT, RIB_R, RIB_PROUD, CLEAR, IN, hole_profile

FLANGE_T = 1.2      # 6 layers at 0.2 mm (v3: 2.2)
FLANGE_LIP = 1.0    # overhang past the drilled hole per side (v3: 1.75)
WALL = 1.2          # barrel wall, 3 perimeters with a 0.4 nozzle
CHAMF = 0.6         # chamfer on the visible face of the wire opening

SIZES = [("0ga",7/8*IN,("round",17.5)),("4ga",5/8*IN,("round",12.8)),("RCA",3/4*IN,("round",14.0)),
         ("12ga",5/8*IN,("slot",5.6,10.6)),("14ga",1/2*IN,("slot",5.0,9.2))]

def grommet(drill, spec):
    R = drill/2 - CLEAR
    fr = drill/2 + FLANGE_LIP
    total = FLANGE_T + BARREL_L
    flange = Manifold.cylinder(FLANGE_T-0.4, fr, fr, SEG) + \
             Manifold.cylinder(0.4, fr, fr-0.4, SEG).translate((0,0,FLANGE_T-0.4))
    barrel = Manifold.cylinder(BARREL_L-0.8, R, R, SEG).translate((0,0,FLANGE_T)) + \
             Manifold.cylinder(0.8, R, R-0.4, SEG).translate((0,0,total-0.8))
    ribs = Manifold()
    for i in range(RIB_COUNT):
        ribs += Manifold.cylinder(BARREL_L-1.5, RIB_R, RIB_R, 24)\
            .translate((drill/2+RIB_PROUD-RIB_R,0,FLANGE_T)).rotate((0,0,360*i/RIB_COUNT))
    part = flange + barrel + ribs
    # hollow barrel
    part -= Manifold.cylinder(BARREL_L+1, R-WALL, R-WALL, SEG).translate((0,0,FLANGE_T))
    # wire opening through the flange, chamfered on the show face (bed side)
    cut = hole_profile(spec).extrude(FLANGE_T+2).translate((0,0,-1))
    steps = 6
    for i in range(steps):
        za = CHAMF*i/steps - 0.01
        cut += hole_profile(spec, CHAMF*(1-(i+0.5)/steps)).extrude(CHAMF/steps+0.02).translate((0,0,za))
    part -= cut
    return part, fr

def to_mesh(man):
    m = man.to_mesh()
    t = trimesh.Trimesh(np.asarray(m.vert_properties)[:,:3], np.asarray(m.tri_verts))
    t.apply_translation(-t.bounds[0]); return t

if __name__ == "__main__":
    print(f"{'size':6}{'v3 cm3':>8}{'v4 cm3':>8}{'saved':>7}{'flange OD v3→v4':>18}")
    test = Manifold(); x = 0
    for name, d, spec in SIZES:
        p3, r3 = g3.grommet(d, spec); p4, r4 = grommet(d, spec)
        v3, v4 = p3.volume()/1000, p4.volume()/1000
        print(f"{name:6}{v3:8.2f}{v4:8.2f}{(1-v4/v3)*100:6.0f}%{2*r3:9.1f} → {2*r4:.1f}")
        cell = 2*r4 + 4
        plate = Manifold()
        for i in range(12): plate += p4.translate(((i%4)*cell, -(i//4)*cell, 0))
        t = to_mesh(plate); f = f"plates_v4/grommets_{name}_x12_v4.stl"; t.export(f)
        print("   ", f, t.is_watertight, len(t.split()), np.round(t.extents[:2],1))
        test += p4.translate((x + r4, 0, 0)); x += 2*r4 + 4
    t = to_mesh(test); t.export("grommets_v4_test_set.stl")
    print("test set", t.is_watertight, len(t.split()), np.round(t.extents,1))
