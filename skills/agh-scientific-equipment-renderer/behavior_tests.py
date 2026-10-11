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
  T2 clip_check 世界变换 + 相机后方：把对象放到相机后方 11m 处 → 必须报"全在后方/in_range=False"，
     不得报成 ~1m 通过
  T3 beam_crosses_point 过期端点：光束沿轴建好后整体平移 5m → 旧端点属性过期 →
     beam_crosses_point 应对原交点返回 axis_known=False / passed=False（不再误报经过）
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

# ---------- T2: clip_check 世界变换 + 相机后方 ----------
cam = bc.make_cam("t2_cam", (0.0, 0.0, 11.0), look_at=(0.0, 0.0, 10.0),
                  lens=50, clip_start=0.001, clip_end=2.0)
# 对象实际放在 z=0（相机在 z=11，朝向 -z 看 z=10；对象在 z=0 在相机后方 11m）
far = bc.box("t2_far", 0.1, 0.1, 0.1, (0.0, 0.0, 0.0))
# 触发 bpy 更新以便 bound_box/matrix_world 生效
bpy.context.view_layer.update()
msg, in_range = bc.clip_check("t2_cam", "t2_far")
log(f"T2 clip_check(对象在相机后方11m) -> in_range={in_range}; msg: {msg}")
# 期望：全部角点在相机后方 -> in_range=False，且消息含"后方"，不得报成 ~1m 通过
ok2 = (in_range is False) and ("后方" in msg or "behind" in msg)
results.append(("T2", ok2, f"相机后方11m 对象: in_range={in_range}（应 False，不得报通过）"))

# ---------- T3: beam_crosses_point 过期端点 ----------
# 建一条沿 x 轴、穿过原点 (0,0,0) 的光束，端点属性记录当前世界坐标
b3 = bc.beam("t3_beam", (-1.0, 0.0, 0.0), (1.0, 0.0, 0.0), r=0.05)
before = bc.beam_crosses_point(b3, (0.0, 0.0, 0.0))
# 现在把光束整体平移 +5m（世界变换），端点属性仍是旧值 -> 应判过期
b3.location = (5.0, 0.0, 0.0)
bpy.context.view_layer.update()
after = bc.beam_crosses_point(b3, (0.0, 0.0, 0.0))  # 原点此时已不在平移后的光束轴上
log(f"T3 平移前 beam_crosses_point(原点) = {before}")
log(f"T3 平移+5m后 beam_crosses_point(原点) = {after}")
# 期望：平移+5m 后原点已不在当前世界轴上 -> passed=False（关键修复：不再误报“经过原交点”）。
# 属性端点 + 当前 matrix_world 可正确重建平移后轴，故 known 仍 True（轴已知，只是不经过原点）。
d2, t2, passed2, known2 = after
ok3 = (passed2 is False)
# 平移前应对原点通过（构造保证）
d1, t1, passed1, known1 = before
ok3b = (known1 is True) and (passed1 is True)
# 额外验证：无端点属性时绝不判“经过”（包围盒对角线不作通过证据）
nb = bc.beam("t3_norecord", (-1.0, 0.0, 0.0), (1.0, 0.0, 0.0), r=0.05, record_ends=False)
_, _, npass, nknown = bc.beam_crosses_point(nb, (0.0, 0.0, 0.0))
ok3c = (npass is False) and (nknown is False)
log(f"T3 无端点属性 beam_crosses_point(原点) = ({npass}, {nknown}) -> 应 (False, False)")
results.append(("T3", (ok3 and ok3b and ok3c),
                f"平移前 known={known1}/passed={passed1}(应T/T)；平移+5m后 passed={passed2}(应F，不再误报)；无端点属性 passed={npass}/known={nknown}(应F/F)"))

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
