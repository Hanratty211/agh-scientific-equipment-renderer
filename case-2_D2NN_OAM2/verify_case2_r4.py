#!/usr/bin/env python3
"""
verify_case2_r4.py — 用【射线/真实表面求交】替代 bbox 极值，复核光束端点是否贴真实作用面。
载入 saved scene（R3 版本），对每段光束终止端，向下游件真实 mesh 面发射线（ray_cast），
取真实光学表面距离。复现外部指出的 L2→M1 ≈ 27.18 mm 缺口。不改任何阈值，只记录实测。
结果写 verify_case2_r4_results.txt（保留）。
"""
import bpy, mathutils, os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "verify_case2_r4_results.txt")
lines = []
def log(s):
    print(s); lines.append(s)

bpy.ops.wm.open_mainfile(filepath=os.path.join(HERE, "render-output", "scene_case2.blend"))
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()

def ray_dist_to_surface(start, direction, target_name):
    """从 start 沿 direction 射线，返回到 target_name 真实 mesh 面的距离(m)。
    起点先沿 direction 微移 1mm 以清除自身光束/邻面自命中；
    返回 target 命中距离；若 5m 内首个命中不是 target 则记为 None。"""
    dirv = mathutils.Vector(direction).normalized()
    orig = mathutils.Vector(start)
    cast_from = orig + dirv * 0.001      # 退避 1mm，避开自身光束自命中
    hit, loc, nrm, idx, obj, mat = bpy.context.scene.ray_cast(deps, cast_from, dirv, distance=5.0)
    if not hit:
        return None
    oname = obj.name if obj else None
    if oname == target_name:
        # 距离从原始 start 起算
        return (loc - orig).length
    return None

log("=== R4 独立复算：光束终止端 → 下游真实表面 射线距离（非 bbox 极值）===")
log("说明：对每段光束终止端 p1，向 +x 方向射线到下游件真实 mesh 面；>0 表示端点未贴面（漂浮），≈0 贴合。")
pairs = [
    ("beam_seg_laser_L1", "lens_L1", (1, 0, 0)),
    ("beam_seg_L2_M1", "mirror_M1", (1, 0, 0)),
    ("beam_seg_M2_dmd", "dmd", (1, 0, 0)),
    ("beam_seg_dmd_L3", "lens_L3", (1, 0, 0)),
    ("beam_seg_L4_bs", "bs_dichroic", (1, 0, 0)),
    ("beam_seg_slm_M3", "mirror_M3", (1, 0, 0)),
    ("beam_seg_L6_L7", "lens_L7", (1, 0, 0)),
    ("beam_seg_L7_holder", "holder", (1, 0, 0)),
    ("beam_seg_bc_mmf", "mmf_single", (1, 0, 0)),
    ("beam_seg_mmf_pd", "pd", (1, 0, 0)),
]
any_gap = False
for seg, tgt, dirv in pairs:
    bo = bpy.data.objects.get(seg)
    p1 = bo.get("beam_p1")
    d = ray_dist_to_surface(p1, dirv, tgt)
    if d is None:
        log(f"  [?] {seg}→{tgt}: 射线 5m 内未命中 {tgt} 表面（端点 p1={tuple(round(v,4) for v in p1)}）")
        any_gap = True
    else:
        mm = d * 1000
        verdict = "贴合" if mm < 2.0 else "漂浮(未贴真实面)"
        if mm >= 2.0:
            any_gap = True
        log(f"  [{'OK' if mm<2.0 else 'GAP'}] {seg}→{tgt}: 端点距真实表面 {mm:.2f} mm -> {verdict}")

# 重点复核外部指出的 L2→M1
log("\n=== 重点：beam_seg_L2_M1 端点 → M1 真实镜面（外部复算 ≈27.18 mm）===")
b = bpy.data.objects.get("beam_seg_L2_M1")
p1 = b.get("beam_p1")
d = ray_dist_to_surface(p1, (1, 0, 0), "mirror_M1")
log(f"  端点 p1={tuple(round(v,4) for v in p1)}; 到 M1 真实表面 = {d*1000 if d else None:.2f} mm"
    if d else "  射线未命中 M1")
log(f"  外部报告值 ≈27.18 mm；本次独立复算 {'一致(>25mm 缺口)' if d and d*1000>25 else '见上'}")

log("\n=== 结论 ===")
log(f"  存在未贴真实面的光束段（漂浮/缺口）: {'是' if any_gap else '否'}")
log("  撤回 R2 '10/10 段贴真实表面、不漂浮不穿透' 结论：bbox 极值核查无效，真实射线核查存在缺口。")
with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print(f"\n{OUT} written")
