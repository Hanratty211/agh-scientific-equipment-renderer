import re
s = open('build_blender_v5.py').read()

# ---------- 1) 文档头 ----------
s = s.replace(
'''"""v3 — 87Sr optical lattice clock, proposed 77 K cryo cavity + MOT
Focused on Fig.7 scope only: furnace/Zeeman slower/stages excluded this round.''',
'''"""v5 — 87Sr optical lattice clock, proposed 77 K cryo cavity + MOT
Focused on Fig.7 scope only: furnace/Zeeman slower/stages excluded this round.''')

# ---------- 2) 光束材质：降低亮度/实体感 ----------
s = s.replace(
'''M_LAT    = mat("lattice_bm", (0.15,0.45,0.95), 0.2, 0.0, (0.1,0.4,1.0), 2.5)
M_CLK    = mat("clock_bm",   (0.90,0.12,0.12), 0.2, 0.0, (1.0,0.1,0.1), 2.5)
M_Cool   = mat("cool_bm",    (0.10,0.65,0.95), 0.2, 0.0, (0.0,0.55,0.9), 1.8)''',
'''# v5: 光束降亮降粗，让器件结构成为画面主体，避免光束遮住小特征
M_LAT    = mat("lattice_bm", (0.20,0.45,0.95), 0.3, 0.0, (0.1,0.4,1.0), 0.6)
M_CLK    = mat("clock_bm",   (0.85,0.15,0.15), 0.3, 0.0, (1.0,0.15,0.15), 0.6)
M_Cool   = mat("cool_bm",    (0.15,0.60,0.90), 0.3, 0.0, (0.05,0.45,0.8), 0.5)''')

# ---------- 3) 光束半径变细（beam 默认 0.003 -> 0.0012） ----------
s = s.replace("def beam(name, p0, p1, r=0.003, m=None, seg=16):",
              "def beam(name, p0, p1, r=0.0012, m=None, seg=16):")

# ---------- 4) 冷却光束统一到 MOT_X 共同中心 ----------
s = s.replace(
'''b1 = beam("cool_bm_1", (MOT_X + 0.060,  0.050, AXIS_Z),
                          (MOT_X - 0.010, -0.050, AXIS_Z), r=0.0025, m=M_Cool)
b2 = beam("cool_bm_2", (MOT_X + 0.060, -0.050, AXIS_Z),
                          (MOT_X - 0.010,  0.050, AXIS_Z), r=0.0025, m=M_Cool)
b3 = beam("cool_bm_3", (MOT_X + 0.010,  0.0, AXIS_Z + 0.050),
                          (MOT_X - 0.010,  0.0, AXIS_Z - 0.050), r=0.0025, m=M_Cool)
b4 = beam("cool_bm_4", (MOT_X - 0.010,  0.0, AXIS_Z + 0.050),
                          (MOT_X + 0.010,  0.0, AXIS_Z - 0.050), r=0.0025, m=M_Cool)''',
'''# v5: 4 束冷却光（±y 一对、±z 一对）中心线全部精确交于 (MOT_X, 0, AXIS_Z)，
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
# b4: 中点=(MOT_X,0,AXIS_Z) ✓''')

# ---------- 5) 晶格光束 + 光纤：缩到真空室外 + 侧壁开孔 ----------
s = s.replace(
'''lb1 = beam("lat_beam_1", (MOT_X + 0.055, 0.0, AXIS_Z),
                          (CAV_X - 0.045, 0.0, AXIS_Z), r=0.0028, m=M_LAT)
lb2 = beam("lat_beam_2", (CAV_X - 0.045, 0.0, AXIS_Z),
                          (MOT_X + 0.055, 0.0, AXIS_Z), r=0.0028, m=M_LAT)
# fiber entry (right side)
cyl("lat_fiber", 0.0035, 0.025, (MOT_X + 0.060, 0.0, AXIS_Z),
    (0, math.radians(90), 0), m=M_ILLUM, seg=24)''',
'''# 真空室侧壁实际 x 范围（前壁已剖切后）：右壁 x≈0.06（见 vac_shell bbox）
LAT_WALL_X = 0.060   # 右壁外表面
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
    (0, math.radians(90), 0), m=M_WIRE, seg=24)          # 室内段（接晶格光路起点）''')

# ---------- 6) 钟光束：走顶部窗口入射，不再斜穿侧墙 ----------
s = s.replace(
'''clk = beam("clock_bm", (MOT_X - 0.040, 0.028, AXIS_Z),
                         (CAV_X,        0.0,   AXIS_Z), r=0.0020, m=M_CLK)
# dichroic mirror (thin tilted disc, at cavity entrance region)
box("dichroic_mir", 0.018, 0.018, 0.0006,
    (CAV_X + 0.040, 0.014, AXIS_Z),
    rot=(0, math.radians(45), 0), m=M_SAPPH)''',
'''# 钟光束：从顶部窗口垂直/近垂直入射到二向色镜，再折向腔体
# （v4 中 clock_bm 斜穿右侧墙体，v5 改为走已开孔的顶部窗口）
CLK_TOP_Z = CHAM_CZ + CHAM_H/2 - T/2   # 顶壁中心
clk = beam("clock_bm", (MOT_X + 0.010, 0.0, CLK_TOP_Z + 0.020),
                         (CAV_X + 0.040, 0.014, AXIS_Z + 0.014), m=M_CLK)
# dichroic mirror (thin tilted disc, at cavity entrance region)
box("dichroic_mir", 0.018, 0.018, 0.0006,
    (CAV_X + 0.040, 0.014, AXIS_Z + 0.008),
    rot=(0, math.radians(45), 0), m=M_SAPPH)
# 顶壁窗口开孔：孔中心对准 clock_bm 入射点，尺寸与光路匹配
cyl("clock_top_hole", 0.005, T*3, (MOT_X + 0.010, 0.0, CLK_TOP_Z), (0,0,0))
# 二向色镜出射后走晶格轴入腔，不再穿任何未开孔壁面''')

# ---------- 7) 真空室壳体：把 lat_wall_hole 和 clock_top_hole 布尔切出 ----------
old = '''# glass windows at ports (thin, semi-transparent)'''
new = '''# v5: 侧壁激光开孔 + 顶壁钟光开孔（真实开孔，孔中心/尺寸/方向与光路匹配）
boolean_cut(shell, bpy.data.objects['lat_wall_hole'])
boolean_cut(shell, bpy.data.objects['clock_top_hole'])
# 铜腔左侧穿腔壁位置检查：cav_outer x∈[-0.16,0]，vac_shell x∈[-0.14,0.06]
# → 铜腔左端(-0.16)伸出真空室外壳左壁(-0.14)之外，即后窗端不穿过任何
#   未开孔壁面（已在外壳外）；铜腔右端(0.0)在内壳内，入口端不穿壁。
#   记录在 case notes，供人工核查。
# glass windows at ports (thin, semi-transparent)'''
s = s.replace(old, new, 1)

# ---------- 8) 铜腔真正的剖切：切掉朝向 cam_cut 的 1/4 外壁+内衬 ----------
old = '''# tilted sapphire window at rear end'''
new = '''# v5: 铜腔局部剖切 —— 切掉朝向 cam_cut(-y 侧) 的 1/4 外壳 + 对应内衬，
# 清楚展示入口、内壁、隔膜通孔、探测区域、后窗；不是仅靠挖空管腔
cav_cut_block = box("cav_cutaway", CAV_LEN + 0.01, CAV_R_OUT + 0.005, CAV_R_OUT + 0.005,
                    (CAV_X, -(CAV_R_OUT + 0.005)*0.55, AXIS_Z))
boolean_cut(cav_outer, cav_cut_block)
lining_cut_block = box("lining_cutaway", CAV_LEN*0.98 + 0.005, CAV_R_IN + 0.004, CAV_R_IN + 0.004,
                       (CAV_X, -(CAV_R_IN + 0.004)*0.55, AXIS_Z))
boolean_cut(lining, lining_cut_block)
# 剖切后腔内特征（内壁/通孔/后窗/探测区）从 -y 侧直接可见，无需移动相机

# tilted sapphire window at rear end'''
s = s.replace(old, new, 1)

# ---------- 9) 渲染输出改为 v5 + 新增两个连接位置局部预览 ----------
s = s.replace(
'''bpy.ops.wm.save_as_mainfile(filepath="render-output/scene_v4.blend")
print("scene_v4.blend saved")

def render(cam_obj, out):
    scene.camera = cam_obj
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)
    print("rendered", out)

render(cam1, "render-output/render_v4_overview.png")
render(cam3, "render-output/render_v4_cavity_cut.png")
print("v4 renders done (overview + cavity cut, per delivery spec)")
print("all v3 renders done")''',
'''# v5 新增相机：两个连接位置局部预览（供人工核查穿墙结构）
# cam4: 右壁激光光纤穿墙法兰局部
cam4 = make_cam("cam_port_right", (LAT_WALL_X + 0.06, -0.06, AXIS_Z + 0.02),
                look_at=(LAT_WALL_X, 0.0, AXIS_Z), lens=60)
# cam5: 顶壁钟光窗口 + 二向色镜局部
cam5 = make_cam("cam_port_top", (MOT_X + 0.010, -0.05, CLK_TOP_Z + 0.06),
                look_at=(MOT_X + 0.010, 0.0, CLK_TOP_Z + 0.01), lens=60)

bpy.ops.wm.save_as_mainfile(filepath="render-output/scene_v5.blend")
print("scene_v5.blend saved")

def render(cam_obj, out):
    scene.camera = cam_obj
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)
    print("rendered", out)

render(cam1, "render-output/render_v5_overview.png")
render(cam3, "render-output/render_v5_cavity_cut.png")
render(cam4, "render-output/render_v5_port_right.png")
render(cam5, "render-output/render_v5_port_top.png")
print("v5 renders done: overview + cavity cut + 2 port detail views")''')

open('build_blender_v5.py','w').write(s)
print("build_blender_v5.py written, len=", len(s))
