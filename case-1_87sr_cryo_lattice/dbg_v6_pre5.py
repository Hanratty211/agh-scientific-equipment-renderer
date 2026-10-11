import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v5.blend")
deps=bpy.context.evaluated_depsgraph_get()
scene=bpy.context.scene
cam2=bpy.data.objects['cam_port_top']
# cam2 朝 look_at 方向: 脚本里 look_at=(0.010, 0.0, CLK_TOP_Z+0.01) ≈ (0.010,0,0.08)
d = mathutils.Vector((0.010, 0.0, 0.08)) - cam2.matrix_world.translation
hit,loc,nrm,idx,ob,_=scene.ray_cast(deps, cam2.matrix_world.translation, d.normalized())
print("cam_port_top 朝 look_at(0.010,0,0.08): 先命中", ob.name if ob else None,
      "loc" , [round(v,3) for v in loc] if hit else None)
# 顶壁 z=0.075, cam z=0.133 在顶壁上方，往下看应该命中 clock_bm/镜/壁，检查是否被大物体遮挡
for probe in [mathutils.Vector((0.010,0.0,0.075)), mathutils.Vector((0.0,0.0,0.075)), mathutils.Vector((0.04,0.014,0.028))]:
    d2=probe-cam2.matrix_world.translation
    hit,loc,nrm,idx,ob,_=scene.ray_cast(deps, cam2.matrix_world.translation, d2.normalized())
    print(f"  probe {tuple(round(v,3) for v in probe)}: 先命中 {ob.name if ob else None}")
