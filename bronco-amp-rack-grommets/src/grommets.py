"""Flanged press-in cable grommets for amp rack wiring.
Printed flange-down. Barrel has crush ribs so it presses into a drilled hole.
All dimensions in mm.
"""
import math
import numpy as np
import trimesh
from manifold3d import Manifold, CrossSection

SEG = 96            # circle smoothness
FLANGE_T = 2.2      # flange thickness
FLANGE_LIP = 1.75   # flange overhang past the hole, per side (v3: was 3.5)
BARREL_L = 6.0      # barrel depth into the panel
RIB_COUNT = 8
RIB_R = 0.6         # crush rib radius
RIB_PROUD = 0.45       # how far ribs stand past the drilled hole (v2: was 0.25)
CLEAR = 0.0          # barrel undersize vs. drilled hole (v2: was 0.15)
CHAMF = 1.0         # wire-side edge chamfer on the hole
IN = 25.4

# name, drill size (mm), hole: ("round", d) or ("slot", w, l), qty
PARTS = [
    ("0ga main power",   7/8 * IN, ("round", 17.5),        1),
    ("4ga power",        5/8 * IN, ("round", 12.8),        1),
    ("4ga ground",       5/8 * IN, ("round", 12.8),        1),
    ("RCA pair",         3/4 * IN, ("round", 14.0),        1),
    ("12ga speaker",     5/8 * IN, ("slot", 5.6, 10.6),    1),
    ("14ga speaker",     1/2 * IN, ("slot", 5.0, 9.2),     1),
]


def hole_profile(spec, grow=0.0):
    if spec[0] == "round":
        return CrossSection.circle(spec[1] / 2 + grow, SEG)
    _, w, l = spec
    r = w / 2 + grow
    off = (l - w) / 2
    c1 = CrossSection.circle(r, SEG).translate((-off, 0))
    c2 = CrossSection.circle(r, SEG).translate((off, 0))
    box = CrossSection.square((2 * off, 2 * r), center=True)
    return c1 + c2 + box


def hole_cutter(spec, height):
    """Through-hole plus a chamfer at both ends."""
    body = hole_profile(spec).extrude(height + 2).translate((0, 0, -1))
    cut = body
    for z0, z1, g0, g1 in [(-0.01, CHAMF, CHAMF + 0.01, 0.0),
                           (height - CHAMF, height + 0.01, 0.0, CHAMF + 0.01)]:
        # stack thin layers to approximate an offset-chamfer that works for slots too
        steps = 8
        for i in range(steps):
            za = z0 + (z1 - z0) * i / steps
            zb = z0 + (z1 - z0) * (i + 1) / steps
            g = g0 + (g1 - g0) * (i + 0.5) / steps
            cut = cut + hole_profile(spec, g).extrude(zb - za + 0.001).translate((0, 0, za))
    return cut


def grommet(drill, spec):
    barrel_r = drill / 2 - CLEAR
    flange_r = drill / 2 + FLANGE_LIP
    total = FLANGE_T + BARREL_L

    flange = Manifold.cylinder(FLANGE_T - 0.6, flange_r, flange_r, SEG)
    # small rounded-over top edge on the flange (chamfer)
    flange += Manifold.cylinder(0.6, flange_r, flange_r - 0.6, SEG).translate((0, 0, FLANGE_T - 0.6))

    # barrel with a lead-in taper at the end
    barrel = Manifold.cylinder(BARREL_L - 0.8, barrel_r, barrel_r, SEG).translate((0, 0, FLANGE_T))
    barrel += Manifold.cylinder(0.8, barrel_r, barrel_r - 0.6, SEG).translate((0, 0, total - 0.8))

    ribs = Manifold()
    rib_x = drill / 2 + RIB_PROUD - RIB_R
    rib_len = BARREL_L - 1.5
    for i in range(RIB_COUNT):
        a = 360 * i / RIB_COUNT
        rib = Manifold.cylinder(rib_len, RIB_R, RIB_R, 24).translate((rib_x, 0, FLANGE_T))
        ribs += rib.rotate((0, 0, a))

    part = flange + barrel + ribs
    part -= hole_cutter(spec, total)
    return part, flange_r


def layout():
    pieces = []
    for name, drill, spec, qty in PARTS:
        for _ in range(qty):
            p, r = grommet(drill, spec)
            pieces.append((name, p, r))
    # simple 3-wide grid, largest first
    pieces.sort(key=lambda t: -t[2])
    gap = 5.0
    cols = 3
    cell = max(r for _, _, r in pieces) * 2 + gap
    plate = Manifold()
    placed = []
    for i, (name, p, r) in enumerate(pieces):
        x = (i % cols) * cell
        y = -(i // cols) * cell
        plate += p.translate((x, y, 0))
        placed.append((name, x, y))
    return plate, placed


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "amp_rack_grommets.stl"
    plate, placed = layout()
    m = plate.to_mesh()
    mesh = trimesh.Trimesh(np.asarray(m.vert_properties)[:, :3], np.asarray(m.tri_verts))
    mesh.apply_translation(-mesh.bounds[0] * [1, 1, 1])
    mesh.export(out)
    print("watertight:", mesh.is_watertight, "bodies:", len(mesh.split()))
    print("plate size (mm):", np.round(mesh.extents, 1))
    for name, x, y in placed:
        print(name, x, y)
