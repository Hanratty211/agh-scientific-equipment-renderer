#!/usr/bin/env python3
"""独立几何核查（载入 case-2 场景，不渲染）：光路段贴合 / MMF 并排 / 相机入框。"""
import bpy, mathutils, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=os.path.join(HERE, "render-output", "scene_case2.blend"))
sys.path.insert(0, "/Users/wht/Desktop/黑客松/agh-research-figure-skill/skills/agh-scientific-equipment-renderer/scripts")
import blender_core as bc
bpy.context.view_layer.update()

def nearest_x_face(o, probe_x):
    bb = [o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    xs = [v[0] for v in bb]
    return min(xs, key=lambda z: abs(z - probe_x))

print("=== 光路段 终止端-目标入射面 贴合核查 (间隙应<2mm, 不漂浮不穿透) ===")
checks = [
    ("beam_seg_laser_L1", "lens_L1"),
    ("beam_seg_L2_M1", "mirror_M1"),
    ("beam_seg_M2_dmd", "dmd"),
    ("beam_seg_dmd_L3", "lens_L3"),
    ("beam_seg_L4_bs", "bs_dichroic"),
    ("beam_seg_slm_M3", "mirror_M3"),
    ("beam_seg_L6_L7", "lens_L7"),
    ("beam_seg_L7_holder", "holder"),
    ("beam_seg_bc_mmf", "mmf_single"),
    ("beam_seg_mmf_pd", "pd"),
]
for seg, tgt in checks:
    bo = bpy.data.objects.get(seg)
    p1 = bo.get("beam_p1")
    to = bpy.data.objects.get(tgt)
    nf = nearest_x_face(to, p1[0])
    gap = abs(p1[0] - nf) * 1000
    ok = gap < 2.0
    print(f"  [{'OK' if ok else 'GAP'}] {seg}: 终止端p1x={p1[0]:.4f} {tgt}入射面x={nf:.4f} 间隙={gap:.1f}mm")

print("\n=== 3×MMF 延迟线并排位置 (y 应 -0.02/0/0.02, 折叠成束) ===")
for i in (1, 2, 3):
    o = bpy.data.objects.get(f"mmf_delay_{i}")
    print(f"  mmf_delay_{i}: loc=({o.location.x:.3f},{o.location.y:.3f},{o.location.z:.3f})")

print("\n=== 相机 in_frame 核查 (clip_check 修复版, 世界坐标) ===")
for cam, tgt in [("cam_link_fiber", "holder"), ("cam_link_fiber", "bc_combiner"),
                 ("cam_link_dmd_slm", "dmd"), ("cam_link_dmd_slm", "slm"),
                 ("cam_overview", "pulse_laser"), ("cam_overview", "oscilloscope")]:
    m, inr = bc.clip_check(cam, tgt)
    print(f"  [{ 'OK' if inr else 'FAIL'}] {cam}->{tgt}: in_frame={inr}")

print("\n=== beam_crosses_point 对光路段终止端一致性 (record_ends) ===")
b = bpy.data.objects.get("beam_seg_L4_bs")
p1 = b.get("beam_p1")
d, t, passed, known = bc.beam_crosses_point(b, p1)
print(f"  beam_seg_L4_bs 终止端p1={tuple(round(v,4) for v in p1)}: dist={d}, passed={passed}, axis_known={known}")
