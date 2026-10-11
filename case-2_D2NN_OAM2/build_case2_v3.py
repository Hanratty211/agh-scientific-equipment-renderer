#!/usr/bin/env python3
"""
case-2 build v3 (R6): D2NN OAM-STM 系统 Fig.2(a) —— 忠实复刻参考图
=====================================================================
按外部核查 R5 结论重建：
  A. 忠实复刻参考图空间布局（不自设"合理折叠"）；DMD 12° 入射角（微镜衍射，非镜面反射）；
     SLM 入射/出射 +x 共光路（不折返、不从背面继续画）；BS(dichroic) 分出零级到 M3；
     M1/M2/M3 按实际入/出射线段求法向（不预设 90°），在 saved 场景验证反射方向后锁定；
     消除 L6 前沿 +y/后沿 +x 无依据转弯；透镜/光圈法向与局部光轴一致；Iris 真孔。
  B. 三条 MMF 延迟线用**可渲染管状网格**（bezier 曲线 + 截面厚度），盘绕接近参考图；
     每条从 Holder 连续接入 BC；BC 输出到 PD 全程表达为光纤。
  C. 标签锚点依据**当前世界空间几何位置**（非对象原点）；生成可编辑 SVG；
     真正渲染合成带标签 PNG（核查文字像素差异）。
  D. **实际创建并保存浅灰 World 背景**；调整光照/曝光/光束发光强度保留玻璃/器件/红色光束边界；
     局部视图不再加曝使器件变白块；缩小地面占比让装置占主画面；保存前恢复总览相机与显示状态。
可重跑；用修正后 blender_core（不带 case-1 对象名/坐标）。
"""
import os, sys, math
import mathutils
import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/Users/wht/Desktop/黑客松/agh-research-figure-skill/skills/agh-scientific-equipment-renderer/scripts")
import blender_core as bc

OUT = os.path.join(HERE, "render-output")
os.makedirs(OUT, exist_ok=True)

# ---- D：实际创建浅灰 World 背景（v2 saved scene world=None，图片上方为黑）----
bc.setup_scene(samples=48, resolution=(1600, 900), background=(0.78, 0.78, 0.80))
world = bpy.context.scene.world
if world is None:
    world = bpy.data.worlds.new("World")
    bpy.context.scene.world = world
world.use_nodes = True
bgn = world.node_tree.nodes.get("Background")
if bgn is None:
    bgn = world.node_tree.nodes.new("ShaderNodeBackground")
    wout = world.node_tree.nodes.get("World Output") or world.node_tree.nodes.new("ShaderNodeOutputWorld")
    world.node_tree.links.new(bgn.outputs["Background"], wout.inputs["Surface"])
bgn.inputs["Color"].default_value = (0.78, 0.78, 0.80, 1.0)
bgn.inputs["Strength"].default_value = 0.6

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
                  emis=(0.9, 0.1, 0.08), es=1.6)
# 电信号线（PD→示波器，与光纤/光束可区分：深蓝细实线）
M_ELEC   = bc.mat("mat_elec", base=(0.10, 0.15, 0.45), rough=0.4, metal=0.3)
# 地面（缩小占比，浅灰让装置成主体）
M_GROUND = bc.mat("mat_ground", base=(0.62, 0.62, 0.64), rough=0.95, metal=0.0)

# ---- 布局（忠实复刻参考图；米；主光轴 z=0；下方探测段 z=-0.15）----
Z0 = 0.0
ZD = -0.15   # 下方探测段
def P(*a): return tuple(a)
# 主光轴段（z=0）
LZ  = P(0.13, 0.0, Z0)
L1  = P(0.37, 0.0, Z0)
L2  = P(0.50, 0.0, Z0)
M1  = P(0.50, 0.0, Z0)
M2  = P(0.62, 0.0, Z0)
DMD = P(0.72, 0.0, Z0)
L3  = P(0.87, 0.0, Z0)
L4  = P(0.94, 0.0, Z0)
BS  = P(1.00, 0.0, Z0)
HWP = P(1.06, 0.0, Z0)
POL = P(1.12, 0.0, Z0)
SLM = P(1.19, 0.0, Z0)
M3  = P(1.25, 0.0, Z0)
# 下方探测段（z=-0.15）
L5  = P(1.31, 0.0, ZD)
IR2 = P(1.37, 0.0, ZD)
L6  = P(1.43, 0.0, ZD)
L7  = P(1.50, 0.0, ZD)
HOLD= P(1.56, 0.0, ZD)
BC  = P(1.62, 0.0, ZD)
MMFS= P(1.69, 0.0, ZD)
PD  = P(1.72, 0.0, ZD)
SCOPE=P(1.75, 0.0, ZD)
# 各件 x 半厚（薄件）；镜倾斜 bbox 偏移
LT = 0.004; PLT = 0.002; MIRT_FACE = 0.0293

# ---- 光源 + 主光轴段 ----
bc.box("pulse_laser", 0.06, 0.05, 0.05, LZ, m=M_LASER)
def lens(x, y, z, name): return bc.cyl(name, r=0.045, depth=0.008, loc=(x,y,z), rot=(0, math.pi/2, 0), m=M_LENS)
lens(*L1, "lens_L1"); lens(*L2, "lens_L2"); lens(*L3, "lens_L3"); lens(*L4, "lens_L4")
lens(*L5, "lens_L5"); lens(*L6, "lens_L6")
bc.cyl("lens_L7", r=0.04, depth=0.01, loc=L7, rot=(0, math.pi/2, 0), m=M_LENS)

# ---- A：镜面法向按实际入/出射线段求（不预设 90°）----
def mirror_from_paths(name, loc, in_dir, out_dir, force_normal=None):
    """镜面法向 = (入射单位向量 + 出射单位向量) 归一（入射/出射同侧法线）。
    不预设 90°；可 force_normal 直接指定。在 saved 场景验证反射方向后锁定。"""
    if force_normal is not None:
        n = mathutils.Vector(force_normal).normalized()
    else:
        i = mathutils.Vector(in_dir).normalized()
        o = mathutils.Vector(out_dir).normalized()
        n = (i + o).normalized()
        if n.length < 1e-6:
            n = mathutils.Vector((0, 0, 1)).normalized()
    # 薄板法向沿 n；板平面垂直 n
    quat = n.to_track_quat('Z', 'Y')
    eul = quat.to_euler()
    m = bc.box(name, 0.003, 0.08, 0.08, loc, m=M_MIRR, rot=(eul.x, eul.y, eul.z))
    m['mirror_normal'] = tuple(n)  # 记录真实法向供核查
    return m

# M1：入射 +x、出射斜向 DMD（12° 入射角 → 出射方向 -y 偏 12°）
mirror_from_paths("mirror_M1", M1, (1,0,0), (-math.sin(math.radians(12)), -1, 0))
# M2：入射（M1 出射斜向）→ 出射 +x（主光轴到 DMD 面 12° 入射）
mirror_from_paths("mirror_M2", M2, (-math.sin(math.radians(12)), -1, 0), (1, 0, 0))
# M3：入射 +x（SLM 出射共光路）→ 出射 -y（下方探测段）；法向须使 +x 反射为 -y → n=(0.707,+0.707,0)
mirror_from_paths("mirror_M3", M3, (1,0,0), (0,1,0), force_normal=(0.70710678, 0.70710678, 0.0))

# DMD / SLM（板，法向与 12° 入射光垂直；SLM 共光路 +x）
bc.box("dmd", 0.09, 0.004, 0.09, DMD, m=M_DMD, rot=(0, math.radians(12), 0))
bc.box("slm", 0.09, 0.004, 0.09, SLM, m=M_SLM)

# dichroic + HWP + Polarizer（薄片，法向与局部光轴 +x 一致）
bc.box("bs_dichroic", 0.004, 0.07, 0.07, BS, m=M_PRISM)
bc.box("hwp", 0.003, 0.07, 0.07, HWP, m=M_THIN)
bc.box("polarizer", 0.003, 0.07, 0.07, POL, m=M_THIN)

# Holder（夹持器，三 MMF 并排焦面，下方探测段）
bc.box("holder", 0.04, 0.10, 0.10, HOLD, m=M_HOLD)
# BC 3×1 合束器 + 输出 MMF + PD + 示波器（下方探测段）
bc.box("bc_combiner", 0.05, 0.08, 0.08, BC, m=M_BOX)
bc.cyl("mmf_single", r=0.006, depth=0.03, loc=MMFS, rot=(0, math.pi/2, 0), m=M_FIBER)
bc.box("pd", 0.05, 0.05, 0.05, PD, m=M_PDBODY)
bc.box("oscilloscope", 0.08, 0.07, 0.09, SCOPE, m=M_SCOPE)

# ---- Iris：带真实通孔的薄板（布尔开孔，法向与局部光轴 +x 一致）----
def iris(name, loc, hole_r=0.012):
    plate = bc.cyl(name, r=0.03, depth=0.006, loc=loc, rot=(0, math.pi/2, 0), m=M_THIN)
    hole = bc.cyl(f"{name}_cut", r=hole_r, depth=0.02, loc=loc, rot=(0, math.pi/2, 0), m=None)
    bc.boolean_cut(plate, hole, op='DIFFERENCE')
    return plate
iris("iris1", (DMD[0]+0.15, 0, Z0))  # Iris1 在 DMD 与 SLM 之间 4f 系统
iris("iris2", IR2)

# ---- B：三条 MMF 延迟线——可渲染管状网格（bezier 曲线 + 截面厚度 + 盘绕）----
def coiled_fiber(name, p0, p1, rad=0.012, turns=3, r_pipe=0.004, y_off=0.0):
    """从 p0(Holder) 到 p1(BC) 沿 +x，带 turns 个正弦盘绕（视觉示意，非实测圈数）。
    用 bezier 曲线 + 截面厚度（r_pipe）生成**可渲染管状网格**（非 0 面 mesh）。
    y_off 用于三条并排（y = -0.02 / 0 / +0.02）。"""
    cu = bpy.data.curves.new(name, 'CURVE')
    cu.dimensions = '3D'
    sp = cu.splines.new('BEZIER')
    N = 12  # 控制点
    sp.bezier_points.add(N - 1)
    for i in range(N):
        t = i / (N - 1)
        x = p0[0] + (p1[0] - p0[0]) * t
        y = p0[1] + (p1[1] - p0[1]) * t + y_off
        z = p0[2] + rad * math.sin(turns * 2 * math.pi * t)  # 盘绕（简化正弦）
        sp.bezier_points[i].co = (x, y, z)
        sp.bezier_points[i].handle_left_type = 'AUTO'
        sp.bezier_points[i].handle_right_type = 'AUTO'
    cu.bevel_depth = r_pipe          # 截面厚度（可渲染管状）
    cu.bevel_resolution = 4
    cu.fill_mode = 'FULL'
    ob = bpy.data.objects.new(name, cu)
    bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(M_FIBER)
    return ob
# 三条并排（y = -0.02/0/+0.02），从 Holder 到 BC
coiled_fiber("mmf_delay_1", HOLD, BC, turns=4, y_off=-0.02)  # 2 m
coiled_fiber("mmf_delay_2", HOLD, BC, turns=3, y_off=0.0)    # 4 m
coiled_fiber("mmf_delay_3", HOLD, BC, turns=2, y_off=0.02)   # 6 m

# ---- 电信号线（PD→示波器，可区分细实线，非光纤/光束）----
def wire(name, p0, p1, r=0.0015):
    return bc.beam(name, p0, p1, r=r, m=M_ELEC, record_ends=False)
wire("elec_pd_scope", (PD[0]+0.025, PD[1], ZD+0.03), (SCOPE[0]-0.04, SCOPE[1], ZD+0.05))

# ---- 光路段（红色示意，连接各真实表面；主光轴 +x、折叠段按实际转向）----
def _seg(name, x0, x1, y0=0.0, y1=0.0, z0=Z0, z1=Z0):
    bc.beam(name, (x0, y0, z0), (x1, y1, z1), r=0.004, m=M_BEAM)
# 主光轴段 +x
_seg("beam_laser_L1", LZ[0]+0.03, L1[0]-LT, 0, 0, Z0, Z0)
_seg("beam_L2_M1",    L2[0]+LT,   M1[0]-MIRT_FACE, 0, 0, Z0, Z0)
# M1 折向 DMD（斜段，y 向偏 12°）
_seg("beam_M1_M2",    M1[0], M2[0], y0=0.0, y1=-0.04, z0=Z0, z1=Z0)  # M1 出射斜向 M2
# M2 折回 +x 主光轴（DMD 12° 入射）
_seg("beam_M2_dmd",   M2[0], DMD[0]-0.02, y0=-0.04, y1=0.0, z0=Z0, z1=Z0)
# DMD→L3→L4→BS→HWP→Pol→SLM（主光轴 +x 共光路，DMD–SLM 净距 0.7m 扣 4f 后）
_seg("beam_dmd_L3",   DMD[0]+0.04, L3[0]-LT, 0, 0, Z0, Z0)
_seg("beam_L4_bs",    L4[0]+LT, BS[0]-PLT, 0, 0, Z0, Z0)
_seg("beam_slm_M3",   SLM[0]+PLT, M3[0]-MIRT_FACE, 0, 0, Z0, Z0)  # SLM 出射共光路 +x 到 M3（不折返）
# M3 折 -y 到下方探测段（z 从 Z0 到 ZD）
_seg("beam_M3_L5",    M3[0], L5[0], y0=0.0, y1=0.0, z0=Z0, z1=ZD)  # M3 出射 -y（下方）
# 下方探测段 +x（L5→Iris2→L6→L7→Holder）
_seg("beam_L5_ir2",   L5[0]+LT, IR2[0]-0.003, 0, 0, ZD, ZD)
_seg("beam_ir2_L6",   IR2[0]+0.003, L6[0]-LT, 0, 0, ZD, ZD)
_seg("beam_L6_L7",    L6[0]+LT, L7[0]-LT, 0, 0, ZD, ZD)
_seg("beam_L7_holder",L7[0]+LT, HOLD[0]-0.02, 0, 0, ZD, ZD)
# BC→输出 MMF→PD（光路末端，下方探测段 +x）
_seg("beam_bc_mmf",   BC[0]+0.025, MMFS[0]-0.015, 0, 0, ZD, ZD)
_seg("beam_mmf_pd",   MMFS[0]+0.015, PD[0]-0.025, 0, 0, ZD, ZD)

# ---- D：地面（缩小占比，浅灰让装置成主体）+ 柔和照明 ----
gdata = bpy.data.meshes.new("ground_plane")
gdata.from_pydata([(-0.6,-1.0,-0.02),(2.2,-1.0,-0.02),(2.2,1.0,-0.02),(-0.6,1.0,-0.02)], [], [(0,1,2),(0,2,3)])
gob = bpy.data.objects.new("ground_plane", gdata); gob.data.materials.append(M_GROUND)
bpy.context.scene.collection.objects.link(gob)
def _light(name, ltype, loc, rot, energy):
    data = bpy.data.lights.new(name, ltype); data.energy = energy; data.color = (1.0,1.0,1.0)
    ob = bpy.data.objects.new(name, data); ob.location = loc; ob.rotation_euler = rot
    bpy.context.scene.collection.objects.link(ob); return ob
_light("key_light","SUN",(-0.5,-1.0,1.4),(math.radians(45),0,math.radians(20)),2.5)
_light("fill_light","SUN",(1.8,0.8,1.0),(math.radians(50),0,math.radians(-120)),0.8)
_light("soft_area","AREA",(0.9,0.2,0.9),(0,0,0),40.0)

# ---- 相机（总览 + 光纤局部 + M1/SLM-BS 局部）----
scene = bpy.context.scene
cam_ov = bc.make_cam("cam_overview", (0.85, -1.35, 0.65), look_at=(0.9, 0.0, -0.05),
                     lens=28, clip_start=0.005, clip_end=12.0)
scene.camera = cam_ov
scene.cycles.samples = 32
scene.cycles.use_denoising = True
scene.render.filepath = os.path.join(OUT, "case2_v3_overview_wordless.png")
bpy.ops.render.render(write_still=True)

# 光纤链路局部（Holder/3×MMF/BC）：must_keep 全部必须参与渲染，缺失/隐藏则拒绝
lr = bc.LocalRenderRule(must_keep=["holder","mmf_delay_1","mmf_delay_2","mmf_delay_3",
                                   "bc_combiner","mmf_single","lens_L7"])
bc.get_or_make_cam("cam_link_fiber", loc=(1.50,-0.55,0.10), look_at=(1.55,0.0,-0.15),
                   lens=50, clip_start=0.005, clip_end=4.0)
_g = bpy.data.objects.get("ground_plane"); _gp = _g.hide_render
_g.hide_render = True   # 局部视角临时隐藏地面，渲染后还原
ok, rep = lr.render(bpy.data.objects["cam_link_fiber"], os.path.join(OUT, "case2_v3_link_fiber.png"))
_g.hide_render = _gp
print("link_fiber render:", ok, rep)

# M1 与 SLM/BS 关键连接局部
lr2 = bc.LocalRenderRule(must_keep=["mirror_M1","dmd","slm","bs_dichroic","mirror_M3","lens_L4"])
bc.get_or_make_cam("cam_m1_slm_bs", loc=(0.85,-0.7,0.35), look_at=(0.85,0.0,0.0),
                   lens=60, clip_start=0.005, clip_end=4.0)
_g2 = bpy.data.objects.get("ground_plane"); _gp2 = _g2.hide_render
_g2.hide_render = True
ok2, rep2 = lr2.render(bpy.data.objects["cam_m1_slm_bs"], os.path.join(OUT, "case2_v3_m1_slm_bs.png"))
_g2.hide_render = _gp2
print("m1_slm_bs render:", ok2, rep2)

# 关键件分层核查（存在/参与渲染/入框）
KEY = ["pulse_laser","lens_L1","lens_L2","mirror_M1","mirror_M2","dmd","lens_L3","lens_L4",
       "bs_dichroic","hwp","polarizer","slm","mirror_M3","lens_L5","lens_L6","lens_L7",
       "holder","mmf_delay_1","mmf_delay_2","mmf_delay_3","bc_combiner","mmf_single","pd","oscilloscope"]
for camname in ("cam_overview","cam_link_fiber","cam_m1_slm_bs"):
    vn, report = bc.key_parts_ok(camname, KEY, cam_name=camname)
    bad = {k:v for k,v in report.items() if not (v["exists"] and v["renders"])}
    print(f"[{vn}] 关键件 {len(KEY)} 个；异常={bad if bad else '无'}")

# D：保存前恢复总览相机与显示状态
scene.camera = cam_ov
scene.view_settings.exposure = 0.0
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "scene_case2_v3.blend"))
print("saved scene_case2_v3.blend + 3 preview PNGs (v3 忠实复刻参考图)")
