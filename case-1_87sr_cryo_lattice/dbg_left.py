import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v5.blend")
scene=bpy.context.scene
deps=bpy.context.evaluated_depsgraph_get()
cam_pos = mathutils.Vector((-0.24, 0.0, 0.02))   # 从铜腔左端更外侧一点看
targets = {'cav_outer':(-0.16,0.0,0.02), 'sapph_window':(-0.162,0.0,0.02)}
for name,pt in targets.items():
    o=bpy.data.objects.get(name)
    bb=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    c=(mathutils.Vector((min(v[i] for v in bb) for i in range(3))) +
       mathutils.Vector((max(v[i] for v in bb) for i in range(3))))/2
    hit,loc,nrm,idx,ob,_ = scene.ray_cast(deps, cam_pos, (c-cam_pos).normalized())
    print(f"{name}: ray from x=-0.24 hits '{ob.name if ob else None}' first (目标本体={name})")
# 同时确认左壁是否有实体挡在 cav 左端与 -x 方向观察者之间
shell=bpy.data.objects['vac_shell']
bb=[shell.matrix_world @ mathutils.Vector(c) for c in shell.bound_box]
sx_lo=min(v.x for v in bb)
print("vac_shell x_min =", round(sx_lo,4), " (cav 左端 -0.160 是否 < sx_lo?", -0.160<sx_lo, ")")
