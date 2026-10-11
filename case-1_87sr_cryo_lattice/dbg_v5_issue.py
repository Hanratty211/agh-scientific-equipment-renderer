import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v5.blend")
scene=bpy.context.scene
deps=bpy.context.evaluated_depsgraph_get()

def bb(name):
    o=bpy.data.objects.get(name)
    if not o: return None,None
    b=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    lo=mathutils.Vector((min(v[i] for v in b) for i in range(3)))
    hi=mathutils.Vector((max(v[i] for v in b) for i in range(3)))
    return lo,hi

print("=== 1. 铜腔 vs 左壁 轴线高度不一致 ===")
lo,hi = bb('cav_outer')
print(f"cav_outer z range: [{lo.z:+.4f},{hi.z:+.4f}]  axis z={(lo.z+hi.z)/2:+.4f}")
lo2,hi2 = bb('vac_shell')
# 左壁位置 x=-0.14
print(f"vac_shell x range: [{lo2.x:+.3f},{hi2.x:+.3f}]")
# 铜腔轴线 z=0.02，左壁窗口（port_left）在 z 哪里？
# 检查现有端口开孔位置
for k in ['win_left','port_left']:
    lo3,hi3 = bb(k) if k in bpy.data.objects else (None,None)
    if lo3: print(f"{k} x[{lo3.x:+.3f},{hi3.x:+.3f}] y[{lo3.y:+.3f},{hi3.y:+.3f}] z[{lo3.z:+.3f},{hi3.z:+.3f}]")

print("\n=== 2. 铜腔左端是否真的穿过左壁（管壁 z 范围 vs 左壁开孔 z 范围） ===")
# 铜腔左端 x=-0.160，左壁 x=-0.140..-0.137 (壁厚3mm)
# 铜腔轴线 z=0.020；左壁 port_left 窗口在哪里？
# 从 x=-0.20 向 +x 发射射线，在铜腔轴线高度 z=0.02, y=0
hit,loc,nrm,idx,ob,_ = scene.ray_cast(deps, mathutils.Vector((-0.20,0.0,0.020)), mathutils.Vector((1,0,0)))
print(f"从(-0.20,0,0.02)向+x射线: 先命中 '{ob.name if ob else None}' loc={[round(v,3) for v in (loc if hit else [])]}")
# 铜腔管壁与左壁金属是否相交：检查 (x=-0.14, y=0, z=0.02) 点是否同时在两个物体里
import mathutils as mu
p = mathutils.Vector((-0.140, 0.0, 0.020))
# 用 BVH 判定
for objname in ['cav_outer','vac_shell']:
    o=bpy.data.objects.get(objname)
    if not o: continue
    # 世界坐标转局部
    lp = o.matrix_world.inverted() @ p
    found=False
    bvh = o.evaluated_get(deps).data  # 已含修改器
    # 简单包围盒检查
    lb=[bvh.bound_box[i] for i in range(8)]
    lo4=mu.Vector((min(v[i] for v in lb) for i in range(3)))
    hi4=mu.Vector((max(v[i] for v in lb) for i in range(3)))
    inside = all(lo4[i]<=lp[i]<=hi4[i] for i in range(3))
    print(f"  点(-0.140,0,0.020) 在 {objname} 局部包围盒内? {inside}")

print("\n=== 3. 钟光路径（v5 实际位置） ===")
for k in ['clock_bm','clock_bm_2','clock_bm_3','dichroic_mir','clock_top_hole']:
    lo,hi=bb(k)
    if lo: print(f"{k:16s} x[{lo.x:+.3f},{hi.x:+.3f}] y[{lo.y:+.3f},{hi.y:+.3f}] z[{lo.z:+.3f},{hi.z:+.3f}]")
# 二向色镜朝向：rotation
o=bpy.data.objects.get('dichroic_mir')
if o: print(f"dichroic_mir rotation_euler (度): {[round(math.degrees(v),1) for v in o.rotation_euler]}")

print("\n=== 4. 右壁局部图被谁遮挡（cam_port_right 位置） ===")
cam=bpy.data.objects['cam_port_right']
print(f"cam_port_right loc: {[round(v,3) for v in cam.location]}  lens {cam.data.lens}")
# 从 cam 向 lat_fiber_flange 中心发射射线
lo,hi=bb('lat_fiber_flange')
c=(lo+hi)/2
hit,loc,nrm,idx,ob,_=scene.ray_cast(deps, cam.matrix_world.translation, (c-cam.matrix_world.translation).normalized())
print(f"cam_port_right -> lat_fiber_flange 中心: 先命中 '{ob.name if ob else None}'")
