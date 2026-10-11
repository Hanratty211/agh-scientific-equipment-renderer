#!/usr/bin/env python3
"""Case 1: 171Yb spin-1/2 optical lattice clock (NIST, PRL 2009, arXiv:0906.1219)
Schematic of the research system / experimental apparatus.

All labels are grounded in the paper text (see case-1/notes/source-facts.md).
Unverified elements (oven/collimator, Zeeman slower) are drawn as DASHED
"uncertain" outlines and listed in the report.

Output: figure_output_171Yb_schematic.svg  (rsvg-convert -> PNG)
"""
W, H = 1360, 760
OUT = "figure_output_171Yb_schematic.svg"

parts = []
p = parts.append

p(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
  f'viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">')
p('<defs>')
# arrow markers
for mid in [("ah", "#444"), ("ar", "#b02a37"), ("ag", "#1a6b52"), ("ap", "#7c5cbf"),
            ("ab", "#2b6ca3"), ("ao", "#c56a1f")]:
    nid, col = mid
    p(f'<marker id="{nid}" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
      f'<path d="M0,0 L8,4 L0,8 z" fill="{col}"/></marker>')
p('</defs>')
p(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fbfcfd"/>')

def box(x, y, w, h, fill="#fff", stroke="#444", sw=1.5, rx=8, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    p(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
      f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

def txt(x, y, s, size=13, fill="#222", anchor="start", weight="normal", style=None):
    import html as _h
    s = _h.escape(s, quote=False)
    st = f' font-style="{style}"' if style else ''
    p(f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
      f'font-weight="{weight}"{st}>{s}</text>')

def line(x1, y1, x2, y2, color="#444", w=2.2, marker=None, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    m = f' marker-end="url(#{marker})"' if marker else ''
    p(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
      f'stroke-width="{w}"{d}{m}/>')

# ================= title =================
txt(20, 34, '171Yb Spin-1/2 Optical Lattice Clock - Apparatus & Experimental Sequence',
    20, weight="bold")
txt(20, 54, 'NIST (Lemke et al., PRL 2009, arXiv:0906.1219); dashed outlines = not described in this paper',
    11, fill="#777")

# ================= main vacuum system (left) =================
# vacuum chamber
box(60, 100, 620, 480, fill="#f4f7f9", stroke="#9aa5ad", sw=2)
txt(72, 122, 'Main vacuum system (UHV)', 12, fill="#5a656d")

# --- atomic beam / oven (UNVERIFIED, dashed) ---
box(90, 140, 150, 80, fill="#fff", stroke="#8a8f94", sw=1.5, dash="6 4")
txt(165, 168, 'Heated Yb oven', 13, anchor="middle")
txt(165, 186, 'thermal 171Yb beam', 11, anchor="middle", fill="#8a8f94")
txt(165, 201, 'not described in [ref]', 9, anchor="middle", fill="#b04a4a")
line(240, 180, 330, 180, "#8a8f94", 1.8, marker="ah", dash="6 4")
txt(285, 170, 'beam', 10, anchor="middle", fill="#8a8f94")

# --- Zeeman slower (UNVERIFIED, dashed) ---
box(330, 150, 130, 60, fill="#fff", stroke="#8a8f94", sw=1.5, dash="6 4")
txt(395, 176, 'Zeeman slower', 12, anchor="middle")
txt(395, 193, 'not described in [ref]', 9, anchor="middle", fill="#b04a4a")
line(460, 180, 560, 180, "#8a8f94", 1.8, marker="ah", dash="6 4")

# --- MOT region ---
box(560, 140, 230, 200, fill="#eef3f8", stroke="#2b6ca3", sw=2)
txt(675, 163, 'MOT region', 14, anchor="middle", weight="bold", fill="#1d4e79")
# cooling beams (399 nm, six-beam MOT)
line(580, 320, 770, 320, "#1a6b52", 2.5, marker="ag")
txt(675, 338, '399 nm 1S0-1P1 cooling / trapping beams (6-beam MOT)',
    11, anchor="middle", fill="#145241")
line(675, 355, 675, 430, "#1a6b52", 2.5, marker="ag")
txt(683, 428, 'repump 556 nm (1S0-3P1)', 11, fill="#145241")
txt(568, 445, 'atoms: 3e4, T ~15 uK after 399+556 nm cooling',
    11, fill="#5a656d")
txt(568, 462, '99% optical pumping to a single mF (+-1/2, alternating)',
    11, fill="#5a656d")

# --- atom transfer to lattice (arrow from MOT) ---
line(675, 470, 675, 560, "#444", 2.5, marker="ah")
txt(683, 520, 'slow-down + load into 1D lattice', 11, fill="#5a656d")

# --- 1D optical lattice (horizontal) ---
box(560, 570, 230, 70, fill="#f3ecfa", stroke="#7c5cbf", sw=2)
txt(675, 594, '1D optical lattice (horizontal)', 13, anchor="middle", weight="bold", fill="#4f3d8f")
txt(675, 612, 'counter-propagating 759 nm beams', 11, anchor="middle", fill="#4f3d8f")
txt(675, 628, 'magic frequency 394 798 329(10) MHz; depth 500 E_R (50 uK)',
    10, anchor="middle", fill="#4f3d8f")
# lattice counter-propagating beam arrows
line(770, 545, 580, 545, "#7c5cbf", 2, marker="ap", dash="2 0")
line(580, 650, 770, 650, "#7c5cbf", 2, marker="ap", dash="2 0")

# --- vertical B-field for spectroscopy ---
box(330, 380, 150, 130, fill="#fdf6e8", stroke="#c56a1f", sw=2)
txt(405, 404, 'Applied B field', 12, anchor="middle", weight="bold", fill="#8a4a10")
txt(405, 422, '0.11 mT, vertical', 11, anchor="middle", fill="#8a4a10")
txt(405, 440, 'first-order Zeeman effect', 10, anchor="middle", fill="#8a4a10")
txt(405, 454, 'canceled by mF=+-1/2 averaging', 10, anchor="middle", fill="#8a4a10")
line(405, 380, 405, 510, "#c56a1f", 2, marker="ao")
line(405, 510, 405, 380, "#c56a1f", 1, marker="ao", dash="4 3")

# ================= right column: laser & detection =================
txt(740, 92, 'Laser & detection systems', 15, weight="bold", fill="#333")

# 399 nm laser
box(740, 110, 250, 70, fill="#fff", stroke="#1a6b52", sw=2)
txt(865, 134, '399 nm laser (1S0-1P1)', 13, anchor="middle", weight="bold", fill="#145241")
txt(865, 154, 'cooling, slowing beam, and detection pulses', 11, anchor="middle", fill="#145241")
txt(865, 170, '3 x 5 ms pulses for state readout', 11, anchor="middle", fill="#145241")

# 556 nm laser
box(740, 196, 250, 58, fill="#fff", stroke="#1a6b52", sw=2)
txt(865, 218, '556 nm laser (1S0-3P1)', 13, anchor="middle", weight="bold", fill="#145241")
txt(865, 238, 'narrow-line cooling + optical pumping (99%)', 11, anchor="middle", fill="#145241")

# lattice laser (magic)
box(740, 270, 250, 58, fill="#fff", stroke="#7c5cbf", sw=2)
txt(865, 292, 'Magic-wavelength lattice laser', 13, anchor="middle", weight="bold", fill="#4f3d8f")
txt(865, 312, '759 nm; 394 798 329(10) MHz (magic)', 11, anchor="middle", fill="#4f3d8f")

# 578 nm clock laser
box(740, 344, 250, 58, fill="#fff", stroke="#b02a37", sw=2)
txt(865, 366, '578 nm clock laser (1S0-3P0)', 13, anchor="middle", weight="bold", fill="#7d1a24")
txt(865, 386, 'pi-pulse 80 ms; Fourier-limited 10 Hz', 11, anchor="middle", fill="#7d1a24")

# pre-stabilized cavity
box(740, 418, 250, 58, fill="#fff", stroke="#2b6ca3", sw=2)
txt(865, 440, 'High-finesse pre-stabilization cavity', 13, anchor="middle", weight="bold", fill="#1d4e79")
txt(865, 460, '578 nm pre-stabilized (env. isolated)', 11, anchor="middle", fill="#1d4e79")

# 1388 nm repump
box(740, 492, 250, 58, fill="#fff", stroke="#c56a1f", sw=2)
txt(865, 514, '1388 nm repump laser', 13, anchor="middle", weight="bold", fill="#8a4a10")
txt(865, 534, '3P0-3D1: returns excited clock atoms to 1S0', 11, anchor="middle", fill="#8a4a10")

# detection: PMT + microprocessor
box(740, 566, 250, 76, fill="#f4f7f9", stroke="#444", sw=2)
txt(865, 588, 'Fluorescence detection (399 nm scattered)', 12, anchor="middle", weight="bold", fill="#333")
txt(865, 606, 'photomultiplier tube (PMT)', 11, anchor="middle")
txt(865, 624, '3-pulse seq -> microproc -> normalized fraction',
    10, anchor="middle", fill="#5a656d")

# ================= arrows: lasers -> interaction region =================
line(740, 145, 500, 250, "#1a6b52", 2, marker="ag", dash="5 4")
line(740, 225, 500, 290, "#1a6b52", 2, marker="ag", dash="5 4")
line(740, 299, 520, 600, "#7c5cbf", 2, marker="ap", dash="5 4")
line(740, 373, 520, 590, "#b02a37", 2, marker="ar", dash="5 4")
line(740, 447, 500, 560, "#2b6ca3", 2, marker="ab", dash="5 4")
line(740, 521, 540, 565, "#c56a1f", 2, marker="ao", dash="5 4")

# scattered light out to PMT
line(560, 590, 740, 590, "#555", 2, marker="ah")
txt(650, 582, 'scattered 399 nm', 10, fill="#555")

# ================= sequence strip (bottom) =================
seq_y = 672
txt(60, seq_y - 8, 'Experimental sequence (per cycle):', 13, weight="bold")
steps = [
    ('1  oven / thermal Yb beam', "#8a8f94", True),
    ('2  MOT cooling 399+556 nm', "#1a6b52", False),
    ('3  load into 1D lattice', "#7c5cbf", False),
    ('4  optical pump to mF=+-1/2', "#1a6b52", False),
    ('5  578 nm pi-pulse on clock line', "#b02a37", False),
    ('6  399 nm 3-pulse readout to PMT', "#555", False),
]
sx = 60
for i, (label, col, dashed) in enumerate(steps):
    wlen = 150
    box(sx, seq_y, wlen, 52, fill="#fff", stroke=col, sw=1.6, dash="5 3" if dashed else None)
    txt(sx + wlen/2, seq_y + 20, label, 10, anchor="middle", fill=col)
    if i == 0:
        txt(sx + wlen/2, seq_y + 38, '(uncertain)', 9, anchor="middle", fill="#b04a4a")
    if i != len(steps)-1:
        line(sx + wlen + 2, seq_y + 26, sx + wlen + 16, seq_y + 26, "#666", 1.8, marker="ah")
    sx += wlen + 18

# ================= legend (right of sequence) =================
box(1010, 672, 330, 76, fill="#f7f8fa", stroke="#bbb", sw=1.2)
txt(1024, 692, 'Legend', 12, weight="bold")
line(1024, 706, 1064, 706, "#1a6b52", 2.2, marker="ag")
txt(1070, 710, 'solid = described in paper', 11, fill="#555")
line(1024, 726, 1064, 726, "#8a8f94", 1.8, marker="ah", dash="6 4")
txt(1070, 730, 'dashed = not described in paper', 11, fill="#b04a4a")

p('</svg>')

open(OUT, "w").write("\n".join(parts))
print("wrote", OUT)
