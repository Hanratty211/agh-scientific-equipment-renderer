#!/usr/bin/env python3
"""
case-2 build: D2NN OAM-STM 系统 Fig.2(a) 三维重建（可重跑）
使用修正后的通用助手 blender_core（不带 case-1 对象名/坐标）。
本轮为低成本初稿：无字总览 + 关键连接局部视图 + 证据表引用；不追求正式高样本。
"""
import os, sys, math
import mathutils
import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, "/Users/wht/Desktop/黑客松/agh-research-figure-skill/skills/agh-scientific-equipment-renderer/scripts")
import blender_core as bc

OUT = os.path.join(HERE, "render-output")
os.makedirs(OUT, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
bc.setup_scene()

# ---- 材质（示意，中性；红为参考图着色，不渲染实体红光）----
M_LASER  = bc.mat("mat_laser",  base=(0.20, 0.22, 0.26), rough=0.5, metal=0.6)
M_LENS   = bc.glass_mat("mat_lens", base=(0.65, 0.85, 0.95), rough=0.05, ior=1.5)
M_MIRR   = bc.mat("mat_mirr",   base=(0.85, 0.87, 0.90), rough=0.08, metal=1.0)
M_DMD    = bc.mat("mat_dmd",    base=(0.12, 0.14, 0.18), rough=0.4, metal=0.3)
M_SLM    = bc.mat("mat_slm",    base=(0.10, 0.12, 0.16), rough=0.4, metal=0.3)
M_THIN   = bc.glass_mat("mat_thin", base=(0.55, 0.75, 0.90), rough=0.15, ior=1.5)   # HWP/Polarizer/Iris 薄件（半透）
M_PRISM  = bc.glass_mat("mat_prism", base=(0.55, 0.75, 0.95), rough=0.05, ior=1.5)
M_FIBER  = bc.mat("mat_fiber",  base=(0.95, 0.95, 0.90), rough=0.4, metal=0.0)
M_HOLD   = bc.mat("mat_holder", base=(0.35, 0.35, 0.38), rough=0.6, metal=0.5)
M_BOX    = bc.mat("mat_box",    base=(0.30, 0.30, 0.34), rough=0.6, metal=0.4)
M_PDBODY = bc.mat("mat_pd",     base=(0.15, 0.45, 0.25), rough=0.5, metal=0.3)
M_SCOPE  = bc.mat("mat_scope",  base=(0.10, 0.12, 0.14), rough=0.5, metal=0.3)
M_BEAM   = bc.glass_mat("mat_beam", base=(0.85, 0.85, 0.90), rough=0.2, ior=1.2)  # 中性示意光束（非红）

# ---- 照明（关键修复）：factory empty 场景无灯光；加 Sun/area 灯，否则 Cycles 渲染全黑 ----
def _add_light(name, ltype, loc, rot, energy, color=(1.0, 1.0, 1.0)):
    data = bpy.data.lights.new(name, ltype)
    data.energy = energy
    data.color = color
    ob = bpy.data.objects.new(name, data)
    ob.location = loc
    ob.rotation_euler = rot
    bpy.context.scene.collection.objects.link(ob)
    return ob

_add_light("key_light",  "SUN",  (-0.6, -1.2, 1.6), (math.radians(45), 0, math.radians(20)), 14.0)
_add_light("fill_light", "SUN",  (1.6, 0.8, 1.0), (math.radians(50), 0, math.radians(-120)), 5.0)
_add_light("rim_light",  "AREA", (0.85, 0.0, 0.7), (0, 0, 0), 600.0)

# 地面参考平面（z=-0.02，浅灰；提供环境反射基准，非光学部件）
import mathutils
gdata = bpy.data.meshes.new("ground_plane")
verts = [(-0.6, -1.5, -0.02), (2.3, -1.5, -0.02), (2.3, 1.5, -0.02), (-0.6, 1.5, -0.02)]
gdata.from_pydata(verts, [], [(0,1,2),(0,2,3)])
gmat = bpy.data.materials.new("mat_ground"); gmat.use_nodes = True
gmat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.30,0.30,0.32,1.0)
gmat.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.9
gob = bpy.data.objects.new("ground_plane", gdata)
gob.data.materials.append(gmat)
bpy.context.scene.collection.objects.link(gob)


# ---- 布局常量（米；光路沿 +x 水平，z=0 为主光轴；建模假设，不标实测）----
Z0 = 0.0
# 各部件 x 位置（从左到右），等距示意（间距为建模假设）
X = {
    "laser": 0.00, "L1": 0.10, "L2": 0.20, "M1": 0.30, "M2": 0.40,
    "dmd": 0.50, "L3": 0.60, "iris1": 0.66, "L4": 0.72,
    "bs": 0.80, "hwp": 0.84, "pol": 0.87, "slm": 0.92, "M3": 1.02,
    "L5": 1.12, "iris2": 1.18, "L6": 1.24, "L7": 1.32,
    "holder": 1.40, "bc": 1.50, "mmf_s": 1.56, "pd": 1.62, "scope": 1.70,
}

def lens_at(name, x):
    # 薄镜：用扁圆柱（绕 z 轴旋转使轴向沿 x）
    o = bc.cyl(f"{name}", r=0.045, depth=0.008, loc=(x, 0, Z0), rot=(0, math.pi/2, 0), m=M_LENS)
    return o

def mirror_at(name, x):
    # 薄反射镜，竖直放置，反射 90°（M1/M2/M3 折叠）
    return bc.box(name, 0.003, 0.08, 0.08, (x, 0.0, Z0), m=M_MIRR,
                  rot=(0, math.radians(45), 0))

# 光源
bc.box("pulse_laser", 0.06, 0.05, 0.05, (X["laser"], 0, Z0), m=M_LASER)
# L1,L2 4f 扩束
lens_at("lens_L1", X["L1"]); lens_at("lens_L2", X["L2"])
# M1,M2 折叠镜
mirror_at("mirror_M1", X["M1"]); mirror_at("mirror_M2", X["M2"])
# DMD（板）
bc.box("dmd", 0.004, 0.09, 0.09, (X["dmd"], 0, Z0), m=M_DMD)
# L3+Iris+L4 4f 滤波
lens_at("lens_L3", X["L3"])
bc.cyl("iris1", r=0.02, depth=0.006, loc=(X["iris1"], 0, Z0), rot=(0, math.pi/2, 0), m=M_THIN)
lens_at("lens_L4", X["L4"])
# 分光棱镜(dichroic) + HWP + Polarizer + SLM
bc.box("bs_dichroic", 0.004, 0.07, 0.07, (X["bs"], 0, Z0), m=M_PRISM)
bc.box("hwp", 0.003, 0.07, 0.07, (X["hwp"], 0, Z0), m=M_THIN)
bc.box("polarizer", 0.003, 0.07, 0.07, (X["pol"], 0, Z0), m=M_THIN)
bc.box("slm", 0.004, 0.09, 0.09, (X["slm"], 0, Z0), m=M_SLM)
# M3 反射
mirror_at("mirror_M3", X["M3"])
# L5+Iris+L6 4f 滤波
lens_at("lens_L5", X["L5"])
bc.cyl("iris2", r=0.02, depth=0.006, loc=(X["iris2"], 0, Z0), rot=(0, math.pi/2, 0), m=M_THIN)
lens_at("lens_L6", X["L6"])
# L7 聚焦 + Holder
lens_at("lens_L7", X["L7"])
bc.box("holder", 0.04, 0.10, 0.10, (X["holder"], 0, Z0), m=M_HOLD)
# 3 条 MMF 延迟线（并排短圆柱 + 束；2/4/6 m 折叠成束，建模假设）
for i, y in enumerate([-0.02, 0.0, 0.02], start=1):
    bc.cyl(f"mmf_delay_{i}", r=0.006, depth=0.06, loc=(X["holder"], y, Z0), rot=(0, math.pi/2, 0), m=M_FIBER)
# 3×1 合束器
bc.box("bc_combiner", 0.05, 0.08, 0.08, (X["bc"], 0, Z0), m=M_BOX)
# 输出 MMF
bc.cyl("mmf_single", r=0.006, depth=0.03, loc=(X["mmf_s"], 0, Z0), rot=(0, math.pi/2, 0), m=M_FIBER)
# PD + Oscilloscope
bc.box("pd", 0.05, 0.05, 0.05, (X["pd"], 0, Z0), m=M_PDBODY)
bc.box("oscilloscope", 0.08, 0.07, 0.09, (X["scope"], 0, Z0), m=M_SCOPE)

# ---- 光路段（示意，中性色）：端点贴【相邻部件实际表面】，不漂浮/不穿透（验证发现的缺陷修正）----
# 各部件 x 半厚（米）：lens=0.004, dmd/slm=0.002, bs=0.002, hwp/pol=0.0015, mirror=0.0015,
# holder=0.02, laser=0.03, mmf_single=0.015, pd=0.025, bc=0.025, scope=0.04
LT=0.004; PLT=0.002; MIRT=0.0015; HWT=0.0015; HDRT=0.02; LAS=0.03; MSF=0.015; PDT=0.025; BCT=0.025
# 45°倾角薄镜的 bbox 最小 x ≈ loc.x - 0.0293（比半厚 0.0015 大），故镜入射面用实际 bbox 面
MIRT_FACE = 0.0293  # 镜倾斜后入射面相对 loc.x 的偏移（米）
def _seg(name, x_upstream_face, x_downstream_face):
    bc.beam(name, (x_upstream_face, 0, Z0), (x_downstream_face, 0, Z0), r=0.004, m=M_BEAM)

_seg("beam_seg_laser_L1", X["laser"]+LAS,   X["L1"]-LT)          # 激光出射面 -> L1 入射面
_seg("beam_seg_L2_M1",    X["L2"]+LT,       X["M1"]-MIRT_FACE)   # L2 出射面 -> M1 入射面（实际镜面）
_seg("beam_seg_M2_dmd",   X["M2"]+MIRT_FACE,X["dmd"]-PLT)        # M2 出射面 -> DMD 入射面
_seg("beam_seg_dmd_L3",   X["dmd"]+PLT,     X["L3"]-LT)          # DMD 出射面 -> L3 入射面
_seg("beam_seg_L4_bs",    X["L4"]+LT,       X["bs"]-PLT)         # L4 出射面 -> BS(dichroic) 入射面
_seg("beam_seg_slm_M3",   X["slm"]+PLT,     X["M3"]-MIRT_FACE)   # SLM 出射面 -> M3 入射面（实际镜面）
_seg("beam_seg_L6_L7",    X["L6"]+LT,       X["L7"]-LT)          # L6 出射面 -> L7 入射面
_seg("beam_seg_L7_holder",X["L7"]+LT,       X["holder"]-HDRT)   # L7 出射面 -> Holder 入射面
_seg("beam_seg_bc_mmf",   X["bc"]+BCT,      X["mmf_s"]-MSF)      # BC 出射面 -> MMF 入射面
_seg("beam_seg_mmf_pd",   X["mmf_s"]+MSF,   X["pd"]-PDT)         # MMF 出射面 -> PD 入射面

# ---- 相机：总览 + 关键连接局部 ----
# （不再二次 setup_scene，那会清空已建几何；裁剪已由首次 setup_scene 设好）
cam_ov = bc.make_cam("cam_overview", (0.85, -1.35, 0.75),
                      look_at=(0.85, 0, 0.0), lens=24, clip_start=0.005, clip_end=10.0)
# 关键连接局部：DMD→SLM 4f 区（L3/L4/BS/SLM）
bc.get_or_make_cam("cam_link_dmd_slm", loc=(0.70, -0.35, 0.25), look_at=(0.78, 0, 0.02),
                   lens=50, clip_start=0.005, clip_end=3.0)
# 关键连接局部：L7→MMF/Holder/BC 区
bc.get_or_make_cam("cam_link_fiber", loc=(1.42, -0.35, 0.22), look_at=(1.45, 0, 0.02),
                   lens=50, clip_start=0.005, clip_end=3.0)

scene = bpy.context.scene
scene.camera = cam_ov
scene.render.resolution_x = 1600
scene.render.resolution_y = 900
scene.cycles.samples = 32          # 低成本初稿
scene.cycles.use_denoising = True

# 无字总览
scene.render.filepath = os.path.join(OUT, "case2_preview_overview_wordless.png")
bpy.ops.render.render(write_still=True)

# 关键连接局部（用 LocalRenderRule，保证光纤束/BC 必须参与渲染，缺失则拒绝）
lr = bc.LocalRenderRule(must_keep=["holder", "mmf_delay_1", "mmf_delay_2", "mmf_delay_3",
                                    "bc_combiner", "mmf_single", "lens_L7"])
_sc = bpy.context.scene
_sc.cycles.use_denoising = True
_sc.view_settings.exposure = -0.6
_g = bpy.data.objects.get("ground_plane")
_g_prev = _g.hide_render if _g else None
if _g:
    _g.hide_render = True     # 局部视角临时隐藏地面（防过曝/占满），渲染后还原
ok, rep = lr.render(bpy.data.objects["cam_link_fiber"], os.path.join(OUT, "case2_preview_link_fiber.png"))
if _g and _g_prev is not None:
    _g.hide_render = _g_prev
_sc.view_settings.exposure = 0.0
print("link_fiber render:", ok, rep)

lr2 = bc.LocalRenderRule(must_keep=["dmd", "slm", "lens_L3", "lens_L4", "bs_dichroic"])
_sc = bpy.context.scene
_sc.view_settings.exposure = -0.6
_g2 = bpy.data.objects.get("ground_plane")
_g2_prev = _g2.hide_render if _g2 else None
if _g2:
    _g2.hide_render = True
ok2, rep2 = lr2.render(bpy.data.objects["cam_link_dmd_slm"], os.path.join(OUT, "case2_preview_link_dmd_slm.png"))
if _g2 and _g2_prev is not None:
    _g2.hide_render = _g2_prev
_sc.view_settings.exposure = 0.0
print("link_dmd_slm render:", ok2, rep2)

# 关键件分层核查（存在/参与渲染/入框）
KEY = ["pulse_laser","lens_L1","lens_L2","mirror_M1","mirror_M2","dmd","lens_L3","lens_L4",
       "bs_dichroic","hwp","polarizer","slm","mirror_M3","lens_L5","lens_L6","lens_L7",
       "holder","mmf_delay_1","mmf_delay_2","mmf_delay_3","bc_combiner","mmf_single","pd","oscilloscope"]
for camname in ("cam_overview","cam_link_dmd_slm","cam_link_fiber"):
    vn, report = bc.key_parts_ok(camname, KEY, cam_name=camname)
    bad = {k:v for k,v in report.items() if not (v["exists"] and v["renders"])}
    print(f"[{vn}] 关键件 {len(KEY)} 个；异常={bad if bad else '无'}")

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "scene_case2.blend"))
print("saved scene_case2.blend + 3 preview PNGs（低成本初稿完成）")
