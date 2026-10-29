# Bronco Amp Rack Grommets

Flanged press-in grommets for the amp rack wiring. Generated in Python (manifold3d + trimesh);
the STLs in `stl/` are build outputs of the scripts in `src/`.

## Drill sizes

| Grommet | Drill / hole saw | Metric | Wire opening |
|---|---|---|---|
| 0 ga main power | 7/8" | 22.2 mm | 17.5 mm round |
| 4 ga power / ground | 5/8" | 15.9 mm | 12.8 mm round |
| RCA pair | 3/4" | 19.1 mm | 14 mm round |
| 12 ga speaker | 5/8" | 15.9 mm | 5.6 × 10.6 mm slot |
| 14 ga speaker | 1/2" | 12.7 mm | 5.0 × 9.2 mm slot |

Reference: 4 ga size based on the Sky High Car Audio plastic grommet (15.91 mm cutout, 12.76 mm ID).

## Versions

| Version | Change | Status |
|---|---|---|
| v1 | Initial design, 3.5 mm flange lip | Too loose in hole |
| v2 | Barrel to full drill size, ribs 0.45 mm proud | Good fit |
| v3 | Flange lip halved to 1.75 mm; 12-up plates per size | Tested, works (superseded) |
| v4 | 1.0 mm lip, 1.2 mm flange, hollow 1.2 mm barrel wall (35–60% less plastic) | **Tested, perfect fit — current version** |

## Printing

Use the files in `stl/v4/`: `grommets_v4_test_set.stl` (one of each) or the `_x12_v4` plates for bulk.

- Flange-down on the bed, no supports.
- PETG or ASA (PLA can soften in a hot cab).
- Spacing between holes: half of each drill size + 2 mm (v4), + 3.5 mm (v3).

## Rebuild

```bash
pip install manifold3d trimesh numpy
cd src
python grommets.py ../stl/v1-v3/amp_rack_grommets_v3.stl   # v3 one-of-each plate
python plates.py                                             # v3 12-up plates (writes plates/)
mkdir -p plates_v4 && python grommets_v4.py                  # v4 test set + 12-up plates
```
