#!/usr/bin/env python3
# Generate blockMeshDict for n tiled groove units (each unit width = 5).
# Preserves your cell counts/edgeGradings and avoids internal-face patching
# by emitting exact 4-vertex patch faces built once.

import argparse
from textwrap import dedent

# ---- Geometry params (same semantics as your working file) ----
SCALE = "0.01"                 # blockMesh 'scale' (cm -> m)
HAR = "1"                      # thickness in z (cm before scale)
GROOVE_HEIGHT = "-1.7"         # y of groove floor
ABSORB_WALL_HEIGHT = "2.1"     # top wall y (absorbing wall)

# Unit pattern along x (width 5): flat 0→1, groove 1→4, flat 4→5
W  = 5.0
A  = 1.0
B  = 4.0

# Channel block resolutions (match your dict)
NX_SHORT = 15   # for 0→1 and 4→5 spans
NX_LONG  = 45   # for 1→4 groove spans
NY = 40
NZ = 1

# Wall (absorb) block resolution
WALL_NX_SHORT = 15
WALL_NX_LONG  = 45
WALL_NY = 5
WALL_NZ = 1

# Edge-grading templates (copied from your file)
EG_A = ".1 1 1 .1\n        ((.5 .5 10)(.5 .5 .1)) ((.5 .5 10)(.5 .5 .1)) ((.5 .5 10)(.5 .5 .1)) ((.5 .5 10)(.5 .5 .1))\n        1 1 1 1"
EG_B = "((.5 .5 10)(.5 .5 .1)) 1 1 ((.5 .5 10)(.5 .5 .1))\n        ((.5 .5 10)(.5 .5 .1)) ((.5 .5 10)(.5 .5 .1)) ((.5 .5 10)(.5 .5 .1)) ((.5 .5 10)(.5 .5 .1))\n        1 1 1 1"
EG_C = "10 1 1 10\n        ((.5 .5 10)(.5 .5 .1)) ((.5 .5 10)(.5 .5 .1)) ((.5 .5 10)(.5 .5 .1)) ((.5 .5 10)(.5 .5 .1))\n        1 1 1 1"
EG_D = "1 ((.5 .5 10)(.5 .5 .1)) ((.5 .5 10)(.5 .5 .1)) 1\n        .1 .1 .1 .1\n        1 1 1 1"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, required=True, help="number of groove units to tile")
    ap.add_argument("--out", type=str, default="system/blockMeshDict")
    args = ap.parse_args()
    n = args.n
    X_end = n * W

    # ---- Vertex table ----
    verts = []           # list[(x,y,z)]
    vid = {}             # map (x, yTag, zTag) -> index

    def add_vert(x, y, z):
        verts.append((x, y, z))
        return len(verts) - 1

    def ensure(x, yTag, zTag):
        key = (float(x), yTag, zTag)
        if key in vid:
            return vid[key]
        if yTag == 'y2':     y = 2.0
        elif yTag == 'y0':   y = 0.0
        elif yTag == 'yg':   y = float(GROOVE_HEIGHT)
        elif yTag == 'yTop': y = float(ABSORB_WALL_HEIGHT)
        else: raise ValueError("bad yTag")
        if zTag == 'z0':     z = 0.0
        elif zTag == 'zH':   z = float(HAR)
        else: raise ValueError("bad zTag")
        idx = add_vert(float(x), y, z)
        vid[key] = idx
        return idx

    # x-positions used in the mesh
    xs = sorted({0.0} | {k*W + o for k in range(n) for o in (0.0, A, B, W)} | {X_end})

    # Build “flat” y-level vertices (y2, y0, yTop) at z0/zH
    for x in xs:
        for yTag in ('y2','y0','yTop'):
            ensure(x, yTag, 'z0')
            ensure(x, yTag, 'zH')

    # Build “groove” y-level vertices (yg) at z0/zH only at groove edges (x=A,B in each unit)
    for k in range(n):
        for x in (k*W + A, k*W + B):
            ensure(x, 'yg', 'z0')
            ensure(x, 'yg', 'zH')

    # ---- Helpers for hexahedra ----
    def quad(xA, xB, yLo, yHi, zTag):
        # Order matches your pattern: (xA,yLo,z) (xB,yLo,z) (xB,yHi,z) (xA,yHi,z)
        return (ensure(xA, yLo, zTag), ensure(xB, yLo, zTag),
                ensure(xB, yHi, zTag), ensure(xA, yHi, zTag))

    def hex8(xA, xB, yLo, yHi):
        a0,a1,a2,a3 = quad(xA, xB, yLo, yHi, 'z0')
        b0,b1,b2,b3 = quad(xA, xB, yLo, yHi, 'zH')
        return (a0,a1,a2,a3,b0,b1,b2,b3)

    # ---- Channel blocks (4 per unit) ----
    chan_blocks = []  # list of (nx,ny,nz, edgeGradingStr, hex)
    for k in range(n):
        xL = k*W + 0.0
        xG1= k*W + A
        xG2= k*W + B
        xR = k*W + W
        # A: flat 0→1
        chan_blocks.append((NX_SHORT, NY, NZ, EG_A, hex8(xL, xG1, 'y0','y2')))
        # B: span 1→4
        chan_blocks.append((NX_LONG,  NY, NZ, EG_B, hex8(xG1,xG2, 'y0','y2')))
        # C: flat 4→5
        chan_blocks.append((NX_SHORT, NY, NZ, EG_C, hex8(xG2,xR,  'y0','y2')))
        # D: groove cavity 1→4 (yg→y0)
        chan_blocks.append((NX_LONG,  NY, NZ, EG_D, hex8(xG1,xG2, 'yg','y0')))

    # ---- Wall blocks above y=2 (3 per unit) ----
    wall_blocks = []   # list of (nx,ny,nz, hex)
    for k in range(n):
        xL = k*W + 0.0
        xG1= k*W + A
        xG2= k*W + B
        xR = k*W + W
        wall_blocks.append((WALL_NX_SHORT, WALL_NY, WALL_NZ, hex8(xL, xG1, 'y2','yTop')))
        wall_blocks.append((WALL_NX_LONG,  WALL_NY, WALL_NZ, hex8(xG1,xG2, 'y2','yTop')))
        wall_blocks.append((WALL_NX_SHORT, WALL_NY, WALL_NZ, hex8(xG2,xR,  'y2','yTop')))

    # ---- Boundary faces (exact 4-tuples, no recomputation later) ----

    # inlet at x=0  => (4 0 10 14) style: (y0,z0)->(y2,z0)->(y2,zH)->(y0,zH)
    inlet_face = (
        ensure(0.0,'y0','z0'),
        ensure(0.0,'y2','z0'),
        ensure(0.0,'y2','zH'),
        ensure(0.0,'y0','zH'),
    )

    # outlet at x=X_end
    outlet_face = (
        ensure(X_end,'y0','z0'),
        ensure(X_end,'y2','z0'),
        ensure(X_end,'y2','zH'),
        ensure(X_end,'y0','zH'),
    )

    # top faces (yTop across each span in each unit)
    top_faces = []
    for k in range(n):
        xL = k*W + 0.0; xG1 = k*W + A; xG2 = k*W + B; xR = k*W + W
        for xa, xb in ((xL,xG1),(xG1,xG2),(xG2,xR)):
            top_faces.append((
                ensure(xa,'yTop','z0'), ensure(xb,'yTop','z0'),
                ensure(xb,'yTop','zH'), ensure(xa,'yTop','zH'),
            ))

    # bottom faces: flats, groove floor, vertical groove walls (left & right)
    bottom_faces = []
    for k in range(n):
        xL = k*W + 0.0; xG1= k*W + A; xG2= k*W + B; xR = k*W + W
        # flat bottom xL→xG1 : like (14 15 5 4) but generalized
        bottom_faces.append((
            ensure(xL,'y0','zH'), ensure(xG1,'y0','zH'),
            ensure(xG1,'y0','z0'), ensure(xL,'y0','z0'),
        ))
        # flat bottom xG2→xR
        bottom_faces.append((
            ensure(xG2,'y0','zH'), ensure(xR,'y0','zH'),
            ensure(xR,'y0','z0'), ensure(xG2,'y0','z0'),
        ))
        # groove floor xG1→xG2 : like (18 19 9 8)
        bottom_faces.append((
            ensure(xG1,'yg','zH'), ensure(xG2,'yg','zH'),
            ensure(xG2,'yg','z0'), ensure(xG1,'yg','z0'),
        ))
        # groove left wall @ xG1 : like (8 5 15 18)
        bottom_faces.append((
            ensure(xG1,'yg','z0'), ensure(xG1,'y0','z0'),
            ensure(xG1,'y0','zH'), ensure(xG1,'yg','zH'),
        ))
        # groove right wall @ xG2 : like (9 6 16 19)
        bottom_faces.append((
            ensure(xG2,'yg','z0'), ensure(xG2,'y0','z0'),
            ensure(xG2,'y0','zH'), ensure(xG2,'yg','zH'),
        ))

    # side walls at x=0 and x=X_end : follow (10 0 20 24) / (rightmost analog)
    wallSides = [
        (ensure(0.0,'y2','zH'),  ensure(0.0,'y2','z0'),
         ensure(0.0,'yTop','z0'),ensure(0.0,'yTop','zH')),
        (ensure(X_end,'y2','zH'), ensure(X_end,'y2','z0'),
         ensure(X_end,'yTop','z0'), ensure(X_end,'yTop','zH')),
    ]

    # front/back empties: z-faces for all blocks
    fb_faces = []
    def zfaces_of_hex(h):
        a0,a1,a2,a3,b0,b1,b2,b3 = h
        return ( (a0,a1,a2,a3), (b0,b1,b2,b3) )
    for _,_,_,_,h in chan_blocks:       # 5-tuple
        fb_faces += list(zfaces_of_hex(h))
    for _,_,_,h in wall_blocks:         # 4-tuple
        fb_faces += list(zfaces_of_hex(h))

    # ---- Emit blockMeshDict ----
    out = []
    out.append(dedent(f"""\
    /*--------------------------------*- C++ -*----------------------------------*\\
    | =========                 |                                                 |
    | \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
    |  \\\\    /   O peration     | Version:  v2306                                 |
    |   \\\\  /    A nd           | Website:  www.openfoam.com                      |
    |    \\\\/     M anipulation  |                                                 |
    \\*---------------------------------------------------------------------------*/
    FoamFile
    {{
        version     2.0;
        format      ascii;
        class       dictionary;
        object      blockMeshDict;
    }}
    // * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

    scale {SCALE};

    HAR {HAR};
    GROOVE_HEIGHT {GROOVE_HEIGHT};
    ABSORB_WALL_HEIGHT {ABSORB_WALL_HEIGHT};

    vertices
    (
    """))

    for i,(x,y,z) in enumerate(verts):
        out.append(f"    ({x:g} {y:g} {z:g}) // {i}\n")
    out.append(");\n\nblocks\n(\n")

    # channel blocks
    for (nx,ny,nz,eg,h) in chan_blocks:
        a0,a1,a2,a3,b0,b1,b2,b3 = h
        out.append("    hex (%d %d %d %d %d %d %d %d) channel (%d %d %d) edgeGrading (%s)\n\n"
                   % (a0,a1,a2,a3,b0,b1,b2,b3, nx,ny,nz, eg))
    # wall blocks
    for (nx,ny,nz,h) in wall_blocks:
        a0,a1,a2,a3,b0,b1,b2,b3 = h
        out.append("    hex (%d %d %d %d %d %d %d %d) wall (%d %d %d) simpleGrading (1 1 1)\n"
                   % (a0,a1,a2,a3,b0,b1,b2,b3, nx,ny,nz))

    out.append(");\n\nedges\n(\n);\n\nboundary\n(\n")

    # inlet
    out.append("    inlet\n    {\n        type patch;\n        faces\n        (\n")
    a,b,c,d = inlet_face
    out.append(f"            ({a} {b} {c} {d})\n")
    out.append("        );\n    }\n")

    # outlet
    out.append("    outlet\n    {\n        type patch;\n        faces\n        (\n")
    a,b,c,d = outlet_face
    out.append(f"            ({a} {b} {c} {d})\n")
    out.append("        );\n    }\n")

    # top
    out.append("    top\n    {\n        type patch;\n        faces\n        (\n")
    for a,b,c,d in top_faces:
        out.append(f"            ({a} {b} {c} {d})\n")
    out.append("        );\n    }\n")

    # bottom
    out.append("    bottom\n    {\n        type patch;\n        faces\n        (\n")
    for a,b,c,d in bottom_faces:
        out.append(f"            ({a} {b} {c} {d})\n")
    out.append("        );\n    }\n")

    # side walls
    out.append("    wallSides\n    {\n        type wall;\n        faces\n        (\n")
    for a,b,c,d in wallSides:
        out.append(f"            ({a} {b} {c} {d})\n")
    out.append("        );\n    }\n")

    # front/back empties
    out.append("    frontAndBackPlanes\n    {\n        type empty;\n        faces\n        (\n")
    for a,b,c,d in fb_faces:
        out.append(f"            ({a} {b} {c} {d})\n")
    out.append("        );\n    }\n")

    out.append(");\n\n// ************************************************************************* //\n")

    with open(args.out, "w") as f:
        f.writelines(out)

if __name__ == "__main__":
    main()