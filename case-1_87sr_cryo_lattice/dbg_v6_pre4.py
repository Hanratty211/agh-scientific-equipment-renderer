import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v5.blend")
deps=bpy.context.evaluated_depsgraph_get()
scene=bpy.context.scene

# 右壁局部: 检查 cam_port_right 视野内 lat_fiber_flange 是否被 mot_coil_R 或 vac_shell 挡
cam=bpy.data.objects['cam_port_right']
def bb(name):
    o=bpy.data.objects.get(name)
    if not o: return None,None
    b=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    lo=mathutils.Vector((min(v[i] for v in b) for i in range(3)))
    hi=mathutils.Vector((max(v[i] for v in b) for i in range(3)))
    return lo,hi
lo,hi=bb('lat_fiber_flange'); c=(lo+hi)/2
hit,loc,nrm,idx,ob,_=scene.ray_cast(deps, cam.matrix_world.translation, (c-cam.matrix_world.translation).normalized())
print("cam_port_right -> lat_fiber_flange: 先命中", ob.name if ob else None)

# 顶壁局部: cam_port_top 是否被什么挡
cam2=bpy.data.objects['cam_port_top']
lo,hi=bb('clock_top_hole')
if lo:
    c=(lo+hi)/2
    hit,loc,nrm,idx,ob,_=scene.ray_cast(deps, cam2.matrix_world.translation, (c-cam2.matrix_world.translation).normalized())
    print("cam_port_top -> clock_top_hole 中心:", ob.name if ob else None, "loc", [round(v,3) for v in loc] if hit else None)
# 顶壁局部几乎全灰的原因: cam_port_top loc 检查
print("cam_port_top loc:", [round(v,3) for v in cam2.location], "lens", cam2.data.lens)
# 从 cam_port_top 向场景中心发射射线看是否命中什么大面积物体
hit,loc,nrm,idx,ob,_=scene.ray_cast(deps, cam2.matrix_world.translation, mathutils.Vector((-0.01,0,0.05)-mathutils.Vector(cam2.location)).normalized())
print("cam_port_top -> 场景中心方向: 先命中", ob.name if ob else None)
