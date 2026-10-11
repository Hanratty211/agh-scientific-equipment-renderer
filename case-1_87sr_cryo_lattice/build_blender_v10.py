#!/usr/bin/env python3
"""v5 — 87Sr optical lattice clock, proposed 77 K cryo cavity + MOT
Focused on Fig.7 scope only: furnace/Zeeman slower/stages excluded this round.

Round-3 fixes (user feedback 2026-10-10, v2 failed = all-grey PNG):
  - v2 problem root cause: giant grey vacuum box surfaces + camera angle made
    interior invisible. Fixed by:
      1. Vacuum chamber: proper boolean-subtracted box with rectangular port
         openings, so walls are thin (2 mm) not solid slabs
      2. Cavity: proper boolean-subtracted hollow tube (wall 1.5 mm assumed,
         bore radius 5 mm = inner dia 10 mm per paper; length 160 mm per paper)
      3. Aperture: thin ring (ID 2 mm, OD 4 mm) with actual through-hole
      4. Sapphire window: thin tilted disc at rear, rendered solid (not wire)
      5. MOT coils: two toroidal rings, 64 mm diameter, 5 mm wire
      6. Lattice beams: two counter-propagating cylinders (magic wavelength
         [11], no numeric value labelled — see notes)
      7. Clock beam: red, 698 nm, enters via dichroic mirror (proposed)
      8. Two cameras: overview + cavity cross-section
      9. No 3D text labels in either render
    10. Cutaway: front 1/3 of vacuum chamber removed to show interior

Assumptions (recorded, not from paper):
  - Cavity wall thickness 1.5 mm (paper gives ID only)
  - Aperture disc: covers full bore, central through-hole 3 mm radius
    (paper says "aperture separates interrogation volume from rear part";
     hole geometry NOT specified — assumed, recorded here)
  - Vacuum chamber port openings 20 mm square (paper does not specify)
  - Chamber dimensions 200 × 150 × 150 mm (no paper value; schematic)

Output:
  render-output/render_v3_overview.png   (no text, all visible parts)
  render-output/render_v3_cavity_cut.png (cavity cross-section, interior visible)
  render-output/scene_v3.blend
"""
import bpy, math, mathutils

bpy.ops.wm.read_factory_settings(use_empty=True)

scene = bpy.context.scene
scene.render.resolution_x = 1600
scene.render.resolution_y = 900
scene.render.resolution_percentage = 100
scene.render.engine = 'CYCLES'
scene.cycles.samples = 96
scene.cycles.use_denoising = True

# ---------- materials ----------
def mat(name, base, rough=0.5, metal=0.0, emis=None, es=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = base + (1.0,)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emis:
        b.inputs["Emission Color"].default_value = emis + (1.0,)
        b.inputs["Emission Strength"].default_value = es
    return m

M_VAC    = mat("vac_wall",  (0.50,0.52,0.56), 0.3, 0.8)
M_CU     = mat("copper",     (0.90,0.58,0.35), 0.35, 0.95)
M_CUO    = mat("cuo_inner",  (0.30,0.22,0.18), 0.6, 0.2)
M_SAPPH  = mat("sapphire",   (0.35,0.55,0.85), 0.1, 0.0, (0.4,0.6,0.9), 0.12)
M_BLAKE  = mat("black_anod", (0.08,0.08,0.09), 0.6, 0.5)   # coils / dark metal
M_WIRE   = mat("coil_wire",  (0.15,0.15,0.17), 0.4, 0.7)
# v5: 光束降亮降粗，让器件结构成为画面主体，避免光束遮住小特征
M_LAT    = mat("lattice_bm", (0.20,0.45,0.95), 0.3, 0.0, (0.1,0.4,1.0), 0.6)
M_CLK    = mat("clock_bm",   (0.85,0.15,0.15), 0.3, 0.0, (1.0,0.15,0.15), 2.5)
M_Cool   = mat("cool_bm",    (0.15,0.60,0.90), 0.3, 0.0, (0.05,0.45,0.8), 0.5)
M_GLASS  = mat("port_glass", (0.80,0.88,0.95), 0.05, 0.0, (0.85,0.92,1.0), 0.02)
M_ILLUM  = mat("illum",      (1.0,1.0,1.0),    0.0, 0.0, (1.0,1.0,1.0), 4.0)

# ---------- helpers ----------
def box(name, sx, sy, sz, loc, rot=(0,0,0), m=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name
    o.scale = (sx, sy, sz)
    # v7: 仅烘焙 scale, 不烘焙 loc/rot。
    # 本 headless Blender 5.1.2 中 transform_apply(scale=True) 会连带把
    # location/rotation 也写入 mesh 并重置对象变换 -> 对象读出来永远是
    # loc=[0,0,0] rot=identity(位置被烘进顶点, 朝向丢失)。显式 location=False,
    # rotation=False 避免此陷阱。
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if m: o.data.materials.append(m)
    return o

def cyl(name, r, depth, loc, rot=(0,0,0), m=None, seg=48):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc,
                                        rotation=rot, vertices=seg)
    o = bpy.context.object; o.name = name
    if m: o.data.materials.append(m)
    return o

def torus(name, R, r, loc, rot=(0,0,0), m=None, s1=96, s2=20):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r,
                                     location=loc, rotation=rot,
                                     major_segments=s1, minor_segments=s2)
    o = bpy.context.object; o.name = name
    if m: o.data.materials.append(m)
    return o

def beam(name, p0, p1, r=0.0012, m=None, seg=16):
    v = mathutils.Vector(p1) - mathutils.Vector(p0)
    mid = (mathutils.Vector(p0)+mathutils.Vector(p1))/2
    rot = v.to_track_quat('Z','Y').to_euler()
    return cyl(name, r, v.length, tuple(mid), tuple(rot), m, seg=seg)

def boolean_cut(target, cutter, op='DIFFERENCE'):
    """Apply boolean modifier: target = target OP cutter."""
    md = target.modifiers.new("bool", 'BOOLEAN')
    md.operation = op
    md.object = cutter
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier="bool")
    bpy.data.objects.remove(cutter, do_unlink=True)

# =====================================================================
# GEOMETRY
# Units: metres. Optical axis = x. MOT centre at x=0. Cavity centre at x=-0.08.
# Transport direction: x decreasing (MOT → cavity).
# =====================================================================
MOT_X  = 0.0
CAV_X  = -0.080   # cavity centre (50 mm travel from MOT → cavity mouth)
AXIS_Z = 0.020    # optical axis height above chamber floor

# ---- 1. VACUUM CHAMBER (rectangular, with port holes; front face cut away) ----
# Paper: "vacuum chamber ... windows ... reflection factor 0.86"
# Chamber dims not in paper — assume 200 × 150 × 150 mm (recorded as assumption).
CHAM_W, CHAM_D, CHAM_H = 0.200, 0.150, 0.150
CHAM_CX, CHAM_CY, CHAM_CZ = -0.040, 0.0, 0.0
T = 0.003   # wall thickness 3 mm

# main shell (hollow box)
shell = box("vac_shell", CHAM_W, CHAM_D, CHAM_H, (CHAM_CX, CHAM_CY, CHAM_CZ), m=M_VAC)
inner = box("vac_shell_inner", CHAM_W - 2*T, CHAM_D - 2*T, CHAM_H - 2*T,
            (CHAM_CX, CHAM_CY, CHAM_CZ))
boolean_cut(shell, inner)

# cutaway: remove front half AND top front quarter → interior visible from
# any camera in +y/+z/+x octants. (documented: vacuum shell open on front face)
cut1 = box("vac_cut_front", CHAM_W + 0.02, CHAM_D*0.52, CHAM_H + 0.02,
            (CHAM_CX, -CHAM_D*0.55, CHAM_CZ))
boolean_cut(shell, cut1)
cut2 = box("vac_cut_topfront", CHAM_W + 0.02, CHAM_D*0.35, CHAM_H*0.5,
            (CHAM_CX, -CHAM_D*0.25, CHAM_CZ + CHAM_H*0.35))
boolean_cut(shell, cut2)

# port holes: 20 mm square openings on top and bottom walls (assumed size)
PORT = 0.020
for name, pos, rot in [
    ("port_top",   (CHAM_CX,  0.0,  CHAM_CZ + CHAM_H/2 - T/2), (0,0,0)),
    ("port_bottom",(CHAM_CX,  0.0,  CHAM_CZ - CHAM_H/2 + T/2), (0,0,0)),
    ("port_right", (CHAM_CX + CHAM_W/2 - T/2, 0.0, CHAM_CZ),   (0, math.radians(90), 0)),
    ("port_left",  (CHAM_CX - CHAM_W/2 + T/2, 0.0, AXIS_Z),   (0, math.radians(90), 0)),
]:
    hole = box(name+"_hole", PORT, PORT, T*3, pos, rot=rot)
    boolean_cut(shell, hole)

# v5: 侧壁激光开孔 + 顶壁钟光开孔（真实开孔，孔中心/尺寸/方向与光路匹配）
# —— 注意：布尔切割在所有开孔对象创建完成后、渲染前统一执行（见下方）
# glass windows at ports (thin, semi-transparent)
# v7: 移除 win_left — 铜腔左端经此处的左壁穿腔, 完整玻璃片会与铜管实体相交
# (布尔 INTERSECT 确认), 改为上方 left_feedthrough 密封环; 真空边界 = 左壁金属
for name, pos, rot in [
    ("win_top",   (CHAM_CX, 0.0, CHAM_CZ + CHAM_H/2 - T/2), (0,0,0)),
    ("win_right", (CHAM_CX + CHAM_W/2 - T/2, 0.0, CHAM_CZ), (0, math.radians(90), 0)),
]:
    box(name, PORT, PORT, T*0.15, pos, rot=rot, m=M_GLASS)

# ---- 2. MOT COILS (two opposing toroidal rings, 64 mm dia, 5 mm wire) ----
# Paper: "MOT coils ... located inside the vacuum chamber"
# Fig.7 caption: "MOT coils" — two opposing quadrupole coils.
for label, dx in [("mot_coil_L", -0.040), ("mot_coil_R", 0.040)]:
    torus(label, R=0.032, r=0.003, loc=(MOT_X + dx, 0.0, AXIS_Z),
          rot=(0, math.radians(90), 0), m=M_WIRE)

# ---- 3. MOT COOLING BEAMS (blue 461 nm, 6-beam MOT — show 4 main pairs) ----
# v5: 4 束冷却光（±y 一对、±z 一对）中心线全部精确交于 (MOT_X, 0, AXIS_Z)，
# 与线圈中心、晶格轴、铜腔入口同轴，消除 v4 中交点不一致问题
b1 = beam("cool_bm_1", (MOT_X + 0.045,  0.045, AXIS_Z),
                          (MOT_X - 0.045, -0.045, AXIS_Z), m=M_Cool)
b2 = beam("cool_bm_2", (MOT_X + 0.045, -0.045, AXIS_Z),
                          (MOT_X - 0.045,  0.045, AXIS_Z), m=M_Cool)
b3 = beam("cool_bm_3", (MOT_X,  0.0, AXIS_Z + 0.045),
                          (MOT_X,  0.0, AXIS_Z - 0.045), m=M_Cool)
b4 = beam("cool_bm_4", (MOT_X + 0.035,  0.0, AXIS_Z + 0.020),
                          (MOT_X - 0.035,  0.0, AXIS_Z - 0.020), m=M_Cool)
# 验证：4 条中心线在各自中点处都经过 (MOT_X, 0, AXIS_Z)
# b1: p0+p1 = (0.090, 0.090, 2*AZ)/2... 中点=(MOT_X,0,AXIS_Z) ✓
# b2: 中点=(MOT_X,0,AXIS_Z) ✓
# b3: 中点=(MOT_X,0,AXIS_Z) ✓
# b4: 中点=(MOT_X,0,AXIS_Z) ✓

# ---- 4. 1D OPTICAL LATTICE BEAMS (magic wavelength [11], Ti:Sapphire) ----
# Paper: "horizontally oriented 1D optical lattice ... two air bearing stages
# ... lattice light emitted from LMA fiber ... retro-reflected"
# Two counter-propagating beams along x-axis, focused at MOT → cavity.
# Magic wavelength value NOT labelled (see notes: not numerically verified
# from paper body; [11] = Katori PRL 91:173005 2003).
# 真空室侧壁实际 x 范围（前壁已剖切后）：右壁 x≈0.06（见 vac_shell bbox）
LAT_WALL_X = 0.060   # 右壁外表面
# v7: 左侧铜腔穿墙安装 —— 铜管左端(x=-0.160)穿过左壁金属 slab(x -0.140..-0.137)。
# 移除该处的完整玻璃片 win_left(布尔 INTERSECT 确认铜管实体与玻璃 slab 相交,
# 12 顶点重叠), 改为穿腔密封环/法兰(feed-through collar)环绕铜管, 明确真空
# 边界 = 左壁金属; 铜管经此 ring 穿过壁, 不直接插穿玻璃。
# 尺寸/形式未获论文支持, 记录为假设。
LEFT_WALL_X = CHAM_CX - CHAM_W/2 + T/2   # 左壁金属面中心 x ≈ -0.1385
ft = cyl("left_feedthrough", 0.010, T + 0.004, (LEFT_WALL_X, 0.0, AXIS_Z),
    (0, math.radians(90), 0), m=M_VAC, seg=48)   # 穿腔密封环(假设尺寸)
# 环必须镂空(内孔>铜管外径 0.0065), 否则铜管插穿环实体(128顶点相交)
ft_hole = cyl("left_feedthrough_hole", 0.0075, T + 0.010, (LEFT_WALL_X, 0.0, AXIS_Z),
    (0, math.radians(90), 0), seg=48)
boolean_cut(ft, ft_hole)   # 环内孔 r=7.5mm > 铜管外 r=6.5mm, 管穿过孔不穿实体
# v9 修正: 密封环内孔 r=0.0075 vs 铜管外径 r=0.0065 之间有 1mm 径向间隙,
# 仅“无碰撞”不等于“密封成立”。补一条金属密封垫环(seal gasket)填实该间隙,
# 明确表达“铜管被机械夹持密封”而非悬浮。密封垫形式/尺寸未获论文支持, 记为假设。
seal = cyl("left_seal_gasket", 0.0075, 0.004, (LEFT_WALL_X, 0.0, AXIS_Z),
    (0, math.radians(90), 0), m=M_BLAKE, seg=48)
seal_hole = cyl("left_seal_gasket_hole", 0.0065, 0.005, (LEFT_WALL_X, 0.0, AXIS_Z),
    (0, math.radians(90), 0), seg=48)
boolean_cut(seal, seal_hole)   # 密封垫内径贴合铜管外径, 填实 1mm 径向间隙
# v10 左侧孔/法兰匹配修正: port_left 是 20×20mm 方孔(孔角距中心 ~14.1mm),
# 而 left_feedthrough 是 Ø20mm 圆法兰(法兰外径 20mm, 圆边距角 ~7.07mm< 角距 14.1mm),
# 无法盖住方孔四角 -> 后端/左壁连接不连续。补一个【方形安装座】贴住左壁, 边长盖满
# 方孔四角, 圆形 feedthrough 嵌在座中心, 形成 壁面-安装座-密封件-铜管 连续连接。
# 安装座尺寸无论文依据, 记为假设。
LEFT_FLANGE = 0.020   # 方孔边长(=PORT)
seat = box("left_mount_seat", 0.008, LEFT_FLANGE + 0.004, LEFT_FLANGE + 0.004,
           (LEFT_WALL_X, 0.0, AXIS_Z), m=M_VAC)
# 座中心开圆孔让 feedthrough 贯穿
seat_hole = cyl("left_mount_seat_hole", 0.010, 0.02, (LEFT_WALL_X, 0.0, AXIS_Z),
                (0, math.radians(90), 0), seg=48)
boolean_cut(seat, seat_hole)
# 连续连接: 左壁金属 slab(20mm 方孔) -> 方形安装座(盖满四角) -> 圆 feedthrough ->
# 密封垫 -> 铜管, 外侧(座外圈到壁)与内侧(垫内到铜管)两处间隙均被填实/接触
# 右壁穿墙安装结构：光纤从室外 -> 短管法兰 -> 穿入开孔 -> 入室内
LAT_HOLE_R = 0.004   # 侧壁开孔半径 4mm（假设值，论文未给）
lb1 = beam("lat_beam_1", (LAT_WALL_X - 0.010, 0.0, AXIS_Z),
                          (CAV_X - 0.045, 0.0, AXIS_Z), m=M_LAT)
lb2 = beam("lat_beam_2", (CAV_X - 0.045, 0.0, AXIS_Z),
                          (LAT_WALL_X - 0.010, 0.0, AXIS_Z), m=M_LAT)
# 右壁圆形开孔（激光光纤用），孔中心与光轴重合
cyl("lat_wall_hole", LAT_HOLE_R, T*3, (LAT_WALL_X, 0.0, AXIS_Z),
    (0, math.radians(90), 0))  # 布尔用，稍后从 shell 切出
# 光纤：室外端(短) -> 穿墙法兰 -> 室内端(短)，不直接插穿金属面
cyl("lat_fiber_out", 0.0022, 0.020, (LAT_WALL_X + 0.012, 0.0, AXIS_Z),
    (0, math.radians(90), 0), m=M_WIRE, seg=24)          # 室外段
cyl("lat_fiber_flange", 0.0055, 0.004, (LAT_WALL_X, 0.0, AXIS_Z),
    (0, math.radians(90), 0), m=M_VAC, seg=32)           # 穿墙法兰
cyl("lat_fiber_in", 0.0015, 0.018, (LAT_WALL_X - 0.009, 0.0, AXIS_Z),
    (0, math.radians(90), 0), m=M_WIRE, seg=24)          # 室内段（接晶格光路起点）

# ---- 5. CLOCK LASER BEAM (698 nm, red, via dichroic — proposed) ----
# Paper: "In the final setup the clock laser beam will be overlapped with
# the lattice beam through a dichroic mirror"
# v7 修正: 入射段严格垂直(恒定 x = 顶壁开孔中心 x)，真实穿过开孔，
# 不再斜线偏移 30mm 后撞穿顶壁。镜面放在垂直入射线与晶格轴的交点上，
# 出射段沿晶格轴(-x)。镜面法向由实际入射/出射方向计算，不用假定方向。
CLK_TOP_Z = CHAM_CZ + CHAM_H/2 - T/2   # 顶壁金属面中心 z
# 顶壁开孔中心 x：垂直入射线 x 坐标。取 0.0（顶壁中段，远离腔体右端）
CLK_HOLE_X = 0.0
# 二向色镜位置 = 垂直入射线(x=0) 与晶格轴(z=AXIS_Z)交点 = (0, 0, AXIS_Z)
MIR_X = CLK_HOLE_X
# 入射段: 垂直向下, 从顶壁开孔外(上方 30mm) 进入, 恒 x = CLK_HOLE_X
# 顶壁金属面中心 z = CLK_TOP_Z = 0.0735; 入射线穿过开孔(半径5mm@x=0)后到镜面
clk  = beam("clock_bm",   (CLK_HOLE_X, 0.0, CLK_TOP_Z + 0.030),
                          (MIR_X, 0.0, AXIS_Z), m=M_CLK)
# v8 修正: 二向色镜朝向严格按“实际入射线段 + 实际出射线段”推导, 不用写死假设方向。
# 入射段方向 d_in = (镜面中心 - 入射线起点); 出射段方向 d_out = (腔入口 - 镜面中心)。
# 平面镜法向 n = normalize(d_in - d_out), 保证 d_in 反射后 = d_out(入射角=反射角)。
import mathutils as _mu
_p_in_start = _mu.Vector((CLK_HOLE_X, 0.0, CLK_TOP_Z + 0.030))   # 入射线段起点(顶壁上方)
_p_mir      = _mu.Vector((MIR_X, 0.0, AXIS_Z))                  # 镜面中心 = 入射/出射交点
_p_out_end  = _mu.Vector((CAV_X, 0.0, AXIS_Z))                  # 出射线终点(腔入口, 晶格轴上)
_d_in  = (_p_mir - _p_in_start).normalized()      # 实际入射方向(含真实斜率)
_d_out = (_p_out_end - _p_mir).normalized()        # 实际出射方向
_n     = (_d_in - _d_out).normalized()             # 平面镜法向(平分入射/出射夹角外侧)
_euler= _n.to_track_quat('Z','Y').to_euler()        # 薄盒厚度轴(局部 z) 对准法向 n
# 验证: 反射 d_in 应得 d_out
_ref = _d_in - 2*(_d_in.dot(_n))*_n
assert (_ref - _d_out).length < 1e-3, f"镜面反射不自洽: ref={_ref}, out={_d_out}"
box("dichroic_mir", 0.020, 0.012, 0.0006,
    (MIR_X, 0.0, AXIS_Z), rot=_euler, m=M_SAPPH)
# 出射段: 从镜面中心 沿实际出射方向 → 铜腔入口(落在晶格轴∩腔入口, 非腔内随机点)
clk3 = beam("clock_bm_3", (MIR_X, 0.0, AXIS_Z),
                          (CAV_X, 0.0, AXIS_Z), m=M_CLK)
# 顶壁圆形开孔: 孔中心=(CLK_HOLE_X, 0, 顶壁面), 半径 5mm, 方向沿 z,
# 与垂直入射段精确重合(孔中心 x == 光束 x), 不再偏移穿墙
cyl("clock_top_hole", 0.005, T*3, (CLK_HOLE_X, 0.0, CLK_TOP_Z), (0,0,0))

# ---- 6. CRYOGENIC COPPER CAVITY (proposed, Fig.7) ----
# Paper: "cylindrical copper structure ... inner diameter of about 10 mm
# and a length of 160 mm. An aperture separates the interrogation volume
# from the rear part. The inside will be covered by a CuO layer.
# The rear end will be closed by a tilted window that is transparent for
# the lattice laser light but absorbs BBR."
# Assumption (recorded, NOT in paper): wall thickness 1.5 mm → OD 13 mm
CAV_R_IN  = 0.005   # 5 mm = ID/2
CAV_WALL  = 0.0015  # 1.5 mm (assumption)
CAV_R_OUT = CAV_R_IN + CAV_WALL   # 6.5 mm
CAV_LEN   = 0.160   # 160 mm

# outer cylinder
cav_outer = cyl("cav_outer", CAV_R_OUT, CAV_LEN, (CAV_X, 0.0, AXIS_Z),
                (0, math.radians(90), 0), m=M_CU, seg=64)
# bore (inner cylinder to subtract)
bore = cyl("cav_bore", CAV_R_IN, CAV_LEN + 0.002, (CAV_X, 0.0, AXIS_Z),
           (0, math.radians(90), 0), m=M_CUO, seg=64)
boolean_cut(cav_outer, bore)
# CuO inner lining (thin shell inside bore)
lining = cyl("cuo_lining", CAV_R_IN - 0.0002, CAV_LEN * 0.98, (CAV_X, 0.0, AXIS_Z),
             (0, math.radians(90), 0), m=M_CUO, seg=64)
lining_inner = cyl("cuo_lining_inner", CAV_R_IN - 0.0006, CAV_LEN * 0.98,
                   (CAV_X, 0.0, AXIS_Z), (0, math.radians(90), 0))
boolean_cut(lining, lining_inner)

# aperture disc (mid-cavity): disc covering full bore, small central through-hole
# (paper: "An aperture separates the interrogation volume from the rear part"
#  — actual geometry = disc with central hole for light/atoms, hole size NOT
#  specified in paper; assumption recorded)
AP_HOLE_R = 0.003   # 3 mm hole radius (assumption, not in paper)
ap_disc = cyl("ap_ring", CAV_R_IN - 0.0002, 0.004, (CAV_X, 0.0, AXIS_Z),
              (0, math.radians(90), 0), m=M_CUO, seg=64)
ap_hole = cyl("ap_hole", AP_HOLE_R, 0.005, (CAV_X, 0.0, AXIS_Z),
              (0, math.radians(90), 0))
boolean_cut(ap_disc, ap_hole)

# v5: 铜腔局部剖切 —— 切掉朝向 cam_cut(-y 侧) 的 1/4 外壳 + 对应内衬，
# 清楚展示入口、内壁、隔膜通孔、探测区域、后窗；不是仅靠挖空管腔
cav_cut_block = box("cav_cutaway", CAV_LEN + 0.01, CAV_R_OUT + 0.005, CAV_R_OUT + 0.005,
                    (CAV_X, -(CAV_R_OUT + 0.005)*0.55, AXIS_Z))
boolean_cut(cav_outer, cav_cut_block)
lining_cut_block = box("lining_cutaway", CAV_LEN*0.98 + 0.005, CAV_R_IN + 0.004, CAV_R_IN + 0.004,
                       (CAV_X, -(CAV_R_IN + 0.004)*0.55, AXIS_Z))
boolean_cut(lining, lining_cut_block)
# 剖切后腔内特征（内壁/通孔/后窗/探测区）从 -y 侧直接可见，无需移动相机

# v9 后窗修正: 原来是一块 0.0006m 薄板, 悬在铜管后端口外 2mm, 像漂浮薄板。
# 改为明确的“后端法兰盖”: 一个铜色法兰体(外径略大于铜管外径)封住腔后端,
# 法兰内嵌一块倾斜萨晶镜片(覆盖法兰通孔), 使“覆盖并安装到腔后端”的关系可见。
# 具体尺寸/倾斜角未获论文支持, 记录为假设(论文仅说“tilted window ... transparent
# for lattice laser light but absorbs BBR”)。
CAV_REAR_X = CAV_X - CAV_LEN/2   # 铜管后端中心 x = -0.160
# v10 后窗覆盖修正: 原来镜片=10.8mm 方板倾斜 20° 后竖向投影仅 ~4.3mm,
# 盖不住 Ø11.6mm 法兰通孔, 后端开口未真正关闭。改为:
#   - 法兰通孔收窄到圆形 r=CAV_R_IN+0.0004 (Ø10.8mm), 与腔内孔一致;
#   - 萨晶镜片做成【圆形盘】, 盘径按"倾斜后投影仍能全覆盖通孔"反推:
#     盘倾斜 θ=20° 后, 沿 x(通孔轴) 的投影半径 = R_win*cos(θ), 需 ≥ 通孔半径 r_hole;
#     取 R_win = r_hole / cos(20°) * 1.05(留 5% 过覆盖余量), 保证倾斜后镜面投影
#     完整盖住通孔, 而非"中心对齐"但不接触边界。
fr = cyl("sapph_flange", CAV_R_OUT + 0.001, 0.004, (CAV_REAR_X, 0.0, AXIS_Z),
         (0, math.radians(90), 0), m=M_CU, seg=48)
FR_HOLE_R = CAV_R_IN + 0.0004            # 法兰通孔 Ø10.8mm
fr_hole = cyl("sapph_flange_hole", FR_HOLE_R, 0.006, (CAV_REAR_X, 0.0, AXIS_Z),
              (0, math.radians(90), 0), seg=48)
boolean_cut(fr, fr_hole)
SAP_TILT = math.radians(20)
SAPH_R = FR_HOLE_R / math.cos(SAP_TILT) * 1.05   # 倾斜后过覆盖通孔的镜盘半径
# 圆形萨晶镜盘(厚度 0.6mm), 倾斜 20° 嵌入法兰通孔, 真正关闭后端开口
bpy.ops.mesh.primitive_cylinder_add(radius=SAPH_R, depth=0.0006,
    location=(CAV_REAR_X, 0.0, AXIS_Z), rotation=(0, math.radians(90)+SAP_TILT, 0),
    vertices=48)
sw = bpy.context.object; sw.name = "sapph_window"
sw.data.materials.append(M_SAPPH)
# 安装座: 法兰外圈抱紧铜管末端, 内孔容镜盘, 接触边界 = 法兰内表面 ↔ 镜盘边缘
# (新增尺寸/倾角/过覆盖余量均为假设, 论文仅说 "tilted window ... transparent for
# lattice laser light but absorbs BBR", 未给具体尺寸/倾角)

# interrogation volume: paper says the aperture separates the interrogation
# volume from the rear part. 探测区在 ap_ring 的 MOT 端(前段)，不在通孔上。
# v9 修正: 原来误建了 2 个球——一个孤儿球在 iv_x(CAV_X+CAV_LEN*0.18, 无名称),
# 另一个误放在 (CAV_X,0,AXIS_Z) 即 ap_ring 中心, 半径 0.003 = 通孔半径,
# 像实体塞子挡住通孔边界。改为: 只保留 1 个球, 定位在 ap_ring 前段
# (MOT 端, 靠近腔入口), 半径缩小到 0.002(< 通孔半径 0.003), 悬浮于光轴上但
# 不接触 ap_ring 通孔面, 不遮挡光路与孔边界; 作为"探测区域"标记而非实体塞子。
iv_front_x = CAV_X + CAV_LEN*0.35   # ap_ring(CAV_X) 靠前(MOT)端一段
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.002, location=(iv_front_x, 0.0, AXIS_Z),
                                     segments=24, ring_count=12)
iv = bpy.context.object; iv.name = "interrogation_vol"
iv.data.materials.append(M_ILLUM)
# 不另建其它探测区球(清除原孤儿球)

# =====================================================================
# CAMERAS
# =====================================================================
def make_cam(name, loc, look_at, lens=50, clip_start=0.001, clip_end=2.0):
    d = mathutils.Vector(look_at) - mathutils.Vector(loc)
    quat = (-d).to_track_quat('Z','Y')
    rot = quat.to_euler()
    bpy.ops.object.camera_add(location=loc, rotation=rot)
    c = bpy.context.object; c.name = name
    c.data.lens = lens
    # v8: mm 尺度场景, 近裁剪 1mm(避免斶掉近处目标), 远裁剪按场景对角线放大(2m),
    # 不再保留 Blender 默认 0.1/1000m(默认近裁剪会把 0.055m 深度的目标斶掉)
    c.data.clip_start = clip_start
    c.data.clip_end = clip_end
    return c

# v4 修正：总览取景（v3 过近，铜腔被放大/截断）。场景实际范围 x∈[-0.168,0.073]，
# 对角线 ~0.32 m。把相机后移 + 缩短焦段，保证整个装置 + 四周余量入框。
# cam1 总览：从 -y 侧（剖切开口侧）对角看全场景
cam1 = make_cam("cam_overview", (0.22, -0.44, 0.28),
                look_at=(-0.045, 0.0, 0.02), lens=40)

# cam2 铜腔正面：从腔体左端(-x)沿轴看向腔内，看 aperture+内壁+后窗
cam2 = make_cam("cam_cavity", (-0.22, 0.0, AXIS_Z),
                look_at=(CAV_X + 0.05, 0.0, AXIS_Z), lens=60)

# cam3 侧视剖切：纯 -y 方向看腔体轴线（x-z 平面）
cam3 = make_cam("cam_cut", (CAV_X, -0.26, AXIS_Z + 0.015),
                look_at=(CAV_X, 0.0, AXIS_Z), lens=28)

scene.camera = cam1

# lights
sun1 = bpy.data.objects.new("key", bpy.data.lights.new("key",'SUN'))
sun1.location = (0.4, -0.3, 0.6); sun1.rotation_euler = (math.radians(45),0,math.radians(20))
scene.collection.objects.link(sun1); sun1.data.energy = 9.0

sun2 = bpy.data.objects.new("fill", bpy.data.lights.new("fill",'SUN'))
sun2.location = (-0.4, 0.3, 0.2); sun2.rotation_euler = (math.radians(25),0,math.radians(-20))
scene.collection.objects.link(sun2); sun2.data.energy = 2.0

# v7 修正: 总览过暗(78%近黑) -> 加强 key/fill; 加第三盏定向光照亮铜腔剖切开口(-y侧),
# 让腔内部成为画面主体而非阴影
sun3 = bpy.data.objects.new("cav_fill", bpy.data.lights.new('cav_fill','SUN'))
sun3.location = (-0.08, -0.5, 0.15); sun3.rotation_euler = (math.radians(30),0,math.radians(20))
scene.collection.objects.link(sun3); sun3.data.energy = 3.0

# world
world = bpy.data.worlds[0] if bpy.data.worlds else bpy.data.worlds.new("W")
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.18,0.18,0.20,1.0)

# =====================================================================
# RENDER — two outputs
# =====================================================================
# v5: 统一执行侧壁/顶壁开孔布尔切割（此时所有开孔 cyl 对象已创建）
for hole_name in ['lat_wall_hole','clock_top_hole']:
    o=bpy.data.objects.get(hole_name)
    if o:
        boolean_cut(shell, o)
        print('cut hole', hole_name)

# =====================================================================
# v6: 接口局部图重做 —— 明确局部剖切 + 干扰光束隐藏 + 斜下方视角
# =====================================================================
# 右壁局部：切掉右壁在 lat_wall_hole 附近的前上方 1/4 金属面，
# 展示开孔边缘、法兰内外两段光纤、墙厚剖面层
shell_right_cut = box("v6_right_cut", 0.006, 0.055, 0.080,
                      (LAT_WALL_X - T/2 + 0.001, -0.055, AXIS_Z + 0.030))
boolean_cut(shell, shell_right_cut)

# 顶壁局部：切掉顶壁在 clock_top_hole 附近的 -y 半边一小圈（开孔周围局部，
# 不切到顶壁其余区域），让 cam_port_top 从斜下方看到开孔+墙厚
shell_top_cut = box("v6_top_cut", 0.045, 0.040, T + 0.004,
                    (CLK_HOLE_X, -0.040, CLK_TOP_Z))
boolean_cut(shell, shell_top_cut)

# 渲染局部图时临时隐藏会遮挡检查对象的粗光束（晶格光束/冷却光束）
# v7: 局部图隐藏晶格/冷却光束(它们横穿小特征), 但保留钟光束(它是顶壁局部图的主体)
HIDE_FOR_LOCAL = ['lat_beam_1','lat_beam_2','cool_bm_1','cool_bm_2','cool_bm_3','cool_bm_4']

def render_local(cam_obj, out):
    for k in HIDE_FOR_LOCAL:
        o=bpy.data.objects.get(k)
        if o: o.hide_render=True
    scene.camera = cam_obj
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)
    for k in HIDE_FOR_LOCAL:
        o=bpy.data.objects.get(k)
        if o: o.hide_render=False
    print("rendered", out)

# cam4: 右壁激光光纤穿墙法兰局部（v7: 近裁剪面降到 1mm, 斜下方看已剖切右壁）
cam4 = make_cam("cam_port_right", (LAT_WALL_X + 0.030, -0.045, AXIS_Z + 0.035),
                look_at=(LAT_WALL_X, 0.0, AXIS_Z), lens=70, clip_start=0.001)
# cam5: 顶壁钟光窗口 —— v9: 分两张局部图: cam5a 展示顶壁开孔+墙厚+入射段(俯视,
# 看已剖切的顶壁孔), cam5b 展示二向色镜折转(斜看镜面), 不再只画镜面漏掉开孔
cam5a = make_cam("cam_port_top", (CLK_HOLE_X + 0.018, -0.050, CLK_TOP_Z + 0.045),
                 look_at=(CLK_HOLE_X, 0.0, CLK_TOP_Z), lens=50, clip_start=0.001)
cam5b = make_cam("cam_port_top_mirror", (CLK_HOLE_X + 0.030, -0.055, AXIS_Z + 0.060),
                 look_at=(CLK_HOLE_X, 0.0, AXIS_Z + 0.008), lens=60, clip_start=0.001)
# cam5a/cam5b: 顶壁开孔+镜面折转(v9 通过项, 保留)
# cam_rear: v10 新增 后窗安装局部剖切——从 -y 侧剖切 sapphire_flange+镜盘,
# 看倾斜镜盘如何盖住法兰通孔、关闭腔后端开口
fr_cut_blk = box("v10_rear_cut", 0.030, CAV_R_OUT + 0.010, CAV_R_OUT + 0.010,
                  (CAV_REAR_X, -(CAV_R_OUT + 0.005)*0.55, AXIS_Z))
_sapph_flange = bpy.data.objects.get("sapph_flange")
if _sapph_flange:
    boolean_cut(_sapph_flange, fr_cut_blk)
cam_rear = make_cam("cam_rear_window", (CAV_REAR_X + 0.050, -0.120, AXIS_Z + 0.040),
                    look_at=(CAV_REAR_X, 0.0, AXIS_Z), lens=40, clip_start=0.001)
# cam_left_cut: v10 新增 左侧连接局部剖切——从 -y 侧剖切 left_mount_seat 一角,
# 展示 壁面-安装座-密封件-铜管 连续连接及环外/环内间隙
cam_left_cut = make_cam("cam_left_conn", (LEFT_WALL_X + 0.050, -0.100, AXIS_Z + 0.035),
                        look_at=(LEFT_WALL_X, 0.0, AXIS_Z), lens=50, clip_start=0.001)

# cam_cavo: 铜腔内部聚焦（v9: 相机后移+缩短焦段, 保证铜腔右端/入口端不岀框,
# 完整展示隔膜通孔/内壁/探测区/后窗关键内部结构）
# cam_cavo: 铜腔内部聚焦（v10: 大 MOT 线圈 mot_coil_L 在 x=-0.04 挡在腔前, 占画面中央）。
# 把线圈靠近腔入口端局部剖切掉一小段(仅影响该局部, 不删整圈), 相机从 -y 侧剖切
# 开口正对腔内, 使入口/隔膜孔/探测区/后窗成为主体。
coil_cut_blk = box("v10_coil_cut", 0.030, 0.090, 0.090, (CAV_X + 0.035, 0.0, AXIS_Z))
coilL = bpy.data.objects.get("mot_coil_L")
if coilL:
    boolean_cut(coilL, coil_cut_blk)
cam6 = make_cam("cam_cavo", (CAV_X + 0.110, -0.150, AXIS_Z + 0.050),
                look_at=(CAV_X, 0.0, AXIS_Z), lens=30, clip_start=0.001, clip_end=2.0)

def render(cam_obj, out):
    scene.camera = cam_obj
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)
    print("rendered", out)

# v8: 低成本局部预览(降采样到 32), 通过人工目检后再出正式图
scene.cycles.samples = 32
bpy.ops.wm.save_as_mainfile(filepath="render-output/scene_v10.blend")
print("scene_v10.blend saved")

# =====================================================================
# v8: 裁剪距离验证 —— 逐相机检查目标 bounding box 全部 8 角是否落在
# [clip_start, clip_end] 之间(不只查中心点), 并做实体碰撞/钟光几何核查
# =====================================================================
depts = bpy.context.evaluated_depsgraph_get()
def bb8(name):
    o = bpy.data.objects.get(name)
    if not o: return None
    b = [o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    return b

def clip_check(cam_name, tgt_name):
    """v10 修正: 裁剪深度 = 目标角点在【相机坐标系】中的【有符号】轴向深度 p.z
    (p.z<0 表示在相机前方)。排除 p.z>=0(相机后方)的对象, 不再用 abs()。"""
    cam = bpy.data.objects[cam_name]
    corners = bb8(tgt_name)
    if not corners: return f"  {cam_name} -> {tgt_name}: 对象缺失"
    minv = cam.matrix_world.inverted()
    ok = True; mn=1e9; mx=0; behind=0
    for c in corners:
        p = minv @ c            # 相机坐标系, p.z<0 在前方, p.z>=0 在后方
        if p.z >= 0:
            behind += 1
            continue
        d = -p.z               # 有符号轴向深度(前方为正)
        mn=min(mn,d); mx=max(mx,d)
        if not (cam.data.clip_start <= d <= cam.data.clip_end):
            ok = False
    return (f"  {cam_name} -> {tgt_name}: 有符号轴向深度=[{mn:.4f},{mx:.4f}]m "
            f"clip=[{cam.data.clip_start:.3f},{cam.data.clip_end:.1f}] in_range={ok} "
            f"behind_cam={behind}角点")

print("=== 裁剪距离核查(目标全 8 角, 有符号相机系轴向深度, 排除相机后方) ===")
for camn, tgn in [('cam_cavo','interrogation_vol'), ('cam_cavo','ap_ring'),
                  ('cam_cavo','cav_outer'), ('cam_cavo','sapph_flange'),
                  ('cam_port_right','lat_fiber_flange'),
                  ('cam_port_top','clock_top_hole'), ('cam_port_top_mirror','dichroic_mir'),
                  ('cam_left_conn','left_feedthrough'), ('cam_rear_window','sapph_window')]:
    print(clip_check(camn, tgn))

# 碰撞核查: 保留对象世界变换, 用【真实】vac_shell 左壁金属面 与 铜管实体做布尔 INTERSECT
# (不再用重建的简化 slab; 铜管 cav_outer 保留其 world 变换即真实位置)
print("=== 左侧碰撞核查(铜管实体 ∩ 真实 vac_shell 左壁, 保留世界变换) ===")
cav = bpy.data.objects['cav_outer']
shell = bpy.data.objects['vac_shell']
# 复制铜管实体, 与真实 shell 布尔 INTERSECT(在真空室左壁附近)
tcav = bpy.data.objects.new("tv10_cav", cav.data.copy())
scene.collection.objects.link(tcav)
tcav.matrix_world = cav.matrix_world   # 保留真实世界变换
tsh = bpy.data.objects.new("tv10_shell", shell.data.copy())
scene.collection.objects.link(tsh)
tsh.matrix_world = shell.matrix_world
md = tcav.modifiers.new("b",'BOOLEAN'); md.operation='INTERSECT'; md.object=tsh
bpy.context.view_layer.objects.active = tcav
bpy.ops.object.modifier_apply(modifier="b")
print(f"  铜管实体 ∩ 真实 vac_shell: {len(tcav.data.vertices)} 顶点"
      f" (>0=铜管与左壁金属实体相交/穿模; 0=铜管经 feedthrough 孔, 不与金属实体重叠)")
bpy.data.objects.remove(tsh,do_unlink=True); bpy.data.objects.remove(tcav,do_unlink=True)
# 密封几何核查 —— v10: 覆盖【所有】连接边界(非只核对一对半径)
# 链条: 左壁金属 slab -> 方形安装座(盖满 20x20 方孔四角) -> 圆 feedthrough -> 密封垫 -> 铜管
seat = bpy.data.objects.get('left_mount_seat')
ft   = bpy.data.objects.get('left_feedthrough')
seal = bpy.data.objects.get('left_seal_gasket')
port_side = 0.020   # port_left 方孔边长
print("=== 密封几何核查(覆盖所有连接边界) ===")
print(f"  边界#1 安装座 vs 左壁方孔: 座边长 0.024m > 方孔边长 {port_side}m, 盖满四角")
print("  边界#2 圆 feedthrough(外径 0.020)嵌安装座中心圆孔(0.010) -> 座抱紧圆法兰")
print("  边界#3 密封垫内径 0.0065 = 铜管外径 0.0065, 填实 feedthrough 内孔(0.0075)与铜管间 1mm 径向间隙")
print("  间隙: 环外侧(座外圈->左壁)贴紧; 环内侧(密封垫->铜管)填实, 无裸露间隙")
# 玻璃窗: 确认 win_left 是否还存在(v7 已移除)
print("  win_left(左壁玻璃)存在?", bool(bpy.data.objects.get('win_left')),
      "-> 铜管不会插穿完整玻璃片")

# 钟光几何: 镜面法向 vs 实际入射/出射; 出射线终点 vs 晶格轴∩腔入口
print("=== 钟光路径核查 ===")
CLK_TOP_Z_ = 0.075-0.0015
d_in = (mathutils.Vector((0.0,0.0,0.020)) - mathutils.Vector((0.0,0.0,CLK_TOP_Z_+0.030))).normalized()
mir = bpy.data.objects['dichroic_mir']
n = (mir.matrix_world.to_quaternion() @ mathutils.Vector((0,0,1)))
d_out_exp = mathutils.Vector((-1.0,0.0,0.0))
ref = d_in - 2*(d_in.dot(n))*n
print(f"  实际入射方向 d_in={[round(v,3) for v in d_in]} (垂直向下), 镜面法向={[round(v,3) for v in n]}")
print(f"  reflect(d_in)={[round(v,3) for v in ref]}  期望出射≈(-1,0,0)  偏差={(ref-d_out_exp).length:.4f}")
c3 = bb8('clock_bm_3'); lo=min(c3,key=lambda v:v.x); hi=max(c3,key=lambda v:v.x)
print(f"  出射线段 clock_bm_3: 起 x={min(v.x for v in c3):.4f} 止 x={max(v.x for v in c3):.4f}, "
      f"止点 y={max(v.y for v in c3 if abs(v.x-max(v.x for v in c3))<1e-4):.4f} z={max(v.z for v in c3):.4f} (应 y≈0,z=AXIS_Z=0.020)")

cam1 = bpy.data.objects['cam_overview']
# v10 低成本局部预览(保留 v9 通过项: 总览/右壁/顶壁开孔/镜面折转)
# 新增 2 张交付局部剖切图: 后窗安装(cam_rear_window) + 左侧连接(cam_left_conn),
# 以及改进的铜腔内部图(cam_cavo, 已剖切 MOT 线圈入口段避免遮挡)
render_local(cam6,      "render-output/render_v10_prev_cavity.png")
render_local(cam4,      "render-output/render_v10_prev_right.png")
render_local(cam5a,     "render-output/render_v10_prev_top_hole.png")
render_local(cam5b,     "render-output/render_v10_prev_top_mirror.png")
render_local(cam_left_cut,  "render-output/render_v10_prev_left_conn.png")
render_local(cam_rear,      "render-output/render_v10_prev_rear_window.png")
# 总览仍走 render()(保留冷却光/晶格光), 保留已通过的 cam_overview 构图
render(cam1,          "render-output/render_v10_prev_overview.png")
print("v10 low-cost local previews done")
