import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v6.blend")
scene=bpy.context.scene
deps=bpy.context.evaluated_depsgraph_get()

def bb(name):
    o=bpy.data.objects.get(name)
    if not o: return None
    b=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    lo=mathutils.Vector((min(v[i] for v in b) for i in range(3)))
    hi=mathutils.Vector((max(v[i] for v in b) for i in range(3)))
    return lo,hi

print("=== 1. 左壁穿腔窗口高度 vs 铜腔轴线 ===")
lo,hi=bb('cav_outer')
print("cav_outer 轴线 z =", round((lo.z+hi.z)/2,4))
lo2,hi2=bb('win_left')
print("win_left z range:", [round(v,3) for v in (lo2.z,hi2.z)], "中心 z =", round((lo2.z+hi2.z)/2,4))

print("\n=== 2. 铜腔管壁与左壁金属是否相交（无碰撞 vs 仅可见 区分） ===")
o=bpy.data.objects['cav_outer']; oev=o.evaluated_get(deps); me=oev.data
inside=[]
for v in me.vertices:
    w=oev.matrix_world @ v.co
    if -0.142<=w.x<=-0.135 and abs(w.y)<=0.0066 and abs(w.z-0.020)<=0.0066:
        inside.append((round(w.x,4),round(w.y,4),round(w.z,4)))
print("cav_outer 顶点落在左壁薄壳(x∈[-0.142,-0.135], 铜腔半径内)的数量:", len(inside))
# 左壁薄壳在此 x 段是否仍有实体金属（开孔后）
o2=bpy.data.objects['vac_shell']; o2ev=o2ev2=o2.evaluated_get(deps); me2=o2ev2.data
wall_pts=[v for v in me2.vertices if -0.142<=(o2ev2.matrix_world @ v.co).x<=-0.135]
print("vac_shell 左壁薄壳(x∈[-0.142,-0.135]) 顶点总数:", len(wall_pts))
# 射线: 铜腔轴线高度从外侧看
hit,loc,nrm,idx,ob,_=scene.ray_cast(deps, mathutils.Vector((-0.20,0.0,0.020)), mathutils.Vector((1,0,0)))
print("从(-0.20,0,0.02)向+x: 先命中", ob.name if ob else None, "loc", [round(v,3) for v in loc] if hit else None)

print("\n=== 3. 钟光路径: 入射/出射是否首尾相接于二向色镜中心 ===")
for k in ['clock_bm','dichroic_mir','clock_bm_3']:
    lo,hi=bb(k)
    c=(lo+hi)/2
    print(f"  {k:14s} 中心={[round(v,4) for v in c]}")
o=bpy.data.objects['dichroic_mir']
import math
print("  dichroic_mir rot(deg):", [round(math.degrees(v),1) for v in o.rotation_euler])

print("\n=== 4. 局部图视角: cam_port_right/cam_port_top/cam_cavo 是否对准目标且不被光束遮挡 ===")
def ray_to(cam_name, tgt):
    cam=bpy.data.objects[cam_name]
    lo,hi=bb(tgt); c=(lo+hi)/2
    d=(c-cam.matrix_world.translation).normalized()
    hit,loc,nrm,idx,ob,_=scene.ray_cast(deps, cam.matrix_world.translation, d)
    first=ob.name if ob else None
    return first, c
for cam_name,tgt in [('cam_port_right','lat_fiber_flange'),('cam_port_top','clock_top_hole'),('cam_cavo','ap_ring')]:
    first,c=ray_to(cam_name,tgt)
    print(f"  {cam_name} -> {tgt}: 先命中 '{first}'  目标中心={[round(v,3) for v in c]}")
    # 是否被粗光束先命中
    if first and first.startswith(('lat_beam','cool_bm')):
        print("     ** 仍被粗光束遮挡, 局部图可能仍不合格")
    elif first in (None, tgt, 'cav_outer','vac_shell','sapph_window','cuo_lining','interrogation_vol'):
        print("     OK (先命中目标本体或同区域结构)")

print("\n=== 5. 视锥: cam_cavo 下 隔膜通孔/内壁/探测区/后窗 是否入框 ===")
cam=bpy.data.objects['cam_cavo']; lens=cam.data.lens; SW=18.0
for tgt in ['ap_ring','interrogation_vol','sapph_window','cav_outer']:
    lo,hi=bb(tgt); c=(lo+hi)/2
    m=cam.matrix_world.inverted(); p=m @ c
    if p.z>0: print(f"  cam_cavo -> {tgt}: BEHIND"); continue
    nx=(p.x/abs(p.z))*(lens/SW*0.5)
    print(f"  cam_cavo -> {tgt:18s} nx={nx:+.2f} in_x={abs(nx)<0.5}")
