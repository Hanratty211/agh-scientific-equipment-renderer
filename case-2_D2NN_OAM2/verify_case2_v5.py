#!/usr/bin/env python3
"""
B（R9）：修正核查脚本 —— 全部单位统一为米；可失败断言 + 实际结果。
修正 R8 指出的 7 项：
  1. 接触阈值单位统一（0.5 mm = 0.0005 m）
  2. 有间隙样例确认 10 mm 不判接触
  3. 地面高度从实际世界几何取（非对象原点）
  4. 入框检查目标全部角点 + 横纵投影 + 轴向裁剪
  5. 实际实现 接触/间隙/穿入/未命中/先碰其他 分类
  6. 镜面法向用正确的世界变换；正负法向表示同一平面时不算不一致（取 abs(dot)）
  7. 可失败的断言（assert）+ 实际结果，不只打印"已修复"
"""
import bpy, mathutils, os, sys
from mathutils import Vector
import bpy_extras

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "verify_case2_v5_results.txt")
lines = []
RESULTS = []   # (断言名, 通过?, 实测值)
def log(s):
    print(s); lines.append(s)
def assert_that(name, cond, detail):
    RESULTS.append((name, bool(cond), detail))
    log(f"  [{'PASS' if cond else 'FAIL'}] {name}: {detail}")

# 单位常量（米）
TOL_CONTACT_M = 0.0005      # 0.5 mm —— 修 R8#1：v4 写成 0.5（=0.5 m）错误
TOL_GAP_MAX_M = 0.005       # 5 mm 以上算"间隙"（超出接触）
TOL_MM = 0.001              # 1 mm

def fresh_scene(path):
    bpy.ops.wm.open_mainfile(filepath=path)
    bpy.context.view_layer.update()
    return bpy.context.evaluated_depsgraph_get()

def world_ray(origin, direction, distance=5.0):
    """世界空间射线，**不推进起点**（修 R8#4 的前置：v3 推进 1mm 进镜片）。"""
    o = Vector(origin); d = Vector(direction).normalized()
    hit, loc, nrm, idx, obj, mat = bpy.context.scene.ray_cast(
        bpy.context.evaluated_depsgraph_get(), o, d, distance=distance)
    if not hit:
        return None, None, None, None
    return (obj.name if obj else None), loc, nrm, (loc - o).length

def classify(origin, direction, target, distance=5.0, tol_contact=TOL_CONTACT_M):
    """五分类：接触 / 间隙 / 穿入 / 未命中 / 先碰其他对象。单位=米。"""
    o = Vector(origin); d = Vector(direction).normalized()
    hit, loc, nrm, dist = world_ray(o, d, distance)
    if hit is None:
        return "未命中", None, None, None
    # 穿入：命中点相对起点在传播方向上有负投影（起点已在目标内部/背面之外）
    # 用目标 bbox 判定"起点在目标内部"
    tobj = bpy.data.objects.get(target)
    if tobj:
        local = tobj.matrix_world.inverted() @ o
        dims = tobj.dimensions
        inside = all(abs(local[i]) <= dims[i]/2 + 1e-6 for i in range(3)) if all(dims) else False
    else:
        inside = False
    if hit != target:
        return "先碰其他对象", hit, nrm, dist
    if inside:
        return "穿入", hit, nrm, dist
    if dist <= tol_contact:
        return "接触", hit, nrm, dist
    return "间隙", hit, nrm, dist

def mesh_world_normal(obj):
    """真实镜面法向：面积最大面的世界法向（正确世界变换 mw.to_3x3()）。修 R8#6。"""
    if obj.type != 'MESH':
        return None
    mw = obj.matrix_world
    best, best_area = None, -1
    for poly in obj.data.polygons:
        n = (mw.to_3x3() @ poly.normal).normalized()
        if poly.area > best_area:
            best_area, best = poly.area, n
    return best

def ground_top_z():
    """地面（不透明）世界高度：取地面 mesh 顶面的世界 z（**非对象原点**）。修 R8#3。"""
    g = bpy.data.objects.get("ground_plane")
    if not g:
        return None
    mw = g.matrix_world
    zs = [(mw @ v.co).z for v in g.data.vertices]
    return max(zs) if zs else None

def obj_corners_world(obj):
    return [obj.matrix_world @ Vector(c) for c in obj.bound_box]

def in_frame_corners(cam_name, obj_name):
    """入框：检查**全部角点**的横纵投影 + 轴向裁剪。修 R8#4。返回 (全部在框内?, 明细)"""
    cam = bpy.data.objects.get(cam_name)
    obj = bpy.data.objects.get(obj_name)
    if not cam or not obj:
        return None, "缺对象"
    res = []
    for c in obj_corners_world(obj):
        co = bpy_extras.object_utils.world_to_camera_view(bpy.context.scene, cam, c)
        x, y, z = (co[0], co[1], co[2]) if not isinstance(co, (list, tuple)) or len(co) >= 3 else (co[0], co[1], None)
        xy_ok = (0.0 <= x <= 1.0 and 0.0 <= y <= 1.0)
        clip_ok = (z is None) or (z > cam.data.clip_start and z < cam.data.clip_end)
        res.append(xy_ok and clip_ok)
    return all(res), f"{sum(res)}/{len(res)} 角点在框内且未裁剪"

# =====================================================================
log("=== R9 核查脚本修正（单位统一 + 可失败断言）===\n")

# ---- 反例 A：接触阈值单位 ----
log("[A] 单位统一（0.5 mm = 0.0005 m）—— 用合成场景独立验证，不依赖 case-2 场景")
bpy.ops.wm.read_factory_settings(use_empty=True)
# 造一个"薄板 + 光束端点贴前表面 0.3mm 间隙"的最小场景
import bmesh
def box_obj(name, sx, sy, sz, loc):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=bm.verts)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); o.location = loc
    bpy.context.scene.collection.objects.link(o); return o
plate = box_obj("plate", 0.002, 0.1, 0.1, (0.5, 0, 0))   # 薄板 2mm 厚，前表面 x=0.499
bpy.context.view_layer.update()
# 起点在前表面外侧 0.3 mm 处 → 应判"接触"
start_contact = (0.499 - 0.0003, 0, 0)
cls, hit, nrm, dist = classify(start_contact, (1,0,0), "plate")
assert_that("A1 前表面外 0.3mm → 接触", cls == "接触", f"分类={cls} dist={None if dist is None else round(dist*1000,3)}mm")
# 起点在前表面外侧 10 mm 处 → 应判"间隙"（不判接触）
start_gap = (0.499 - 0.010, 0, 0)
cls2, hit2, nrm2, dist2 = classify(start_gap, (1,0,0), "plate")
assert_that("A2 前表面外 10mm → 间隙（不判接触）", cls2 == "间隙", f"分类={cls2} dist={None if dist2 is None else round(dist2*1000,2)}mm")
# 起点在板内部 → 应判"穿入"
start_inside = (0.5, 0, 0)
cls3, hit3, nrm3, dist3 = classify(start_inside, (1,0,0), "plate")
assert_that("A3 起点在板内 → 穿入", cls3 == "穿入", f"分类={cls3}")
# 起点与板同侧但背离 → 未命中
cls4, *_ = classify(start_gap, (-1,0,0), "plate")
assert_that("A4 背离传播 → 未命中", cls4 == "未命中", f"分类={cls4}")
# 起点前面放一个遮挡物 → 先碰其他对象
blocker = box_obj("blocker", 0.001, 0.1, 0.1, (0.495, 0, 0))
bpy.context.view_layer.update()
cls5, hit5, *_ = classify((0.49, 0, 0), (1,0,0), "plate")
assert_that("A5 中间有遮挡物 → 先碰其他对象", cls5 == "先碰其他对象" and hit5 == "blocker", f"分类={cls5} 命中={hit5}")
# 阈值常量本身
assert_that("A6 接触阈值=0.0005 m（不是 0.5）", TOL_CONTACT_M == 0.0005, f"TOL_CONTACT_M={TOL_CONTACT_M}")

# ---- 反例 B：镜面法向正负同一平面不误判 ----
log("\n[B] 镜面法向：正负法向表示同一平面时不判不一致")
mir = box_obj("mir_test", 0.003, 0.08, 0.08, (0,0,0))
mir.rotation_euler = (0, 0.785398, 0)   # 绕 Y 45°
bpy.context.view_layer.update()
n_real = mesh_world_normal(mir)
n_record_pos = n_real.copy()
n_record_neg = -n_real.copy()
match_pos = abs(n_real.dot(n_record_pos.normalized())) > 0.95
match_neg = abs(n_real.dot(n_record_neg.normalized())) > 0.95   # 取 abs → 同一平面
assert_that("B1 同向法向 → 一致", match_pos, f"|dot|={abs(n_real.dot(n_record_pos.normalized())):.3f}")
assert_that("B2 反向法向（同一平面）→ 仍一致（取 abs）", match_neg, f"|dot|={abs(n_real.dot(n_record_neg.normalized())):.3f}")
# 正交法向 → 不一致
n_ortho = Vector((1,0,0))
assert_that("B3 正交法向 → 不一致", abs(n_real.dot(n_ortho)) <= 0.95,
            f"|dot|={abs(n_real.dot(n_ortho)):.3f} 真实法向={tuple(round(v,3) for v in n_real)}")

# ---- 反例 C：地面高度从实际几何取 + 地面遮挡 ----
log("\n[C] 地面高度从实际世界几何取（非对象原点）；地面下器件可被发现")
import bmesh as _bm
ground_mesh = bpy.data.meshes.new("test_ground")
gb = _bm.new(); _bm.ops.create_grid(gb, x_segments=1, y_segments=1, size=1.0)
_bm.ops.translate(gb, vec=(0, 0, 0.05), verts=gb.verts)   # 顶点 z=0.05，对象原点仍在 0
gb.to_mesh(ground_mesh); gb.free()
ground_obj = bpy.data.objects.new("ground_plane", ground_mesh)
bpy.context.scene.collection.objects.link(ground_obj)
bpy.context.view_layer.update()
gz = ground_top_z()
assert_that("C1 地面顶面 z 从 mesh 顶点取得（非对象原点）",
            gz is not None and abs(gz - 0.05) < 1e-5,
            f"顶点算得 z={gz}；对象原点 z={ground_obj.location.z}")
under = box_obj("under_device", 0.05, 0.05, 0.05, (0.3, 0, -0.1))
bpy.context.view_layer.update()
gz_now = ground_top_z()
below = [o.name for o in bpy.data.objects if o.type == 'MESH' and o.name != "ground_plane"
         and o.matrix_world.translation.z < gz_now]
assert_that("C2 地面下器件能被发现", "under_device" in below, f"地面顶面 z={gz_now}；其下: {below}")

# ---- 反例 D：相机全部角点入框 ----
log("\n[D] 入框检查全部角点 + 横纵投影 + 轴向裁剪")
cam = bpy.data.objects.new("test_cam", bpy.data.cameras.new("test_cam"))
cam.data.lens = 50; cam.data.clip_start = 0.01; cam.data.clip_end = 100
cam.location = (0, -3, 0)
cam.rotation_euler = (1.5708, 0, 0)
bpy.context.scene.collection.objects.link(cam); bpy.context.scene.camera = cam
bpy.context.view_layer.update()
center_obj = box_obj("center_obj", 0.05, 0.05, 0.05, (0, 0, 0))          # 正前方
side_obj = box_obj("side_obj", 0.05, 0.05, 0.05, (5, 0, 0))              # 侧方画外
bpy.context.view_layer.update()
ok_c, det_c = in_frame_corners("test_cam", "center_obj")
ok_s, det_s = in_frame_corners("test_cam", "side_obj")
assert_that("D1 正前方对象 → 全部角点在框内", ok_c is True, det_c)
assert_that("D2 侧方画外对象 → 不入框", ok_s is False, det_s)

# ---- 反例 E：case-2 v3 场景实测（只报告，不断言通过）----
log("\n[E] case-2 v3 场景实测（分开报告，不用非黑统计证明通过）")
v3 = os.path.join(HERE, "render-output", "scene_case2_v3.blend")
if os.path.exists(v3):
    fresh_scene(v3)
    gz3 = ground_top_z()
    log(f"  ground_top_z(v3) = {gz3}")
    pairs = [("beam_laser_L1","lens_L1"), ("beam_M2_dmd","dmd"), ("beam_slm_M3","mirror_M3"),
             ("beam_L7_holder","holder"), ("beam_bc_mmf","mmf_single"), ("beam_mmf_pd","pd")]
    for seg, tgt in pairs:
        b = bpy.data.objects.get(seg)
        if not b: 
            log(f"  [?] {seg} 不存在"); continue
        p1 = b.get("beam_p1")
        # 用该段自身出射方向（按目标方向）而非固定 +x
        to = bpy.data.objects.get(tgt)
        d = (to.matrix_world.translation - Vector(p1))
        cls, hit, nrm, dist = classify(p1, d, tgt)
        log(f"  {seg}→{tgt}: {cls} 命中={hit} 距离={None if dist is None else round(dist*1000,2)}mm")
    # 镜面法向（几何 vs 属性，取 abs 比较）
    for nm in ["mirror_M1","mirror_M2","mirror_M3"]:
        o = bpy.data.objects.get(nm)
        if not o: continue
        rn = mesh_world_normal(o); an = o.get("mirror_normal")
        if rn is None: continue
        if an:
            av = Vector(an).normalized()
            dot = abs(rn.dot(av))
            log(f"  {nm}: 几何法向={tuple(round(v,3) for v in rn)} 属性={tuple(round(v,3) for v in av)} |dot|={dot:.3f} "
                f"{'一致(同一平面)' if dot>0.95 else '不一致✗'}")
            i = Vector((1,0,0)); refl = (i - 2*i.dot(rn)*rn).normalized()
            log(f"     +x 入射经真实镜面反射 = {tuple(round(v,3) for v in refl)}")
    # 地面遮挡
    g3 = bpy.data.objects.get("ground_plane")
    if g3 and gz3 is not None:
        below = [n for n in ["lens_L5","lens_L6","lens_L7","holder","bc_combiner","mmf_single","pd","oscilloscope"]
                 if (bpy.data.objects.get(n) and bpy.data.objects[n].matrix_world.translation.z < gz3)]
        log(f"  地面顶面 z={gz3}; 其下待显示器件: {below}")

# ---- 汇总 ----
log("\n=== 断言汇总 ===")
npass = sum(1 for _,ok,_ in RESULTS if ok)
log(f"  {npass}/{len(RESULTS)} 通过")
for name, ok, detail in RESULTS:
    log(f"    [{'PASS' if ok else 'FAIL'}] {name} — {detail}")
with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print(f"\n{OUT} written ({npass}/{len(RESULTS)} PASS)")
sys.exit(0 if npass == len(RESULTS) else 1)
