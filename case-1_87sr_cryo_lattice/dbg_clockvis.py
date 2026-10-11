import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v7.blend")
scene=bpy.context.scene
deps=bpy.context.evaluated_depsgraph_get()
# clock beam 从 (0,0,0.1035) 垂直下到镜面(0,0,0.02). 顶壁外表面 z=0.075.
# cam_port_top 在 (0.02,-0.055,0.095) look_at (0,0,0.03): 看镜面
# 钟光束是否被顶壁实体遮挡? 射线 cam->clock_bm 中段(0,0,0.06)
def bb(name):
    o=bpy.data.objects.get(name)
    b=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    lo=mathutils.Vector((min(v[i] for v in b) for i in range(3)))
    hi=mathutils.Vector((max(v[i] for v in b) for i in range(3)))
    return lo,hi
lo,hi=bb('clock_bm')
print("clock_bm bbox:",[round(v,3) for v in lo],[round(v,3) for v in hi])
cam=bpy.data.objects['cam_port_top']
pt=mathutils.Vector((0.0,0.0,0.06))  # 光束中段(顶壁附近)
d=(pt-cam.location).normalized()
hit,loc,nrm,idx,ob,_=scene.ray_cast(deps, cam.location, d)
print(f"cam_port_top -> clock_bm中段(0,0,0.06): 先命中 '{ob.name if ob else None}'")
pt2=mathutils.Vector((0.0,0.0,0.02))
d2=(pt2-cam.location).normalized()
hit2,loc2,nrm2,idx2,ob2,_=scene.ray_cast(deps, cam.location, d2)
print(f"cam_port_top -> 镜面(0,0,0.02): 先命中 '{ob2.name if ob2 else None}'")
# clock beam emission 是否够亮? 打印材料
m=bpy.data.materials.get('clock_bm')
b=m.node_tree.nodes.get("Principled BSDF")
print("clock_bm emission:", b.inputs["Emission Color"].default_value, "strength:", b.inputs["Emission Strength"].default_value)
