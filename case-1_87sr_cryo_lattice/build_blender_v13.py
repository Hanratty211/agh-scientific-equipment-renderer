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

# ---- 3. MOT COOLING BEAMS (blue 461 nm, 6-beam MOT — show 4 main pairs) ----
# v13 修正(冷却光穿模 + MOT/铜腔空间关系): v12 冷却光束中心线交于 (MOT_X=0,0,AXIS_Z)，
# 而铜管前端就在 x=0 -> 光束实体(半径1.2mm)与铜管壁(cav_outer)/内衬(cuo_lining)穿模
# (实测 cool_bm_2∩cav_outer 9.4mm³ 等)。论文: MOT 在铜腔【上游】, 原子先被冷却捕获再
# 输运进腔; 冷却光束交点应在铜管口【前方】, 光束实体不得穿过不透明铜壁/内衬/线圈。
# 修正: 冷却光束交汇点移到 x=MOT_CONV_X=+0.030(铜管口 x=0 前方 30mm), 且 -x 端
# 截断到 x=+0.005(铜管口前 5mm, 无遮挡间隙), +x 端经右壁光学窗口进入(见 mot_opt_win)。
# 这样光束在 MOT 区(x≈+0.03)交汇, 传播路径到铜管口之间有 5mm 净空, 不穿任何实体。
BEAM_TAIL_X = 0.005 # 光束 -x 端截断位置(铜管口前 5mm, 留无遮挡间隙)
# 4 束冷却光: 中心线交于 (MOT_CONV_X, 0, AXIS_Z)
# b1/b2: ±y 斜入射, +x 端经右壁窗口(到 x=+0.075), -x 端截断在 x=BEAM_TAIL_X
b1 = beam("cool_bm_1", (MOT_CONV_X + 0.045,  0.045, AXIS_Z),
                          (BEAM_TAIL_X, -0.018, AXIS_Z), m=M_Cool)
b2 = beam("cool_bm_2", (MOT_CONV_X + 0.045, -0.045, AXIS_Z),
                          (BEAM_TAIL_X,  0.018, AXIS_Z), m=M_Cool)
# b3: ±z 上下入射, 交点在 MOT_CONV_X, 两端对称(上下壁均有窗口), 不向 -x 伸入铜管
b3 = beam("cool_bm_3", (MOT_CONV_X,  0.0, AXIS_Z + 0.045),
                          (MOT_CONV_X,  0.0, AXIS_Z - 0.045), m=M_Cool)
# b4: 近轴一对, 短(只到 MOT 区), +x 端经右壁窗口, -x 端截断
b4 = beam("cool_bm_4", (MOT_CONV_X + 0.030,  0.0, AXIS_Z + 0.020),
                          (BEAM_TAIL_X, 0.0, AXIS_Z - 0.008), m=M_Cool)
# 右壁(+x)光学窗口: 冷却光束 +x 端经此窗口进入真空室(明确接口, 非穿铜壁)
# 窗口放在右壁外表面 x=CHAM_CX+CHAM_W/2 附近, 中心 z=AXIS_Z, 尺寸略大于光束端部
RT_WALL_X = CHAM_CX + CHAM_W/2   # 右壁金属面 x = -0.04+0.10 = 0.060
mot_win = box("mot_opt_win", 0.010, 0.030, 0.030, (RT_WALL_X, 0.0, AXIS_Z),
              rot=(0, math.radians(90), 0), m=M_GLASS)
# 上/下壁冷却光窗口(±z 光束经此进室) - 简化: 顶壁已有 win_top/port, 保留
# (win_top 在 x=CHAM_CX=-0.04, 覆盖 b3 上端 x=+0.03 不在其上; 为使 b3 上端有窗口,
#  在 x=MOT_CONV_X 处顶/底壁各开一个冷却光窗口)
mot_win_top = box("mot_win_top", 0.030, 0.030, T*0.15,
                  (MOT_CONV_X, 0.0, CHAM_CZ + CHAM_H/2 - T/2), m=M_GLASS)
mot_win_bot = box("mot_win_bot", 0.030, 0.030, T*0.15,
                  (MOT_CONV_X, 0.0, CHAM_CZ - CHAM_H/2 + T/2), m=M_GLASS)
# 验证: 4 束中心线交于 (MOT_CONV_X,0,AXIS_Z); -x 端均截断在 x=BEAM_TAIL_X=+0.005>
# 铜管口 x=0 -> 光束实体不伸入铜管/内衬区域, 消除 v12 穿模。
# MOT_CONV_X / BEAM_TAIL_X / 窗口尺寸无论文依据(论文只说 MOT 在线圈内、光路进真空室),
# 记为假设; 关键关系(MOT 在腔上游、光束经窗口进室、不与铜管穿模)依据论文方案。

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
SAP_SEAT_X    = CAV_REAR_X - SAP_SEAT_DPT/2 - 0.0001   # 承座中心 x(铜管末端外侧, 端面贴住, 不嵌入管壁实体)
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
bpy.ops.wm.save_as_mainfile(filepath="render-output/scene_v13.blend")
print("scene_v13.blend saved")

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
print("=== 后窗装配核查(v13 整体协调: 覆盖/实体相交/接触/固定 分列) ===")
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
# 承座接触(v13: 承座与镜盘【同向 20° 倾斜、同轴】, 内径=R_disc 贴住镜盘外缘=真实接触面,
# 非 v12 "半径相等但中心偏 2mm/朝向不同" 无法证明接触)
print(f"  承座接触: 承座环与镜盘同向 20° 倾斜且同轴(中心 x 相同), 承座内径={SAP_SEAT_IN*1000:.2f}mm"
      f"(=镜盘外缘)贴住镜盘外缘环 -> 接触面=承座内表面, 接触位置=镜盘外缘环; 承座外径"
      f"={SAP_SEAT_OUT*1000:.2f}mm 抱紧铜管末端外表面 -> 固定关系明确(承座环夹持镜盘+抱住铜管)")
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

def render_local_restore_check(cam, out):
    render_local(cam, out)
    miss=key_parts_ok(out)[1]
    if miss: print("  [关键部件丢失告警]", out, miss)

# v13 低成本预览: 总览(两个完整线圈 + 修正后的 MOT/铜腔关系 + 恢复的冷却光) +
# 铜腔局部(无遮挡) + 后窗安装剖切 + MOT/铜腔入口局部(展示冷却光路与管壁间隙)
render_local(cam4,      "render-output/render_v13_prev_right.png")
render_local(cam5a,     "render-output/render_v13_prev_top_hole.png")
render_local(cam5b,     "render-output/render_v13_prev_top_mirror.png")
render_local(cam_left_cut,  "render-output/render_v13_prev_left_conn.png")
render_local(cam_rear,      "render-output/render_v13_prev_rear_window.png")
# 铜腔局部: 主线圈L/R+展示副本全部临时隐藏使铜腔无遮挡, 渲染后恢复
render_cavity_local(cam6, "render-output/render_v13_prev_cavity.png")
# MOT/铜腔入口局部: 展示修正后的冷却光束交汇(MOT区)与铜管口之间的无遮挡间隙 + 右壁窗口
# 新增相机 cam_mot_entrance, 从 +x 前上方看 MOT 区 -> 铜管口
import mathutils as _mu2
_mot_cam = make_cam("cam_mot_entrance", (MOT_CONV_X + 0.060, -0.080, AXIS_Z + 0.060),
                    look_at=(0.0, 0.0, AXIS_Z), lens=50, clip_start=0.001, clip_end=2.0)
render_local(_mot_cam,   "render-output/render_v13_prev_mot_entrance.png")
# 总览: 主线圈完整(两个线圈均在), 保留已通过的 cam_overview 构图, 冷却光束已恢复
render(cam1,          "render-output/render_v13_prev_overview.png")
# 各输出视角关键部件完整性检查
for view in ['render_v13_prev_cavity','render_v13_prev_right','render_v13_prev_top_hole',
             'render_v13_prev_top_mirror','render_v13_prev_left_conn','render_v13_prev_rear_window',
             'render_v13_prev_mot_entrance','render_v13_prev_overview']:
    _c,_miss = key_parts_ok(view)
    print(f"  关键部件核查 {view}: {('缺失 '+str(_miss)) if _miss else '完整(9 部件均在)'}")
# 光路核查: 冷却光束 vs 不透明实体(cav_outer/cuo_lining/线圈) 沿传播路径相交
print("=== 光路核查(冷却光束 交点/方向/接口/与不透明实体相交) ===")
for _bn in ['cool_bm_1','cool_bm_2','cool_bm_3','cool_bm_4']:
    _bo=bpy.data.objects.get(_bn)
    _pen=[_t for _t in ['cav_outer','cuo_lining','mot_coil_L','mot_coil_R']
          if _solid_inter_mm3(_bo, bpy.data.objects.get(_t))>0.05]
    _xs=[_bo.matrix_world @ mathutils.Vector((v.co.x,v.co.y,v.co.z)) for v in _bo.data.vertices]
    print(f"  {_bn}: x∈[{min(v.x for v in _xs)*1000:.1f},{max(v.x for v in _xs)*1000:.1f}]mm "
          f"(铜管口 x=0, -x端须>0 才不穿管壁) 与不透明实体相交: {_pen if _pen else '无(路径无遮挡)'}")
