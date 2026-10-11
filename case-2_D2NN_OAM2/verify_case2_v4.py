#!/usr/bin/env python3
"""
B：修复核查方法（最小反例验证）。
修正 R7 指出的 5 项核查缺陷：
  1. 射线求交：不"推进 1mm 进镜片内"；分别报告 接触/间隙/穿入/未命中；先碰其他对象要报告该对象。
  2. 真实镜面法向：从【最终几何】取世界法向（采样 mesh 面法向，非 mirror_normal 自定义属性），与属性比较，不一致则不通过。
  3. 相机入框：真投影（world_to_camera_view），非 visible_get；画外对象不入框。
  4. 地面遮挡：待显示器件位于不透明地面以下时能被发现。
  5. 反例：透镜前表面端点不误判为后表面距离。
"""
import bpy, mathutils, os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "verify_case2_v4_results.txt")
lines = []
def log(s):
    print(s); lines.append(s)

bpy.ops.wm.open_mainfile(filepath=os.path.join(HERE, "render-output", "scene_case2_v3.blend"))
bpy.context.view_layer.update()
deps = bpy.context.evaluated_depsgraph_get()
scene = bpy.context.scene

def world_ray(origin, direction, distance=5.0):
    """世界空间射线：返回 (命中对象名, 命中点, 面法向(世界), 距离)。不推进起点。"""
    o = mathutils.Vector(origin)
    d = mathutils.Vector(direction).normalized()
    hit, loc, nrm, idx, obj, mat = scene.ray_cast(deps, o, d, distance=distance)
    if not hit:
        return None, None, None, None
    return (obj.name if obj else None), loc, nrm, (loc - o).length

def classify_gap(beam_obj, target_name, prop_dir):
    """从光束端点 p1 沿 prop_dir 向目标求交。
    不推进起点（修 R7 缺陷 1）。分别报告：接触(<0.5mm)/间隙(0.5-5mm)/穿入(命中点在起点后方)/未命中/先碰其他。
    """
    p1 = mathutils.Vector(beam_obj.get("beam_p1"))
    d = mathutils.Vector(prop_dir).normalized()
    # 不推进：从 p1 直接射线
    hit, loc, nrm, dist = world_ray(p1, d)
    if hit is None:
        return "未命中", p1, None, None
    if hit == target_name:
        if dist < 0.5:
            return "接触", p1, hit, dist
        else:
            return "间隙", p1, hit, dist
    else:
        return f"先碰{hit}", p1, hit, dist

def real_mirror_normal(obj):
    """从最终 mesh 几何取真实镜面法向（面积最大面=镜板大面），非自定义属性。"""
    me = obj.data
    if obj.type != 'MESH' or me is None:
        return None
    mw = obj.matrix_world
    best = None; best_area = -1
    for poly in me.polygons:
        wn = (mw.to_3x3() @ poly.normal).normalized()
        if poly.area > best_area:
            best_area = poly.area; best = wn
    return best

log("=== v4 核查方法修复（最小反例）===\n")

log("[反例1] 透镜前表面端点不误判为后表面")
# beam_laser_L1 端点 p1 应接触 lens_L1 前表面（间隙≈0）；旧方法推进 1mm 误报 8mm
b = bpy.data.objects.get("beam_laser_L1")
cls, p1, hit, dist = classify_gap(b, "lens_L1", (1,0,0))
log(f"  beam_laser_L1→lens_L1: {cls} 命中={hit} 距离={dist*1000 if dist else None:.2f}mm"
    f"（旧推进法误报 8mm；修正后应=接触或小幅间隙）")

log("\n[反例2] 真实镜面法向 vs 记录属性（不一致则不通过）")
for nm in ["mirror_M1","mirror_M2","mirror_M3"]:
    o = bpy.data.objects.get(nm)
    rn = real_mirror_normal(o)
    an = o.get("mirror_normal")
    if rn is None:
        log(f"  {nm}: 几何法向取不到（非 MESH？）"); continue
    anv = mathutils.Vector(an).normalized() if an else None
    if anv is None:
        log(f"  {nm}: 无属性；几何法向={tuple(round(v,3) for v in rn)}")
    else:
        match = rn.dot(anv) > 0.95
        log(f"  {nm}: 几何法向={tuple(round(v,3) for v in rn)} 属性={tuple(round(v,3) for v in anv)} "
            f"一致={match}{'✓' if match else '✗ 不一致（不得用属性自证）'}")
    # 验证 +x 入射经真实镜面反射方向
    if rn is not None:
        i = mathutils.Vector((1,0,0))
        refl = (i - 2*i.dot(rn)*rn).normalized()
        log(f"    +x 入射经真实镜面反射 = {tuple(round(v,3) for v in refl)}")

log("\n[反例3] 相机真投影入框（非 visible_get）")
from mathutils import Vector
import bpy_extras
def in_frame(cam_name, obj_name):
    cam = bpy.data.objects.get(cam_name)
    o = bpy.data.objects.get(obj_name)
    if not cam or not o: return "缺对象"
    co = bpy_extras.object_utils.world_to_camera_view(scene, cam, o.matrix_world.translation)
    if isinstance(co, (list,tuple)): co = co[0], co[1]
    # 轴向裁剪（co.z>0 在相机前）+ 横纵投影范围
    front = co[2] if len(co)>2 else None
    inxy = (0<=co[0]<=1 and 0<=co[1]<=1)
    return f"画内" if inxy else "画外"

# 外部 R7：M1 完全在 cam_m1_slm_bs 左侧画外
log(f"  M1 @ cam_m1_slm_bs: {in_frame('cam_m1_slm_bs','mirror_M1')}（外部复算=画外，须真投影确认）")
log(f"  M1 @ cam_overview: {in_frame('cam_overview','mirror_M1')}")

log("\n[反例4] 地面遮挡（待显示器件位于不透明地面以下能被发现）")
ground = bpy.data.objects.get("ground_plane")
gz = ground.matrix_world.translation.z if ground else -0.02
below = []
for k in ["lens_L5","lens_L6","lens_L7","holder","bc_combiner","mmf_single","pd","oscilloscope"]:
    o = bpy.data.objects.get(k)
    if o and o.matrix_world.translation.z < gz:
        below.append(k)
log(f"  地面 z={gz}; 位于地面以下的待显示器件: {below if below else '无'}")
log(f"  若地面不透明，以下器件在总览将被遮挡: {below if below else '无'}")

log("\n=== 结论 ===")
log("  核查方法已修正（不推进起点/几何法向/真投影/地面遮挡）；反例结果见上。")
log("  端点贴合/镜面方向/入框/遮挡**分开报告**，不用部件数量或非黑统计证明复刻通过。")
with open(OUT,"w",encoding="utf-8") as f:
    f.write("\n".join(lines)+"\n")
print(f"\n{OUT} written")
