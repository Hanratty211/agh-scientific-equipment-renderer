"""V28 acoustic metamaterial nanogenerator build_v01.py
Acoustic metamaterial multi-band sound insulation + acoustic-electric conversion
device: periodic metamaterial panel with piezoelectric sensing/conversion units,
excitation source, measurement chain.
Based on 10.3390/s25216693 (MDPI Sensors, 25(21):6693, OA/BY license).
No local PDF; B-class system architecture reconstruction from SELECTION.md description.
"""
import bpy, math, mathutils, os, hashlib

def setup():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = 'METRIC'
    sc.render.resolution_x = 1280
    sc.render.resolution_y = 960
    sc.render.engine = 'BLENDER_EEVEE'
    sc.render.image_settings.file_format = 'PNG'
    w = bpy.data.worlds.new("W")
    bpy.context.scene.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.05,0.05,0.07,1.0)
    return sc

def mat(name, base, rough=0.5, metal=0.0, emis=None, es=0.0, alpha=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    if alpha < 1.0:
        m.blend_method = 'BLEND'
        m.show_transparent_back = False
    n = m.node_tree.nodes.get("Principled BSDF")
    n.inputs["Base Color"].default_value = base + (alpha,)
    n.inputs["Roughness"].default_value = rough
    n.inputs["Metallic"].default_value = metal
    if emis:
        n.inputs["Emission Color"].default_value = emis + (1.0,)
        n.inputs["Emission Strength"].default_value = es
    tw = n.inputs.get("Transmission Weight")
    if tw: tw.default_value = 1.0 - alpha
    return m

def box(name, sx, sy, sz, loc, m=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object; o.name = name; o.scale = (sx, sy, sz)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if m: o.data.materials.append(m)
    return o

def cyl(name, r, depth, loc, rot=(0,0,0), m=None, seg=32):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=seg)
    o = bpy.context.object; o.name = name
    if m: o.data.materials.append(m)
    return o

def torus(name, R, r, loc, m=None, s1=96, s2=20):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc, major_segments=s1, minor_segments=s2)
    o = bpy.context.object; o.name = name
    if m: o.data.materials.append(m)
    return o

def wire(name, p0, p1, r=0.001, m=None):
    v = mathutils.Vector(p1)-mathutils.Vector(p0)
    mid = (mathutils.Vector(p0)+mathutils.Vector(p1))/2
    rot = v.to_track_quat('Z','Y').to_euler()
    o = cyl(name, r, v.length, tuple(mid), tuple(rot), m, seg=12)
    o['wire_p0'] = tuple(p0); o['wire_p1'] = tuple(p1)
    return o

sc = setup()

# ==== Dimensions ====
Z0 = 0.03   # panel bottom z (on stand)
ZP = Z0 + 0.08   # panel center z
# Metamaterial panel: 0.3m x 0.2m, with periodic unit cells
PANEL_W = 0.30
PANEL_D = 0.20
PANEL_H = 0.08
N_CELLS_X = 5
N_CELLS_Y = 3
CELL_W = PANEL_W / N_CELLS_X
CELL_D = PANEL_D / N_CELLS_Y

# ==== Materials ====
M_panel  = mat("panel_base", (0.40,0.42,0.48), rough=0.4, metal=0.3, alpha=0.85)
M_cell   = mat("cell_frame", (0.30,0.32,0.38), rough=0.4, metal=0.4)
M_piezo  = mat("piezo",      (0.70,0.30,0.80), rough=0.3, metal=0.1, emis=(0.7,0.3,0.8), es=0.4)
M_wire   = mat("wire_c",     (0.10,0.10,0.12), rough=0.5, metal=0.5)
M_gold   = mat("gold_p",     (1.00,0.80,0.10), rough=0.2, metal=0.8)
M_speaker= mat("speaker",    (0.08,0.08,0.10), rough=0.5, metal=0.4)
M_mic    = mat("mic_head",   (0.05,0.05,0.08), rough=0.3, metal=0.7)
M_ampl   = mat("amplifier",  (0.05,0.05,0.08), rough=0.5, metal=0.5)
M_oscil  = mat("osc_box",    (0.10,0.10,0.12), rough=0.5, metal=0.4)
M_stand  = mat("stand_base", (0.15,0.13,0.10), rough=0.6, metal=0.4)
M_beam   = mat("acoustic_w", (0.5,0.5,1.0), rough=0.1, emis=(0.5,0.5,1.0), es=2.0, alpha=0.6)
M_speaker_cone = mat("cone",(0.15,0.15,0.18), rough=0.5, metal=0.2)

# ==== Support base ====
box("support_base", PANEL_W+0.10, PANEL_D+0.10, 0.02, (0, 0, Z0-0.01), M_stand)
for i,(lx,ly) in enumerate([(PANEL_W/2+0.02, PANEL_D/2+0.02),(-PANEL_W/2-0.02, PANEL_D/2+0.02),
                              (PANEL_W/2+0.02,-PANEL_D/2-0.02),(-PANEL_W/2-0.02,-PANEL_D/2-0.02)]):
    cyl(f"stand_leg_{i}", 0.008, Z0-0.02, (lx, ly, (Z0-0.02)/2), (0,0,0), M_stand, seg=16)

# ==== Metamaterial panel (semi-transparent base) ====
box("panel_body", PANEL_W, PANEL_D, PANEL_H, (0, 0, ZP), M_panel)

# ==== Periodic unit cells (multi-band acoustic metamaterial + piezo) ====
# Each cell: frame + central piezo disc
for ix in range(N_CELLS_X):
    for iy in range(N_CELLS_Y):
        cx = -PANEL_W/2 + (ix+0.5)*CELL_W
        cy = -PANEL_D/2 + (iy+0.5)*CELL_D
        # Cell frame (box outline)
        frame_sz = 0.004
        box(f"cell_frame_{ix}_{iy}", CELL_W-0.008, CELL_D-0.008, frame_sz, (cx, cy, ZP-PANEL_H/2+0.002), M_cell)
        box(f"cell_frame_top_{ix}_{iy}", CELL_W-0.008, CELL_D-0.008, frame_sz, (cx, cy, ZP+PANEL_H/2-0.002), M_cell)
        # Central piezo disc (vibration sensing/conversion)
        cyl(f"piezo_{ix}_{iy}", min(CELL_W,CELL_D)*0.3, 0.003, (cx, cy, ZP), (0,0,0), M_piezo, seg=32)
        # Gold electrode pads
        cyl(f"piezo_gold_{ix}_{iy}", min(CELL_W,CELL_D)*0.2, 0.001, (cx, cy, ZP+0.002), (0,0,0), M_gold, seg=24)

# ==== Speaker / excitation source (left side) ====
spk_x = -PANEL_W/2 - 0.08
box("speaker_body", 0.06, 0.06, 0.08, (spk_x, 0, ZP), M_speaker)
cyl("speaker_cone", 0.025, 0.02, (spk_x+0.035, 0, ZP), (0, math.pi/2, 0), M_speaker_cone, seg=32)
# Acoustic wave beam (simplified cone from speaker to panel)
beam_start = (spk_x+0.05, 0, ZP)
beam_end   = (-PANEL_W/2, 0, ZP)
v = mathutils.Vector(beam_end)-mathutils.Vector(beam_start)
mid = (mathutils.Vector(beam_start)+mathutils.Vector(beam_end))/2
rot = v.to_track_quat('Z','Y').to_euler()
o = cyl("acoustic_wave", 0.03, v.length, tuple(mid), tuple(rot), M_beam, seg=16)
o['beam_p0'] = tuple(beam_start); o['beam_p1'] = tuple(beam_end)

# Speaker wires
wire("spk_wire1", (spk_x, -0.04, ZP-0.02), (-PANEL_W/2-0.06, -0.06, Z0-0.01), r=0.0015, m=M_wire)
wire("spk_wire2", (spk_x,  0.04, ZP-0.02), (-PANEL_W/2-0.06,  0.06, Z0-0.01), r=0.0015, m=M_wire)

# ==== Microphone (right side, detects transmitted/attenuated sound) ====
mic_x = PANEL_W/2 + 0.06
box("mic_body", 0.03, 0.03, 0.04, (mic_x, 0, ZP), M_mic)
cyl("mic_head", 0.012, 0.015, (mic_x-0.02, 0, ZP), (0, math.pi/2, 0), M_mic, seg=24)
wire("mic_wire", (mic_x, 0, ZP-0.02), (PANEL_W/2+0.04, -0.06, Z0-0.01), r=0.001, m=M_wire)

# ==== Signal chain: amplifier + oscilloscope (on base) ====
box("amp_box", 0.08, 0.05, 0.03, (0.05, -PANEL_D/2-0.05, Z0-0.005), M_ampl)
# Piezo -> amplifier wire
wire("piezo_amp_wire", (0.0, -PANEL_D/2+0.02, ZP), (0.05, -PANEL_D/2-0.03, Z0-0.005), r=0.001, m=M_wire)
wire("mic_amp_wire",   (PANEL_W/2+0.04, -PANEL_D/2-0.02, Z0-0.01), (0.09, -PANEL_D/2-0.03, Z0-0.005), r=0.001, m=M_wire)

# Oscilloscope
osc_x, osc_y = 0.12, PANEL_D/2+0.08
box("osc_box", 0.10, 0.08, 0.06, (osc_x, osc_y, Z0+0.005+0.03), M_oscil)
box("osc_screen", 0.06, 0.002, 0.04, (osc_x, osc_y+0.041, Z0+0.005+0.03),
    mat("osc_scr2",(0.0,0.4,0.2),rough=0.1,emis=(0,0.4,0.2),es=1.5))
wire("amp_osc", (0.09, -PANEL_D/2-0.05, Z0-0.005), (osc_x-0.04, osc_y-0.04, Z0+0.005+0.03), r=0.0015, m=M_wire)

# Signal generator (drives speaker)
sig_x, sig_y = -0.15, -PANEL_D/2-0.06
box("sig_gen", 0.08, 0.05, 0.04, (sig_x, sig_y, Z0+0.005+0.02), M_oscil)
wire("sig_speaker", (sig_x+0.02, sig_y, Z0+0.005+0.02), (spk_x, -0.04, ZP-0.02), r=0.0015, m=M_wire)
wire("sig_speaker2",(sig_x+0.03, sig_y, Z0+0.005+0.02), (spk_x,  0.04, ZP-0.02), r=0.0015, m=M_wire)

# ==== Render camera ====
cam_pos = (-0.25, -0.25, 0.25)
cam_tgt = (0.0, 0.0, ZP)
d = mathutils.Vector(cam_tgt)-mathutils.Vector(cam_pos)
q = (-d).to_track_quat('Z','Y')
bpy.ops.object.camera_add(location=cam_pos, rotation=q.to_euler())
c = bpy.context.object
c.data.lens = 50; c.data.clip_start = 0.01; c.data.clip_end = 50
sc.camera = c

# Lights
for pos, e in [((0.3,0.1,0.35), 90), ((-0.25,0.25,0.30), 60), ((0.0,-0.30,0.20), 50)]:
    bpy.ops.object.light_add(location=pos, type='POINT')
    bpy.context.object.data.energy = e

# Save & render
out_blend = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scene_v01.blend")
out_png   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "overview_v01.png")
sc.render.filepath = out_png
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=out_blend)

with open(out_png,'rb') as f: h = hashlib.sha256(f.read()).hexdigest()
print(f"V28_BUILD_OK blend={out_blend} png={out_png} sha256={h}")
