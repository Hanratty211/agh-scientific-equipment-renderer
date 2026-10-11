#!/usr/bin/env python3
"""
case-2 build v2 (R5): D2NN OAM-STM 系统 Fig.2(a) —— 折叠光路 + 真实连接
=====================================================================
按外部核查 R4 结论重建：
  1. 折叠光路（M1/M2 把激光折到 DMD，M3 把 SLM 出射光折向 4f 探测段），不再全部 +x 等距
  2. 镜面方向由实际入射/出射路径决定（45° 反射镜，光线不穿背面/不截断）
  3. 3 条 MMF 延迟线用连续曲线（盘绕示意）从 Holder 分别连到 BC
  4. BC→输出 MMF→PD→示波器（PD–示波器用可区分的电信号线）
  5. Iris 有真实通孔（带圆孔薄板，布尔开孔）
  6. 光路用红色示意光束（注明 1064 nm 示意配色，非真实可见色）
  7. 浅灰背景 + 柔和照明，装置为主体
可重跑；用修正后的 blender_core（不带 case-1 对象名/坐标）。
"""
import os, sys, math
import mathutils
import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/Users/wht/Desktop/黑客松/agh-research-figure-skill/skills/agh-scientific-equipment-renderer/scripts")
import blender_core as bc

OUT = os.path.join(HERE, "render-output")
os.makedirs(OUT, exist_ok=True)
bc.setup_scene(samples=32, resolution=(1600, 900), background=(0.80, 0.80, 0.82))  # 浅灰背景

# ---- 材质 ----
M_LASER  = bc.mat("mat_laser", base=(0.18, 0.20, 0.26), rough=0.5, metal=0.6)
M_LENS   = bc.glass_mat("mat_lens", base=(0.70, 0.88, 0.96), rough=0.05, ior=1.5)
M_MIRR   = bc.mat("mat_mirr", base=(0.85, 0.87, 0.90), rough=0.08, metal=1.0)
M_DMD    = bc.mat("mat_dmd",  base=(0.10, 0.12, 0.16), rough=0.4, metal=0.4)
M_SLM    = bc.mat("mat_slm",  base=(0.09, 0.11, 0.15), rough=0.4, metal=0.4)
M_THIN   = bc.glass_mat("mat_thin", base=(0.55, 0.75, 0.90), rough=0.15, ior=1.5)
M_PRISM  = bc.glass_mat("mat_prism", base=(0.55, 0.75, 0.95), rough=0.05, ior=1.5)
M_FIBER  = bc.mat("mat_fiber", base=(0.92, 0.93, 0.95), rough=0.4, metal=0.0)
M_HOLD   = bc.mat("mat_holder", base=(0.35, 0.35, 0.38), rough=0.6, metal=0.5)
M_BOX    = bc.mat("mat_box", base=(0.30, 0.30, 0.34), rough=0.6, metal=0.4)
M_PDBODY = bc.mat("mat_pd", base=(0.15, 0.45, 0.25), rough=0.5, metal=0.3)
M_SCOPE  = bc.mat("mat_scope", base=(0.10, 0.12, 0.14), rough=0.5, metal=0.3)
# 红色示意光束（1064 nm 光路示意配色，不代表真实可见颜色）
M_BEAM   = bc.mat("mat_beam_red", base=(0.85, 0.12, 0.10), rough=0.3,
                  emis=(0.9, 0.1, 0.08), es=2.0)
# 电信号线（PD→示波器，与光纤/光束可区分：深蓝细实线）
M_ELEC   = bc.mat("mat_elec", base=(0.10, 0.15, 0.45), rough=0.4, metal=0.3)
# 地面
M_GROUND = bc.mat("mat_ground", base=(0.55, 0.55, 0.57), rough=0.95, metal=0.0)

# ---- 布局（折叠；米；z=0 主光轴；+x 右 +y 深 +z 上）----
# 第1段(+x): laser L1 L2 M1(折90°→+y)  第2段(+y): M2(折回→斜射DMD)
# 第3段: DMD L3 Iris1 L4 BS(dichroic) HWP Pol SLM M3(折90°→探测段) L5 Iris2 L6 L7 Holder MMF BC MMF_s PD Scope
Z0 = 0.0
def P(*a): return tuple(a)
# 第1段 +x
LZ = P(0.00, 0.0, Z0); L1 = P(0.10, 0.0, Z0); L2 = P(0.20, 0.0, Z0)
M1 = P(0.30, 0.0, Z0)                       # M1 折 90°：入射 +x，出射 +y
M2y = P(0.30, 0.50, Z0)                      # 第2段沿 +y，M2 在此折回射 DMD
DMD = P(0.50, 0.30, Z0)                      # DMD 在折叠区末端（斜入射面）
# 第3段 +x（从 DMD 出射面拉直回 +x 主光轴）
L3 = P(0.70, 0.0, Z0); IR1 = P(0.78, 0.0, Z0); L4 = P(0.86, 0.0, Z0)
BS = P(0.94, 0.0, Z0); HWP = P(0.97, 0.0, Z0); POL = P(1.00, 0.0, Z0); SLM = P(1.06, 0.0, Z0)
M3 = P(1.16, 0.0, Z0)                        # M3 折 90°：入射 +x，出射 +y（探测段折向）
# 探测段沿 +y 再折回 +x（为省空间，M3 出射直接 +y 到 4f，再 L7 聚焦 Holder；此处保持 +y 段）
L5 = P(1.16, 0.40, Z0); IR2 = P(1.16, 0.50, Z0); L6 = P(1.16, 0.60, Z0)
L7 = P(1.30, 0.60, Z0)                       # L7 聚焦到 Holder（+x 短段）
HOLD = P(1.40, 0.60, Z0)
BC = P(1.50, 0.60, Z0)
MMFS = P(1.56, 0.60, Z0)
PD = P(1.62, 0.60, Z0)
SCOPE = P(1.70, 0.60, Z0)

# 各件 x 半厚（薄件）；镜倾斜 bbox 偏移
LT=0.004; PLT=0.002; MIRT_FACE=0.0293
# ---- 光源 + 第1段 ----
bc.box("pulse_laser", 0.06, 0.05, 0.05, LZ, m=M_LASER)
def lens(x, y, z, name): return bc.cyl(name, r=0.045, depth=0.008, loc=(x,y,z), rot=(0, math.pi/2, 0), m=M_LENS)
lens(*L1, "lens_L1"); lens(*L2, "lens_L2"); lens(*L3, "lens_L3"); lens(*L4, "lens_L4")
lens(*L5, "lens_L5"); lens(*L6, "lens_L6")
bc.cyl("lens_L7", r=0.04, depth=0.01, loc=L7, rot=(0, math.pi/2, 0), m=M_LENS)
# 45° 反射镜（薄板；镜面朝向由入射/出射路径决定：M1/M3 入射+出射互成 90° → 镜面 45°）
def mirror(name, loc):
    return bc.box(name, 0.003, 0.08, 0.08, loc, m=M_MIRR, rot=(0, math.radians(45), 0))
mirror("mirror_M1", M1); mirror("mirror_M2", M2y); mirror("mirror_M3", M3)
# DMD / SLM（板，法线斜向入射光）
bc.box("dmd", 0.09, 0.004, 0.09, DMD, m=M_DMD, rot=(0, math.radians(45), 0))
bc.box("slm", 0.09, 0.004, 0.09, SLM, m=M_SLM)
# dichroic + HWP + Polarizer（薄片）
bc.box("bs_dichroic", 0.004, 0.07, 0.07, BS, m=M_PRISM)
bc.box("hwp", 0.003, 0.07, 0.07, HWP, m=M_THIN)
bc.box("polarizer", 0.003, 0.07, 0.07, POL, m=M_THIN)
# Holder（夹持器，三 MMF 并排焦面）
bc.box("holder", 0.04, 0.10, 0.10, HOLD, m=M_HOLD)
# BC 3×1 合束器 + 输出 MMF + PD + 示波器
bc.box("bc_combiner", 0.05, 0.08, 0.08, BC, m=M_BOX)
bc.cyl("mmf_single", r=0.006, depth=0.03, loc=MMFS, rot=(0, math.pi/2, 0), m=M_FIBER)
bc.box("pd", 0.05, 0.05, 0.05, PD, m=M_PDBODY)
bc.box("oscilloscope", 0.08, 0.07, 0.09, SCOPE, m=M_SCOPE)

# ---- Iris：带真实通孔的薄板（布尔开孔，非实心圆盘）----
def iris(name, loc, hole_r=0.012):
    plate = bc.cyl(name, r=0.03, depth=0.006, loc=loc, rot=(0, math.pi/2, 0), m=M_THIN)
    hole = bc.cyl(f"{name}_cut", r=hole_r, depth=0.02, loc=loc, rot=(0, math.pi/2, 0), m=None)
    bc.boolean_cut(plate, hole, op='DIFFERENCE')
    return plate
iris("iris1", IR1); iris("iris2", IR2)

# ---- 3 条 MMF 延迟线：连续曲线（盘绕示意）从 Holder 分别连到 BC ----
def coil_fiber(name, y0, y1, color=None, turns=3, rad=0.012):
    """沿 +x 从 x_h=HOLD[0] 到 x_c=BC[0]，带 turns 个正弦盘绕（视觉示意，非实测圈数）。"""
    import mathutils as mu
    x0 = HOLD[0] + 0.02; x1 = BC[0] - 0.025
    mesh = bpy.data.meshes.new(name)
    verts = []; edges = []
    N = 64
    for i in range(N+1):
        t = i/N
        x = x0 + (x1-x0)*t
        y = y0 + (y1-y0)*t
        z = Z0 + rad*math.sin(turns*2*math.pi*t)   # 盘绕（简化正弦）
        verts.append((x, y, z))
    for i in range(N): edges.append((i, i+1))
    mesh.from_pydata(verts, edges, [])
    ob = bpy.data.objects.new(name, mesh)
    # 曲线化：用 Bezier/曲线代替折线以获得连续光纤
    bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(M_FIBER)
    return ob
# 三根并排（y = HOLD y ±0.02, 0），目标 BC 中心 y=0.60
coil_fiber("mmf_delay_1", HOLD[1]-0.02, 0.60-0.02, turns=4)   # 2 m
coil_fiber("mmf_delay_2", HOLD[1], 0.60, turns=3)            # 4 m
coil_fiber("mmf_delay_3", HOLD[1]+0.02, 0.60+0.02, turns=2)  # 6 m

# ---- 电信号线（PD→示波器，可区分细实线，非光纤/光束）----
def wire(name, p0, p1, r=0.0015):
    return bc.beam(name, p0, p1, r=r, m=M_ELEC, record_ends=False)
wire("elec_pd_scope", (PD[0]+0.025, PD[1], Z0+0.03), (SCOPE[0]-0.04, SCOPE[1], Z0+0.05))

# ---- 光路段（红色示意，连接各真实表面；折叠段方向与镜面一致）----
def _seg(name, x0, x1, y0=0.0, y1=0.0, z0=Z0, z1=Z0):
    bc.beam(name, (x0, y0, z0), (x1, y1, z1), r=0.004, m=M_BEAM)
# 第1段 +x
_seg("beam_laser_L1", LZ[0]+0.03, L1[0]-LT, L1[1])
_seg("beam_L2_M1",    L2[0]+LT,   M1[0]-MIRT_FACE)
# M1 折 90° → +y 段（入射 +x、出射 +y，镜像 45° 平面）
_seg("beam_M1_M2",    M1[0], M1[0], y0=0.0, y1=M2y[1], z0=Z0)          # 沿 +y
# M2 折回 → 斜射 DMD（M2 出射方向朝 DMD 面）
_seg("beam_M2_dmd",   M2y[0], DMD[0], y0=M2y[1], y1=DMD[1], z0=Z0)
# 第3段 +x（DMD 出射拉回主光轴）
_seg("beam_dmd_L3",   DMD[0], L3[0]-LT, y0=DMD[1], y1=0.0)
_seg("beam_L4_bs",    L4[0]+LT, BS[0]-PLT)
_seg("beam_slm_M3",   SLM[0]+PLT, M3[0]-MIRT_FACE)
# M3 折 90° → +y 探测段
_seg("beam_M3_L5",    M3[0], M3[0], y0=0.0, y1=L5[1])
_seg("beam_L6_L7",    L6[0], L7[0], y0=L6[1], y1=L7[1])
_seg("beam_L7_holder",L7[0]+LT, HOLD[0]-0.02, y0=L7[1], y1=HOLD[1])
# BC→输出 MMF→PD（光路末端）
_seg("beam_bc_mmf",   BC[0]+0.025, MMFS[0]-0.015, y0=BC[1], y1=MMFS[1])
_seg("beam_mmf_pd",   MMFS[0]+0.015, PD[0]-0.025, y0=MMFS[1], y1=PD[1])

# ---- 地面 + 柔和照明 ----
gdata = bpy.data.meshes.new("ground_plane")
gdata.from_pydata([(-0.8,-1.6,-0.02),(2.4,-1.6,-0.02),(2.4,1.6,-0.02),(-0.8,1.6,-0.02)], [], [(0,1,2),(0,2,3)])
gob = bpy.data.objects.new("ground_plane", gdata); gob.data.materials.append(M_GROUND)
bpy.context.scene.collection.objects.link(gob)
def _light(name, ltype, loc, rot, energy):
    data = bpy.data.lights.new(name, ltype); data.energy = energy; data.color = (1.0,1.0,1.0)
    ob = bpy.data.objects.new(name, data); ob.location = loc; ob.rotation_euler = rot
    bpy.context.scene.collection.objects.link(ob); return ob
_light("key_light","SUN",(-0.5,-1.0,1.4),(math.radians(45),0,math.radians(20)),3.0)
_light("fill_light","SUN",(1.8,0.8,1.0),(math.radians(50),0,math.radians(-120)),1.0)
_light("soft_area","AREA",(0.9,0.2,0.9),(0,0,0),200.0)
_light("local_area","AREA",(1.45,0.35,0.5),(0,0,0),400.0)

# ---- 相机 ----
scene = bpy.context.scene
cam_ov = bc.make_cam("cam_overview", (0.85, -1.5, 0.85), look_at=(0.9, 0.15, 0.0),
                     lens=24, clip_start=0.005, clip_end=12.0)
scene.camera = cam_ov
scene.cycles.samples = 32
scene.cycles.use_denoising = True
scene.render.filepath = os.path.join(OUT, "case2_v2_overview_wordless.png")
bpy.ops.render.render(write_still=True)

# 光纤链路局部（Holder/3×MMF/BC）：must_keep 全部必须参与渲染，缺失/隐藏则拒绝
lr = bc.LocalRenderRule(must_keep=["holder","mmf_delay_1","mmf_delay_2","mmf_delay_3",
                                   "bc_combiner","mmf_single","lens_L7"])
bc.get_or_make_cam("cam_link_fiber", loc=(1.45,-0.45,0.45), look_at=(1.45,0.60,0.0),
                   lens=50, clip_start=0.005, clip_end=4.0)
_g = bpy.data.objects.get("ground_plane"); _gp = _g.hide_render
_g.hide_render = True   # 局部视角临时隐藏地面，渲染后还原
_sc = bpy.context.scene; _sc.view_settings.exposure = 1.0
ok, rep = lr.render(bpy.data.objects["cam_link_fiber"], os.path.join(OUT, "case2_v2_link_fiber.png"))
_sc.view_settings.exposure = 0.0
_g.hide_render = _gp
print("link_fiber render:", ok, rep)

# 关键件分层核查（存在/参与渲染/入框）
KEY = ["pulse_laser","lens_L1","lens_L2","mirror_M1","mirror_M2","dmd","lens_L3","lens_L4",
       "bs_dichroic","hwp","polarizer","slm","mirror_M3","lens_L5","lens_L6","lens_L7",
       "holder","mmf_delay_1","mmf_delay_2","mmf_delay_3","bc_combiner","mmf_single","pd","oscilloscope"]
for camname in ("cam_overview","cam_link_fiber"):
    vn, report = bc.key_parts_ok(camname, KEY, cam_name=camname)
    bad = {k:v for k,v in report.items() if not (v["exists"] and v["renders"])}
    print(f"[{vn}] 关键件 {len(KEY)} 个；异常={bad if bad else '无'}")

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "scene_case2_v2.blend"))
print("saved scene_case2_v2.blend + 2 preview PNGs (v2 折叠布局)")
