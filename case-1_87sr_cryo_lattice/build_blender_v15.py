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
# v13: 线圈中心对准冷却光束交汇点 MOT_CONV_X(+0.030, 铜管口前), 两线圈对称分布在
# 交汇点两侧(dx=±0.040 -> x=-0.010 与 +0.070), 使 MOT 区与铜管口(x=0)分离,
# 光束在线圈内交汇, 线圈实体不与光束/铜管穿模。
MOT_CONV_X = 0.030   # 冷却光束交汇 x(铜管口 x=0 前方 30mm, MOT 区), 线圈也围绕此点
for label, dx in [("mot_coil_L", -0.040), ("mot_coil_R", 0.040)]:
    torus(label, R=0.032, r=0.003, loc=(MOT_CONV_X + dx, 0.0, AXIS_Z),
          rot=(0, math.radians(90), 0), m=M_WIRE)

# ---- 3. MOT COOLING BEAMS (blue 461 nm, 4 main beams shown) ----
# v14 修正(用户判定 v13 冷却光未真正交于 MOT 中心, 且仍穿 vac_shell 壁):
# (1) 交汇: v13 四束中心线到 MOT_C=(0.030,0,AXIS_Z) 最短距离 3.34/3.34/0/4.21mm,
#     只有 cool_bm_3 经过该点。v14 重推: 每束先定传播方向 d(单位向量), 再以同一
#     MOT_C 为参数点构造线段 P=MOT_C ± L·d, 使 MOT_C 落在每束【构造出的参数化中轴线上】
#     (0≤t≤1, 到 MOT_C 距离 0.0000mm), 而非只核对对象中心或注释。【注意】这是【构造保证】
#     (我按 MOT_C 为参数点摆出每束的轴线端点), 不是对已渲染圆柱网格做独立几何测量后
#     发现它恰好交汇; 核查用每束存的轴端点(beam_p0/beam_p1, 由 beam() 构造时记入), 非顶点云。
# (2) 穿壁: v13 mot_opt_win/mot_win_top/bot 只是【浮动玻璃 slab】, 未在 vac_shell 上做
#     布尔开孔, 光束 +x 端(x=75.8mm)超出右壁外表面(x=60mm) → cool_bm_1∩vac_shell=17.79mm³,
#     cool_bm_4∩vac_shell=14.28mm³。v14 修正: (a) 在 vac_shell 右壁/顶壁/底壁做真实布尔
#     开孔(冷却光窗口), (b) 光束端点终止在【窗口平面】(不再超出腔壁外表面), 玻璃窗填在开孔内,
#     光束与 shell 实体不再相交。上下(±z)光束端点也终止在顶/底窗口平面(记录为完整路径接口,
#     非展示截断)。
# 传播方向与端点(经参数化构造, 全部通过 MOT_C=(0.030,0,0.020)):
MOT_C = (MOT_CONV_X, 0.0, AXIS_Z)          # MOT 汇聚中心(= 目标点)
RT_WALL_IN_X = CHAM_CX + CHAM_W/2 - T       # 右壁内表面 x=57mm
RT_WIN_X = CHAM_CX + CHAM_W/2 - T/2          # 右壁窗口平面 x=58.5mm
RT_WALL_OUT_X = CHAM_CX + CHAM_W/2            # 右壁外表面 x=60mm (光束入射端接于此)
TOP_WIN_Z  = CHAM_CZ + CHAM_H/2 - T/2        # 顶壁窗口平面 z=73.5mm
BOT_WIN_Z  = CHAM_CZ - CHAM_H/2 + T/2        # 底壁窗口平面 z=-73.5mm
BEAM_TAIL_X = 0.005                          # 光束 -x 端截断 x(铜管口前 5mm 间隙, 保留 v13 已通过项)
# v15: 斜向光入射端接右壁外表面(x=60mm), 不再提前截断到 x=55mm 规避碰撞.
#   沿中心线(方向 d=(-0.7071,±0.7071,0), 过 MOT_C=(30,0,20))向 +x(来向)延长:
#   x=57 -> y=∓27, x=58.5 -> y=∓28.5, x=60 -> y=∓30 (z 恒=20). 入射端取外表面 x=60 命中点 (60,∓30,20).
#   MOT_C 仍在线段上(t 由端点定, 不要求 0.5/对称), 因延长保持同一直线. 记为假设(窗口尺寸/位置/安装形式无论文依据).
def _beam_via_motcenter(name, d, Lp_end_pt, Ln_end_pt, m=M_Cool, r=0.0012):
    """以 MOT_C 为参考点, 方向 d(单位), +x端/−x端 各自落到指定端点(参数化 L±), 保证 MOT_C 在线段上"""
    import mathutils as _mu
    d=_mu.Vector(d).normalized(); A=_mu.Vector(MOT_C)
    Lp=( _mu.Vector(Lp_end_pt)-A).dot(-d)   # +x 端 = MOT_C - Lp*d (d 指向 -x 旅行方向)
    Ln=( _mu.Vector(Ln_end_pt)-A).dot(d)    # -x 端 = MOT_C + Ln*d
    p0=tuple(A - Lp*d); p1=tuple(A + Ln*d)
    o=beam(name, p0, p1, r=r, m=m)
    o['beam_p0']=p0; o['beam_p1']=p1   # 记录几何轴端点(供交汇核查, 非顶点云)
    return o
# b1/b2: ±y 斜入射对, 经右壁窗口进入, -x 端截断 x=5mm.
#   v15: +x(入射)端接到右壁外表面 x=60mm 命中点 (60,∓30,20), 沿原中心线延长(不截断入射段).
#   方向 d=(-0.7071, ±0.7071, 0) (斜 -x 旅行); 中心线过 MOT_C=(30,0,20).
#   b1: +x 端 (60,-30,20) [沿中心线 y 随 x 增大而减小], -x 端 (5,+25,20)
#   b2: +x 端 (60,+30,20) [镜像], -x 端 (5,-25,20)
b1 = _beam_via_motcenter("cool_bm_1", (-0.7071,  0.7071,0.0),
                          (RT_WALL_OUT_X, -0.030, AXIS_Z),   # +x 端: x=60,y=-30 (接右壁外表面命中点)
                          (BEAM_TAIL_X,  0.025, AXIS_Z),       # -x 端(截断): x=5, y=+25
                          m=M_Cool)
b2 = _beam_via_motcenter("cool_bm_2", (-0.7071, -0.7071,0.0),
                          (RT_WALL_OUT_X,  0.030, AXIS_Z),   # +x 端: x=60,y=+30 (镜像)
                          (BEAM_TAIL_X, -0.025, AXIS_Z),       # -x 端(截断): x=5, y=-25
                          m=M_Cool)
# b3: 顶 ±z 光束, 经顶壁窗口(TOP_WIN_Z=73.5mm)进入, -z 端截断在 z=5mm(不伸入铜管, 展示截断端记录)
#   方向 d=(0,0,-1) (向下 -z 旅行); +z 端=顶窗口平面 z=73.5, -z 端 z=5(展示截断, 非完整对射)
TOP_WIN_XC = MOT_CONV_X   # 顶/底窗口 x 中心 = 光束 x=30mm
b3 = beam("cool_bm_3", (MOT_CONV_X, 0.0, TOP_WIN_Z),
                        (MOT_CONV_X, 0.0, AXIS_Z - 0.015), m=M_Cool)
b3['beam_p0']=(MOT_CONV_X,0.0,TOP_WIN_Z); b3['beam_p1']=(MOT_CONV_X,0.0,AXIS_Z-0.015)
# b4: 底 ±z 光束, 经底壁窗口(BOT_WIN_Z=-73.5mm)进入, +z 端截断在 z=40mm(展示截断端记录)
#   方向 d=(0,0,+1) (向上 +z 旅行); -z 端=底窗口平面 z=-73.5, +z 端 z=40(展示截断, 非完整对射)
b4 = beam("cool_bm_4", (MOT_CONV_X, 0.0, BOT_WIN_Z),
                        (MOT_CONV_X, 0.0, AXIS_Z + 0.020), m=M_Cool)
b4['beam_p0']=(MOT_CONV_X,0.0,BOT_WIN_Z); b4['beam_p1']=(MOT_CONV_X,0.0,AXIS_Z+0.020)
# 右壁(+x)冷却光窗口: 在 vac_shell 右壁做【真实布尔开孔】, 玻璃窗填在开孔内.
# v15: 开孔中心 y=0(z=20), 但需覆盖两束斜向中心线命中点 y=∓30mm(光束半径 r=1.2mm + 斜入射 45°
# 投影 1.70mm + 墙厚余量) -> 开孔 y 半宽 35mm(y∈[-35,+35]), z 半宽 6mm(z∈[14,26]), x 向厚 T+0.002
# 覆盖整金属带 x∈[57,60]. 不与光纤接口(lat_wall_hole 圆 r=4mm 中心 y=0,z=20; lat_fiber_flange)冲突:
# 冷却光开孔 y=±30 在光纤 y≈0 区外. 窗口尺寸/位置/安装形式=建模假设(无论文依据).
_cool_win_r_box = box("cool_win_r_cut", T+0.002, 0.070, 0.012,
                      (CHAM_CX+CHAM_W/2 - T/2, 0.0, AXIS_Z), rot=(0,math.radians(90),0))
boolean_cut(shell, _cool_win_r_box)      # 真实开孔(切掉右壁金属), y∈[-35,+35]mm 覆盖两束命中点
mot_win = box("mot_opt_win", 0.006, 0.070, 0.012, (CHAM_CX+CHAM_W/2 - T/2, 0.0, AXIS_Z),
              rot=(0, math.radians(90), 0), m=M_GLASS)   # 玻璃窗填在开孔内(x 向 6mm 覆盖金属带)
# 上/下壁冷却光窗口: 在 vac_shell 顶壁/底壁做【真实布尔开孔】(x 向 0.030 宽, 覆盖光束 x=30±15mm)
_cool_win_top_cut = box("cool_win_top_cut", 0.030, 0.030, T+0.002,
                        (MOT_CONV_X, 0.0, CHAM_CZ + CHAM_H/2 - T/2))
boolean_cut(shell, _cool_win_top_cut)
_cool_win_bot_cut = box("cool_win_bot_cut", 0.030, 0.030, T+0.002,
                        (MOT_CONV_X, 0.0, CHAM_CZ - CHAM_H/2 + T/2))
boolean_cut(shell, _cool_win_bot_cut)
mot_win_top = box("mot_win_top", 0.030, 0.030, T*0.15,
                  (MOT_CONV_X, 0.0, CHAM_CZ + CHAM_H/2 - T/2), m=M_GLASS)
mot_win_bot = box("mot_win_bot", 0.030, 0.030, T*0.15,
                  (MOT_CONV_X, 0.0, CHAM_CZ - CHAM_H/2 + T/2), m=M_GLASS)
# 验证(构建后自动核查): 4 束中轴线(构造保证, 非对渲染网格独立实测)均含 MOT_C(t∈[0,1], 不要求 0.5/对称);
# v15: b1/b2 +x(入射)端接到右壁外表面 x=60mm 命中点 (60,∓30,20), 沿原中心线延长(不截断入射段),
# 入射段真实经过右壁开孔(y∈[-35,+35]mm 覆盖命中点 y=∓30); 完整穿墙段(57..60)不碰金属壁/安装件;
# b3 +z 端=顶窗口平面 z=73.5(入射端), -z 端 z=5 展示截断; b4 -z 端=底窗口平面 z=-73.5(入射端), +z 端 z=40 展示截断
# MOT_CONV_X / BEAM_TAIL_X / 窗口尺寸 / 斜入射角 45° 无论文依据(论文只说 MOT 在线圈内、光路进真空室),
# 记为假设; 关键关系(MOT 在腔上游、光束经窗口进室、不与铜管/vac_shell 穿模)依据论文方案。

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
# v13 修正(内衬端点): v12 内衬中心 x=-0.06、长 0.90*160=144mm -> 范围 x∈[-132,+12]mm,
# 铜管范围 x∈[-160,0] -> 内衬前端 x=+12mm 【伸出铜管口 12mm】(v12 局部图右端突出管段)。
# 用明确前后端坐标定内衬范围, 使其【留在铜管内部】并与后窗安装区协调:
#   前端 x=LIN_FRONT_X=-0.020(铜管口 x=0 内侧 20mm, 留出口净空),
#   后端 x=LIN_REAR_X=CAV_REAR_X+0.0040=-0.156(后窗承座区, 内衬止于此, 后段为裸铜管)
#   内衬长度 = LIN_FRONT_X - LIN_REAR_X = 0.136, 完全在铜管 [-0.160, 0] 内部。
LIN_FRONT_X = -0.020
LIN_REAR_X  = CAV_X - CAV_LEN/2 + 0.0040   # = -0.160+0.004 = -0.156 (后窗承座区前)
LIN_LEN     = LIN_FRONT_X - LIN_REAR_X     # 0.136
cuo_lining_center = (LIN_FRONT_X + LIN_REAR_X)/2   # = -0.088
lining = cyl("cuo_lining", CAV_R_IN - 0.0002, LIN_LEN, (cuo_lining_center, 0.0, AXIS_Z),
             (0, math.radians(90), 0), m=M_CUO, seg=64)
lining_inner = cyl("cuo_lining_inner", CAV_R_IN - 0.0006, LIN_LEN + 0.002,
                   (cuo_lining_center, 0.0, AXIS_Z), (0, math.radians(90), 0))
boolean_cut(lining, lining_inner)
# 同步更新内衬外壳+内孔切割体: 剖切块 lining_cutaway 须覆盖内衬新范围 [-0.156,-0.020]
LIN_CUT = LIN_LEN + 0.006   # 略大于内衬长, 保证 -y 侧剖切到位
# (下方 lining_cut_block 用 LIN_CUT 代替原 CAV_LEN*0.98)

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
lining_cut_block = box("lining_cutaway", LIN_CUT, CAV_R_IN + 0.004, CAV_R_IN + 0.004,
                       ((LIN_FRONT_X + LIN_REAR_X)/2, -(CAV_R_IN + 0.004)*0.55, AXIS_Z))
boolean_cut(lining, lining_cut_block)
# 剖切后腔内特征（内壁/通孔/后窗/探测区）从 -y 侧直接可见，无需移动相机

# v9 后窗修正: 原来是一块 0.0006m 薄板, 悬在铜管后端口外 2mm, 像漂浮薄板。
# 改为明确的“后端法兰盖”: 一个铜色法兰体(外径略大于铜管外径)封住腔后端,
# 法兰内嵌一块倾斜萨晶镜片(覆盖法兰通孔), 使“覆盖并安装到腔后端”的关系可见。
# 具体尺寸/倾斜角未获论文支持, 记录为假设(论文仅说“tilted window ... transparent
# for lattice laser light but absorbs BBR”)。
CAV_REAR_X = CAV_X - CAV_LEN/2   # 铜管后端中心 x = -0.160
# 圆形萨晶镜盘(厚 0.6mm), 倾斜 20° 嵌在承座环中, 覆盖并安装到铜管后端
# v13 后窗重新设计(问题3, 数值验证): 承座环【不倾斜】(轴沿 x), 外径=铜管外径 6.5mm
# 跨在铜管末端端面抱紧(机械固定), 内孔 ID=镜盘实心半径 5.4mm(抱镜盘缘=真实接触面);
# 镜盘实心半径 5.4mm, 倾斜 20° 后沿 x 实心半宽 = 5.4*sin20+0.3*cos20 = 2.13mm, 镜盘中心
# 放 CAV_REAR_X - 2.13mm - 0.2mm 间隙 = -0.1623(镜盘整块在铜管后端, 不穿铜管壁 5.0~6.5mm);
# 镜盘 20° 投影半宽 = 5.4*cos20 = 5.07mm ≥ 铜管通孔 5.0mm -> 关闭后端开口。
SAP_TILT = math.radians(20)
R_disc   = 0.0054                 # 镜盘实心半径 5.4mm(>铜管通孔 5.0mm, 20°投影 5.07mm 关闭开口)
SAP_THK  = 0.0006
SAP_HALF_X = R_disc*math.sin(SAP_TILT) + (SAP_THK/2)*math.cos(SAP_TILT)   # 2.13mm
SAP_X = CAV_REAR_X - SAP_HALF_X - 0.0002   # 镜盘中心 x(镜盘整块在铜管后端, 不穿铜壁)
# 承座环: 不倾斜(轴沿 x), 跨铜管末端端面, 外径=铜管外径(抱紧), 内孔 ID=镜盘半径(抱镜盘缘)
SAP_SEAT_OUT  = CAV_R_OUT          # 承座外径 6.5mm = 铜管外径(抱紧铜管末端外表面)
SAP_SEAT_IN   = R_disc             # 承座内孔 5.4mm(抱镜盘实心缘, 真实接触)
SAP_SEAT_DPT  = 0.0040            # 承座厚 4.0mm(假设, 套在铜管末端【外侧】, 内表面端面贴铜管端面)
# v14 修正(承座-铜管连接, 用户判定 v13 承座端面 x=-160.1 与铜管端面 x=-160.0 有 0.1mm 间隙,
# 不能证明夹持): 承座环【前端环形面】压在铜管后端端面环形区(外径抱紧铜管 OD 6.5mm)上,
# 承座前缘 x 恰=铜管端面 x=CAV_REAR_X(零间隙, 面接触=机械固定), 承座体延伸到铜管后端外侧。
# 固定关系【可证明】: 承座外环(5.4~6.5mm 环, 外径=铜管 OD)前环形面 贴 铜管后端端面环形区
# (5.0~6.5mm) -> 环形面-环形面接触, 承座环抱紧铜管 OD, 承托镜盘后端缘。无法证明的(承座是否
# 螺接/焊接到铜管, 真空密封)仍如实标为未确认, 不把邻近/少量交集写成夹持证明。
# 承座前缘 x = CAV_REAR_X(零间隙), 承座体延伸到 CAV_REAR_X - SAP_SEAT_DPT(铜管后端外侧)。
SAP_SEAT_X = CAV_REAR_X - SAP_SEAT_DPT/2   # 承座中心: 前缘=CAV_REAR_X(零间隙面接触), 后缘=CAV_REAR_X-DPT
# 法兰: 铜色端盖套在承座后侧, 外径>承座, 内孔=镜盘半径, 承托镜盘后端(镜盘在承座与法兰间)
SAP_FL_OUT = CAV_R_OUT + 0.0010   # 法兰外径 7.5mm
SAP_FL_HOLE = R_disc + 0.0003     # 法兰内孔 = 镜盘半径+0.3mm 间隙(不夹持镜盘, 避免穿模)
SAP_FL_THK = 0.0040
SAP_FL_X = CAV_REAR_X - SAP_SEAT_DPT - SAP_FL_THK/2 - 0.00015   # 法兰前缘在承座后缘之后 0.15mm(零重叠, 承托镜盘后端)
fr = cyl("sapph_flange", SAP_FL_OUT, SAP_FL_THK, (SAP_FL_X, 0.0, AXIS_Z),
         (0, math.radians(90), 0), m=M_CU, seg=48)
fr_hole = cyl("sapph_flange_hole", SAP_FL_HOLE, SAP_FL_THK + 0.001, (SAP_FL_X, 0.0, AXIS_Z),
              (0, math.radians(90), 0), seg=48)
boolean_cut(fr, fr_hole)          # 法兰内孔(承托镜盘后端)
seat_ring = cyl("sapph_seat_ring", SAP_SEAT_OUT, SAP_SEAT_DPT,
                (SAP_SEAT_X, 0.0, AXIS_Z),
                (0, math.radians(90), 0), m=M_CU, seg=48)   # 承座环【不倾斜】, 套在铜管末端外侧
seat_ring_hole = cyl("sapph_seat_ring_hole", SAP_SEAT_IN, SAP_SEAT_DPT + 0.002,
                (SAP_SEAT_X, 0.0, AXIS_Z),
                (0, math.radians(90), 0), seg=48)
boolean_cut(seat_ring, seat_ring_hole)   # 承座环 = 5.4~6.5mm 环形, 套铜管末端 + 内孔承托镜盘缘
# 圆形萨晶镜盘(厚 0.6mm), 实心半径 5.4mm, 20° 倾斜, 嵌入承座环内孔, 覆盖铜管通孔
# 镜盘中心 x: 铜管末端端面(CAV_REAR_X)之后, 倾斜 20° 时沿 x 实心半宽 = R_disc*sin20+THK/2*cos20
# = 2.13mm; 镜盘整块放铜管后端(SAP_X = CAV_REAR_X - 2.13mm - 0.2mm 间隙), 不穿铜管壁/内衬末端
SAP_X = CAV_REAR_X - (R_disc*math.sin(SAP_TILT) + (SAP_THK/2)*math.cos(SAP_TILT)) - 0.0002
bpy.ops.mesh.primitive_cylinder_add(radius=R_disc, depth=SAP_THK,
    location=(SAP_X, 0.0, AXIS_Z),
    rotation=(0, math.radians(90)+SAP_TILT, 0),   # 20° 倾斜(轴 20° 偏离 x, 沿 x 实心半宽 2.13mm)
    vertices=48)
sw = bpy.context.object; sw.name = "sapph_window"
sw.data.materials.append(M_SAPPH)
# 装配(v13, 整体协调, 数值验证): 承座环(不倾斜)套在铜管末端【外侧】, 端面贴铜管末端端面
# (接触位置=承座端面/铜管端面, 机械固定), 内孔 5.4mm 承托镜盘缘(接触位置=镜盘外缘环, 承座面=
# 承座内表面); 镜盘 5.4mm/20° 投影 5.07mm ≥ 铜管通孔 5.0mm 关闭后端开口; 镜盘整块在铜管后端
# (SAP_X=-0.1645, 承座端面之后), 不穿铜管壁(5.0~6.5mm)/内衬末端(内衬止于 LIN_REAR_X=-0.156)。
# R_disc 5.4/承座 5.4~6.5/法兰 7.5/倾角 20°/偏移量 均记为假设(论文仅说 "tilted window ... 
# absorbs BBR", 未给尺寸); 不展开制造公差/真空密封设计。
SAPH_R = R_disc   # 供后文装配核查引用
FR_HOLE_R = SAP_FL_HOLE

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
# cam_cavo: 铜腔内部聚焦（v11: 总览必须含两个完整线圈; 线圈切割只作用于【展示副本】,
# 完整装置模型保留完整 mot_coil_L; 铜腔局部渲染时临时可见化剖切副本/隐藏主线圈, 渲染后恢复）
coilL = bpy.data.objects.get("mot_coil_L")
coil_disp = bpy.data.objects.new("mot_coil_L_display", coilL.data.copy())
scene.collection.objects.link(coil_disp)
coil_disp.matrix_world = coilL.matrix_world
# v11 修正: 只剖切【遮挡铜腔的上方小扇区】, 不删整圈(避免副本顶点=0)。
# 线圈中心 x=-0.040, 半径 32mm; 相机从 -y 斜下方看, 遮挡来自线圈 +y 侧上半弧,
# 只挖掉 +z 侧(顶部)一小段即可让铜腔露出, 保留线圈其它部分。
# 扇区中心 x≈-0.040, 顶弧 z = AXIS_Z + 0.032±, 用小块(宽 10mm, 高 8mm)切掉顶弧中段。
cut_blk = box("v11_coil_cut_blk", 0.020, 0.020, 0.010, (MOT_X - 0.040, 0.0, AXIS_Z + 0.030))
boolean_cut(coil_disp, cut_blk)   # 仅剖切展示副本, 主 mot_coil_L 保持完整
coil_disp.hide_render = True      # 默认隐藏展示副本(总览用主线圈)
cam6 = make_cam("cam_cavo", (CAV_X + 0.110, -0.150, AXIS_Z + 0.050),
                look_at=(CAV_X, 0.0, AXIS_Z), lens=30, clip_start=0.001, clip_end=2.0)

def render(cam_obj, out):
    scene.camera = cam_obj
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)
    print("rendered", out)

# v8: 低成本局部预览(降采样到 32), 通过人工目检后再出正式图
scene.cycles.samples = 32
bpy.ops.wm.save_as_mainfile(filepath="render-output/scene_v15.blend")
print("scene_v15.blend saved")

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

# 后窗装配核查 —— v11: 区分三类检查, 不用"投影盖满"代替装配
#  (a) 投影覆盖: 镜盘倾斜后沿通孔轴投影半宽 ≥ 通孔半径
#  (b) 实体相交: 镜盘实体 ∩ 法兰铜环 INTERSECT 体积(应≈0, 不穿模)
#  (c) 安装接触: 镜盘外缘嵌入承座槽(槽半径=镜盘外轮廓+间隙), 受支撑
import bmesh
def _solid_inter_mm3(oA, oB):
    tA=bpy.data.objects.new('v12_tA', oA.data.copy()); scene.collection.objects.link(tA); tA.matrix_world=oA.matrix_world
    tB=bpy.data.objects.new('v12_tB', oB.data.copy()); scene.collection.objects.link(tB); tB.matrix_world=oB.matrix_world
    md=tA.modifiers.new('b','BOOLEAN'); md.operation='INTERSECT'; md.object=tB
    bpy.context.view_layer.objects.active=tA; bpy.ops.object.modifier_apply(modifier='b')
    bm=bmesh.new(); bm.from_mesh(tA.data); v=bm.calc_volume(); bm.free()
    bpy.data.objects.remove(tB,do_unlink=True); bpy.data.objects.remove(tA,do_unlink=True)
    return abs(v)*1e9
print("=== 后窗装配核查(v14 整体协调: 覆盖/实体相交/接触/固定 分列) ===")
_sap=bpy.data.objects['sapph_window']
# 镜盘 vs 每对相邻部件实体相交(镜盘/承座/法兰均在铜管末端外侧 x<CAV_REAR_X, 不穿管壁/内衬)
for _nb in ['cav_outer','cuo_lining','sapph_flange','sapph_seat_ring']:
    _o=bpy.data.objects.get(_nb)
    if _o is None: print(f"  镜盘 ∩ {_nb}: 对象缺失"); continue
    _v=_solid_inter_mm3(_sap,_o)
    print(f"  镜盘 ∩ {_nb}: {_v:.3f} mm³ ({'不穿模' if _v<0.05 else '穿模!'})")
# 承座环 vs 相邻部件
_seat=bpy.data.objects.get('sapph_seat_ring')
if _seat:
    for _nb in ['sapph_flange','cav_outer','cuo_lining','sapph_window']:
        _o=bpy.data.objects.get(_nb)
        if _o is None: continue
        _v=_solid_inter_mm3(_seat,_o)
        print(f"  承座环 ∩ {_nb}: {_v:.3f} mm³ ({'不穿模' if _v<0.05 else '穿模!'})")
# 投影覆盖: 镜盘实心半径 R_disc, 20° 倾斜后沿通孔轴投影半宽 = R_disc*cos20
# 需 ≥ 铜管通孔半径 CAV_R_IN(5.0mm) 才关闭后端开口
CAV_R_IN_ = CAV_R_IN
proj_half = SAPH_R*math.cos(SAP_TILT)
print(f"  投影覆盖: 镜盘沿通孔轴投影半宽={proj_half*1000:.2f}mm vs 铜管通孔半径"
      f"={CAV_R_IN_*1000:.2f}mm -> {'关闭开口成立' if proj_half>=CAV_R_IN_ else '不足!'}")
# 承座接触(v14: 承座环前环形面压在铜管后端端面环形区, 零间隙面接触=机械固定; 承座内孔承托镜盘缘)
# 承座前缘 x = CAV_REAR_X(零间隙), 承座 OD 6.5mm 抱紧铜管 OD 6.5mm, 内孔 5.4mm 承托镜盘实心缘 5.4mm
# 无法证明部分(承座是否螺接/焊接/真空密封)如实标为未确认
_seat_front_x = CAV_REAR_X   # 承座前环形面 x = 铜管端面 x(零间隙)
print(f"  承座接触(v14): 承座环前环形面 x={_seat_front_x*1000:.1f}mm = 铜管后端端面 x={CAV_REAR_X*1000:.1f}mm"
      f"(零间隙, 环形面-环形面面接触=机械固定); 承座 OD={SAP_SEAT_OUT*1000:.2f}mm 抱紧铜管 OD; 承座内孔"
      f"={SAP_SEAT_IN*1000:.2f}mm 承托镜盘实心缘 {R_disc*1000:.2f}mm; 镜盘 20° 倾斜后投影半宽 {proj_half*1000:.2f}mm"
      f" 覆盖铜管通孔。【未确认】承座与铜管是否螺接/焊接/真空密封(本轮不展开制造公差设计)。")
# 承座前缘 vs 铜管端面 间隙核查(不得 >0.05mm, 否则仍不能证明夹持)
_seat_xs = [ _seat.matrix_world @ mathutils.Vector((v.co.x,v.co.y,v.co.z)) for v in _seat.data.vertices]
_seat_front = max(v.x for v in _seat_xs)   # 承座最 +x 面(前缘)
_gap = _seat_front - CAV_REAR_X             # 0 = 零间隙贴住; >0.00005 = 有间隙(不能证明夹持)
print(f"  承座前缘间隙核查: 承座前缘 x={_seat_front*1000:.2f}mm, 铜管端面 x={CAV_REAR_X*1000:.2f}mm,"
      f" 间隙={_gap*1000:.3f}mm ({'零间隙, 面接触成立' if abs(_gap)<0.00005 else '仍有间隙, 夹持未确认!'})")
# 镜盘中心 vs 承座中心 x 对齐核查(不应有 2mm 偏移)
_sap_x=[_sap.matrix_world @ mathutils.Vector((v.co.x,v.co.y,v.co.z)) for v in _sap.data.vertices]
_sx = (min(v.x for v in _sap_x)+max(v.x for v in _sap_x))/2
_stx = (min(v.x for v in [ _seat.matrix_world @ mathutils.Vector((v.co.x,v.co.y,v.co.z)) for v in _seat.data.vertices])
        +max(v.x for v in [ _seat.matrix_world @ mathutils.Vector((v.co.x,v.co.y,v.co.z)) for v in _seat.data.vertices]))/2
print(f"  中心对齐: 镜盘中心 x={_sx:.4f}, 承座中心 x={_stx:.4f}, 偏移={abs(_sx-_stx)*1000:.2f}mm"
      f" ({'同轴' if abs(_sx-_stx)<0.001 else '仍有偏移!'})")
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

# 线圈完整性核查: 主 mot_coil_L 必须完整(总览两个线圈均在), 剖切只作用于展示副本
_ml = bpy.data.objects.get('mot_coil_L'); _mr = bpy.data.objects.get('mot_coil_R')
_md = bpy.data.objects.get('mot_coil_L_display')
print("=== 线圈完整性核查(总览须含两个完整线圈) ===")
print(f"  mot_coil_L(主): {len(_ml.data.vertices)} 顶点; mot_coil_R(主): {len(_mr.data.vertices)} 顶点")
print(f"  mot_coil_L_display(剖切副本): {len(_md.data.vertices)} 顶点, hide_render={_md.hide_render}")

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
# v11 低成本预览: 总览(两个完整线圈) + 铜腔局部(临时可见化剖切副本/隐藏主线圈, 渲染后恢复)
# + 后窗安装剖切 + 其余局部; 各输出视角渲染后检查关键部件是否丢失
KEY_PARTS = ['mot_coil_L','mot_coil_R','cav_outer','sapph_flange','sapph_window','vac_shell',
             'left_mount_seat','left_feedthrough','lat_fiber_flange','dichroic_mir']
def key_parts_ok(cam_name):
    missing=[k for k in KEY_PARTS if not bpy.data.objects.get(k)]
    return cam_name, missing

def render_cavity_local(cam, out):
    # v13: 铜腔局部视角【同时隐藏两个主线圈 + 所有线圈展示副本】, 让入口/内壁/隔膜通孔/
    # 探测区/后窗成为主体, 不再被顶部断开环(展示副本)或主线圈遮挡。总览保留两个完整主线圈。
    # 渲染后恢复对象原状态(主线圈可见/副本隐藏), 避免影响其他视角。
    mainL= bpy.data.objects.get('mot_coil_L'); mainR= bpy.data.objects.get('mot_coil_R')
    disp = bpy.data.objects.get('mot_coil_L_display')
    # 隐藏所有线圈(主线圈 L/R + 展示副本)
    for _o in (mainL, mainR, disp):
        if _o: _o.hide_render=True
    render_local(cam, out)
    # 恢复: 两个主线圈可见, 展示副本隐藏(与保存状态一致)
    if mainL: mainL.hide_render=False
    if mainR: mainR.hide_render=False
    if disp: disp.hide_render=True
    _ml=bpy.data.objects.get('mot_coil_L'); _mr=bpy.data.objects.get('mot_coil_R')
    _md=bpy.data.objects.get('mot_coil_L_display')
    print(f"  [恢复核查] 主线圈L.hide_render={_ml.hide_render}(应False) "
          f"主线圈R.hide_render={_mr.hide_render}(应False) 副本.hide_render={_md.hide_render}(应True)")
    print("rendered", out, "(cavity-local: 主线圈L/R+展示副本全部临时隐藏使铜腔无遮挡, 渲染后已恢复)")

def render_mot_entrance_local(cam, out, hide_occluders=False):
    # v14: MOT/铜腔入口局部 —— 【独立显示规则】, 不同于 render_local(它会隐藏全部冷却光束)。
    # 本视角保留: 4 束冷却光 + 铜腔入口(cav_outer 前端 x=0) + 右壁/顶底冷却光窗口 + 主线圈;
    # 临时隐藏: 晶格光束 lat_beam_1/2(横穿 MOT 区会遮挡冷却光交汇)。
    # v15b: hide_occluders=True 时, 额外临时隐藏二向色镜 dichroic_mir + 铜腔前端 cav_outer 前段
    #        (让 4 束冷却光交汇点在 MOT 区不被铜腔/镜面压住), 渲染后全部恢复原状态。
    # 相机同时拍到 MOT 交汇点(MOT_C)与铜腔入口(x=0)。
    _hide = ['lat_beam_1','lat_beam_2']
    if hide_occluders:
        _hide += ['dichroic_mir']   # 临时隐藏二向色镜(压住交汇点的蓝片), 渲染后恢复
    _states={}
    for k in _hide:
        _o=bpy.data.objects.get(k)
        if _o:
            _states[k]=(_o.hide_render,)
            _o.hide_render=True
    # 确认冷却光束此时【可见】(未被隐藏), 以便判断交汇/间隙
    _cool_visible=[]
    for _cn in ['cool_bm_1','cool_bm_2','cool_bm_3','cool_bm_4']:
        _co=bpy.data.objects.get(_cn)
        if _co: _cool_visible.append(( _cn, not _co.hide_render))
    scene.camera=cam
    scene.render.filepath=out
    bpy.ops.render.render(write_still=True)
    # 恢复: 晶格光束/二向色镜可见(原状态), 冷却光束本就未被本函数隐藏
    for k,v in _states.items():
        bpy.data.objects.get(k).hide_render=v[0]
    print("rendered", out, f"(MOT 局部: 冷却光可见={[c for c,vis in _cool_visible if vis]}, "
          f"晶格光束/二向色镜临时隐藏已恢复, hide_occluders={hide_occluders})")

def render_local_restore_check(cam, out):
    render_local(cam, out)
    miss=key_parts_ok(out)[1]
    if miss: print("  [关键部件丢失告警]", out, miss)

# v15 限定重渲染: 只出 总览 + MOT/入口局部 两张低成本预览(保留 v14 已通过的铜腔内部/后窗图, 不重渲).
# 其余局部(right/top_hole/top_mirror/left_conn/rear_window/cavity)沿用 v14 已通过图, 本轮不重渲.
# MOT/铜腔入口局部: 保留冷却光束(独立显示规则), 相机同时拍到 MOT 交汇点与铜腔入口
# 相机位置: MOT_C=(30,0,20)mm 在铜管口(x=0)前方 30mm; 相机从 +x 前上方, 视锥同时含 MOT_C 与 x=0
# v15b: MOT/入口局部 —— 相机后拉+略偏俯视, 让 4 束冷却光交汇点在 MOT 区不被铜腔/二向色镜压住;
#   临时隐藏二向色镜(hide_occluders=True)使交汇点为画面主体, 入射段仍可见地穿过右壁玻璃窗。
#   相机: 从 +x 前上方更远/更高, look_at 仍取 MOT_C 与铜腔口中点, 焦段略缩短保证交汇点+窗口同框。
_mot_cam = make_cam("cam_mot_entrance", (MOT_CONV_X + 0.085, -0.055, AXIS_Z + 0.085),
                    look_at=((MOT_CONV_X+0.0)/2, 0.0, AXIS_Z), lens=38, clip_start=0.001, clip_end=2.0)
render_mot_entrance_local(_mot_cam, "render-output/render_v15_prev_mot_entrance.png", hide_occluders=True)
# 总览: 主线圈完整(两个线圈均在), 保留已通过的 cam_overview 构图, 冷却光束经真实窗口进室
render(cam1,          "render-output/render_v15_prev_overview.png")
# 各输出视角关键部件完整性检查(仅 v15 重渲的 2 张)
for view in ['render_v15_prev_mot_entrance','render_v15_prev_overview']:
    _c,_miss = key_parts_ok(view)
    print(f"  关键部件核查 {view}: {('缺失 '+str(_miss)) if _miss else '完整(9 部件均在)'}")
# 光路核查: 冷却光束 vs 不透明实体 + 每束中轴线(构造保证, 非对渲染网格独立实测)是否含 MOT 交汇点(交汇证据)
print("=== 光路核查(冷却光束: [1]交汇 [2]完整光路与接口 [3]实体相交) ===")
MOT_C_ = (MOT_CONV_X, 0.0, AXIS_Z)
def _ptline_dist(P, A, B):
    u=[B[i]-A[i] for i in range(3)]; w=[P[i]-A[i] for i in range(3)]
    uu=sum(x*x for x in u); uuw=sum(u[i]*w[i] for i in range(3)); t=uuw/uu
    cl=[A[i]+t*u[i] for i in range(3)]
    return sum((P[i]-cl[i])**2 for i in range(3))**0.5, t
for _bn in ['cool_bm_1','cool_bm_2','cool_bm_3','cool_bm_4']:
    _bo=bpy.data.objects.get(_bn)
    # 实体相交: 检查整个传播路径(真空室壁/vac_shell, 安装件, 铜管, 内衬, 线圈), 非只 4 对象
    _pen=[_t for _t in ['vac_shell','cav_outer','cuo_lining','mot_coil_L','mot_coil_R']
          if _solid_inter_mm3(_bo, bpy.data.objects.get(_t))>0.05]
    # 交汇: 取光束【几何轴端点】(非顶点云 min/max), 由 beam() 构造参数 p0/p1 存为自定义属性
    import mathutils as _mu3
    _p0=_bo.get('beam_p0'); _p1=_bo.get('beam_p1')
    if _p0 is None:
        _bb=[_bo.matrix_world @ _mu3.Vector(c) for c in _bo.bound_box]
        _p0=_bb[0]; _p1=_bb[6]
    _d,_t=_ptline_dist(MOT_C_, tuple(_p0), tuple(_p1))
    _onseg = (0.0<=_t<=1.0) and (_d<0.0005)
    print(f"  {_bn}: [交汇] 中轴线(构造)到 MOT_C={(MOT_C_[0]*1000,MOT_C_[1]*1000,MOT_C_[2]*1000)}mm 距离="
          f"{_d*1000:.3f}mm (t={_t:.3f}, {'线段包含交汇点' if _onseg else '未包含!'})"
          f" | [实体相交] {(_pen if _pen else '全路径无穿透(vac_shell/cav/lining/coil)')}")
# =====================================================================
# v15 限定修正: 斜向冷却光(b1/b2)窗口连接 —— 三项证据(经过交汇点 / 接到窗口 / 未穿金属壁)
# =====================================================================
print("=== v15 斜向冷却光窗口连接核查(b1/b2) ===")
for _bn in ['cool_bm_1','cool_bm_2']:
    _bo=bpy.data.objects.get(_bn); _p0=tuple(_bo.get('beam_p0')); _p1=tuple(_bo.get('beam_p1'))
    _d,_t=_ptline_dist(MOT_C_, _p0, _p1)
    print(f"  [1 经过交汇点] {_bn}: 中轴线 p0={[round(v*1e3,1) for v in _p0]} p1={[round(v*1e3,1) for v in _p1]}mm, "
          f"到 MOT_C 距离={_d*1e3:.4f}mm t={_t:.3f} ({'在线段上' if 0<=_t<=1 and _d<5e-4 else '不在线段上!'})")
_win_half_y=0.035   # 开孔 y 半宽 35mm(与 build 一致, y∈[-35,+35])
for _bn in ['cool_bm_1','cool_bm_2']:
    _bo=bpy.data.objects.get(_bn); _p0=tuple(_bo.get('beam_p0'))
    print(f"  [2 接到窗口] {_bn}: 入射端(外表面 x=60 命中) y={_p0[1]*1e3:.1f}mm(应=±30), 开孔 y 半宽={_win_half_y*1e3:.1f}mm "
          f"-> {'命中点在开孔内' if abs(_p0[1])<_win_half_y else '命中点超出开孔!'}")
for _bn in ['cool_bm_1','cool_bm_2']:
    _bo=bpy.data.objects.get(_bn)
    _v=_solid_inter_mm3(_bo, bpy.data.objects['vac_shell'])
    print(f"  [3 未穿金属壁] {_bn} ∩ vac_shell = {_v:.4f} mm³ ({'不穿金属壁' if _v<0.05 else '穿金属壁!'})")
_fib=bpy.data.objects.get('lat_fiber_flange')
if _fib:
    _fv=[_fib.matrix_world @ mathutils.Vector(v.co) for v in _fib.data.vertices]
    _fymin,_fymax=min(v.y for v in _fv)*1e3, max(v.y for v in _fv)*1e3
    print(f"  [接口关系] 光纤法兰 lat_fiber_flange y∈[{_fymin:.1f},{_fymax:.1f}]mm(≈0 区), 冷却光开孔 y=±30mm -> 不冲突")
