#!/usr/bin/env python3
"""
behavior_tests.py — 反例最小行为验证（真实 Blender 运行）
==========================================================
针对外部核查指出的三个反例，验证修复后的 blender_core 行为。
每个测试输出 PASS/FAIL + 实际数值，写入同目录 behavior_results.txt 并保留。

运行（headless）：
    /Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python behavior_tests.py

反例与期望：
  T1 solid_inter_mm3 世界缩放：两个重合单位立方体各自 scale=2 → 应 8 m³ = 8e9 mm³ 重叠
     （修复前漏世界缩放会返回 1 m³ = 1e9 mm³）
  T2 clip_check 数值四反例：前方裁剪内/前方超远/真后方/前后角点混合；
     独立计算 8 个局部角点的相机空间有符号深度，不靠消息文字判通过。
  T3 beam_axis_world 局部端点：非原点非对称轴与真实网格截面中心相等；
     平移/旋转/父级变换后仍相等，旧点不经过；缺失/篡改属性失败关闭。
  T4 key_parts_ok 只返回 in_clip_range：相机前方但水平画外仍可入裁剪深度；
     缺失目标/无相机报告 None，绝不输出误导性的 in_frame 键。
"""
import os
import sys
import math
import bpy
import mathutils

# 允许把本文件放在 skill 根目录或任意路径；从脚本所在目录导入 blender_core
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_here, "scripts"))
import blender_core as bc  # noqa: E402

OUT = os.path.join(_here, "behavior_results.txt")
_lines = []
def log(msg):
    print(msg)
    _lines.append(msg)

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.unit_settings.system = 'METRIC'
scene.unit_settings.scale_length = 1.0

results = []

# ---------- T1: solid_inter_mm3 世界缩放 ----------
# 两个重合单位立方体(size=1)，各自 scale=2 -> 世界 2x2x2，重叠应 8 m³
A = bc.box("t1_a", 1, 1, 1, (0, 0, 0))
B = bc.box("t1_b", 1, 1, 1, (0, 0, 0))
A.scale = (2, 2, 2)
B.scale = (2, 2, 2)
# 赋 scale 后必须刷新 depsgraph，使 matrix_world 生效（否则 determinant 仍为 1）
bpy.context.view_layer.update()
v_mm3 = bc.solid_inter_mm3(A, B)
v_m3 = v_mm3 / 1e9
exp_m3 = 8.0
ok1 = abs(v_m3 - exp_m3) < 0.05
results.append(("T1", ok1, f"重合 scale=2 单位立方体 重叠={v_m3:.3f} m³ (期望 {exp_m3} m³)"))
log(f"T1 solid_inter_mm3(两重合 scale=2 立方体) = {v_m3:.3f} m³ -> {'PASS' if ok1 else 'FAIL'} (期望 8 m³)")

# ---------- T2: 独立计算所有 8 个角点的相机坐标；只判轴向裁剪 ----------
cam = bc.make_cam("t2_cam", (0.0, 0.0, 11.0), look_at=(0.0, 0.0, 10.0),
                  lens=50, clip_start=0.001, clip_end=2.0)
# 世界 Z 越低越在相机前；z=0 是前方 11m，不是后方（撤回旧 T2）。
cases = [
    ("front_in", (0., 0., 10.), 0.1, True, lambda d: all(0.9 < x < 1.1 for x in d)),
    ("front_far", (0., 0., 0.), 0.1, False, lambda d: all(x > 10.9 for x in d)),
    ("behind", (0., 0., 12.), 0.1, False, lambda d: all(x < -0.9 for x in d)),
    ("mixed", (0., 0., 11.), 0.4, False,
     lambda d: sum(x > 0 for x in d) == 4 and sum(x < 0 for x in d) == 4),
]
t2_checks = []
for label, loc, size, expected, depth_rule in cases:
    obj = bc.box("t2_" + label, size, size, size, loc)
    bpy.context.view_layer.update()
    inv = cam.matrix_world.inverted()
    depth = [-(inv @ (obj.matrix_world @ mathutils.Vector(c))).z for c in obj.bound_box]
    _msg, actual = bc.clip_check(cam.name, obj.name)
    numerical = depth_rule(depth)
    full_range = all(cam.data.clip_start <= x <= cam.data.clip_end for x in depth)
    ok = numerical and (full_range is expected) and (actual is expected)
    t2_checks.append(ok)
    log(f"T2 {label}: depth=[{min(depth):.4f},{max(depth):.4f}]m "
        f"front={sum(x>0 for x in depth)}/8 expected={expected} actual={actual} "
        f"numeric={numerical} -> {'PASS' if ok else 'FAIL'}")
results.append(("T2", all(t2_checks), f"四类前后/裁剪组合通过={sum(t2_checks)}/4"))

# ---------- T3: 非原点非对称轴，逐次与真实局部网格截面中心对照 ----------
p0, p1 = mathutils.Vector((1.2, -0.7, 0.4)), mathutils.Vector((2.7, 0.8, 2.3))
b3 = bc.beam("t3_beam", p0, p1, r=0.025)
mid = tuple(p0.lerp(p1, 0.3))  # 不对称测试点，不能只检 0.5 对称点
old_mid = mid

def actual_mesh_axis(obj):
    """独立从圆柱局部网格上下截面顶点求中心，再变换到世界坐标。"""
    verts = obj.data.vertices
    loz, hiz = min(v.co.z for v in verts), max(v.co.z for v in verts)
    def mean_end(z):
        vv = [v.co for v in verts if abs(v.co.z - z) < 1e-6]
        return obj.matrix_world @ (sum(vv, mathutils.Vector()) / len(vv))
    return mean_end(loz), mean_end(hiz)

def axis_check(label, obj, known_expected=True):
    bpy.context.view_layer.update()
    ends = bc.beam_axis_world(obj)
    mesh = actual_mesh_axis(obj)
    axis_ok = (ends is not None and all((mathutils.Vector(a) - b).length < 1e-5
                                         for a, b in zip(ends, mesh))) if known_expected else ends is None
    if known_expected:
        q = tuple(mesh[0].lerp(mesh[1], 0.3))
        d, t, passed, known = bc.beam_crosses_point(obj, q, tol=1e-5)
        axis_ok &= known and passed and abs(d) < 1e-5 and abs(t - 0.3) < 1e-5
        log(f"T3 {label}: axis/mesh Δmax={max((mathutils.Vector(a)-b).length for a,b in zip(ends,mesh)) if ends else -1:.7f}m "
            f"t={t} known={known} pass={passed} -> {'PASS' if axis_ok else 'FAIL'}")
    else:
        _, _, passed, known = bc.beam_crosses_point(obj, tuple(mesh[0]))
        axis_ok &= not known and not passed
        log(f"T3 {label}: axis={ends} known={known} pass={passed} -> {'PASS' if axis_ok else 'FAIL'}")
    return axis_ok

t3_checks = [axis_check('created', b3)]
# 旧坐标的 0.3 位置必须准确；证明不是世界端点再乘对象 matrix_world。
d, t, passed, known = bc.beam_crosses_point(b3, mid, tol=1e-5)
t3_checks.append(known and passed and abs(d) < 1e-5 and abs(t - 0.3) < 1e-5)
b3.location += mathutils.Vector((3.0, -1.0, 0.6))
t3_checks.append(axis_check('translated', b3))
_, _, old_pass, old_known = bc.beam_crosses_point(b3, old_mid, tol=1e-5)
t3_checks.append(old_known and not old_pass)
b3.rotation_euler.rotate_axis('Z', math.radians(41))
t3_checks.append(axis_check('rotated', b3))
parent = bc.box('t3_parent', 0.1, 0.1, 0.1, (0.2, -0.3, 0.4))
bpy.context.view_layer.update()
prior = b3.matrix_world.copy()
b3.parent = parent
b3.matrix_world = prior  # 设父级时不使几何瞬移
parent.location += mathutils.Vector((-0.8, 1.2, 0.3))
parent.rotation_euler[1] = math.radians(28)
t3_checks.append(axis_check('parent_transform', b3))
# 局部属性被改写为错误坐标时不能再假装是网格轴。
b3['beam_p0'] = tuple(mathutils.Vector(b3['beam_p0']) + mathutils.Vector((0.17, 0, 0)))
t3_checks.append(axis_check('tampered_local_endpoint', b3, known_expected=False))
nb = bc.beam('t3_norecord', p0, p1, r=0.025, record_ends=False)
t3_checks.append(axis_check('missing_endpoint', nb, known_expected=False))
results.append(('T3', all(t3_checks), f"网格轴/创建/平移/旋转/父级/旧点/篡改/缺失通过={sum(t3_checks)}/{len(t3_checks)}"))

# ---------- T4: 轴向裁剪与水平/垂直画幅不得混淆 ----------
wide = bc.box('t4_horizontal_outside', .1, .1, .1, (40., 0., 10.))
vertical = bc.box('t4_vertical_outside', .1, .1, .1, (0., 40., 10.))
inside = bc.box('t4_center_inside', .1, .1, .1, (0., 0., 10.))
bpy.context.view_layer.update()
_, r4 = bc.key_parts_ok('t4', [wide.name, vertical.name, inside.name,
                                't4_missing'], cam_name=cam.name)
_, r_none = bc.key_parts_ok('t4_nocamera', [inside.name])
# Independently project bbox corners: xy outside while depth remains between near/far.
from bpy_extras.object_utils import world_to_camera_view
xy = {}
for obj in (wide, vertical, inside):
    vs = [world_to_camera_view(scene, cam, obj.matrix_world @ mathutils.Vector(c))
          for c in obj.bound_box]
    xy[obj.name] = (min(v.x for v in vs), max(v.x for v in vs),
                    min(v.y for v in vs), max(v.y for v in vs))
checks4 = [all('in_clip_range' in r and 'in_frame' not in r for r in r4.values()),
           r4[wide.name]['in_clip_range'] is True,
           r4[vertical.name]['in_clip_range'] is True,
           r4[inside.name]['in_clip_range'] is True,
           xy[wide.name][0] > 1, xy[vertical.name][2] > 1,
           0 < xy[inside.name][0] < xy[inside.name][1] < 1,
           0 < xy[inside.name][2] < xy[inside.name][3] < 1,
           r4['t4_missing']['in_clip_range'] is None,
           r_none[inside.name]['in_clip_range'] is None]
results.append(('T4', all(checks4), f'裁剪与投影分离={sum(checks4)}/{len(checks4)}'))
log(f'T4 clip-only key vs independent XY projection: {sum(checks4)}/{len(checks4)} '
    f"horizontal={xy[wide.name]} vertical={xy[vertical.name]} -> "
    f"{'PASS' if all(checks4) else 'FAIL'}")

# ---------- 汇总 ----------
log("")
log("==== 行为验证汇总 ====")
all_ok = True
for tag, ok, desc in results:
    log(f"  [{ 'PASS' if ok else 'FAIL' }] {tag}: {desc}")
    if not ok:
        all_ok = False
log(f"总体: {'全部 PASS' if all_ok else '存在 FAIL'}")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(_lines) + "\n")
print(f"behavior_results.txt written: {OUT}")
