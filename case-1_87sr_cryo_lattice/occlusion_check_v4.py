import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v4.blend")
scene=bpy.context.scene
depsgraph=bpy.context.evaluated_depsgraph_get()
for cam_name in ['cam_overview','cam_cut']:
    cam=bpy.data.objects[cam_name]
    print(f"--- {cam_name} ---")
    for target in ['mot_coil_L','mot_coil_R','cav_outer','ap_ring','sapph_window']:
        o=bpy.data.objects.get(target)
        if not o: continue
        # 用对象的实际包围盒中心（不是 origin，因为 v3/v4 某些对象 origin 可能在原点）
        bb=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
        c=mathutils.Vector((min(v[i] for v in bb) for i in range(3)))
        c+= (mathutils.Vector((max(v[i] for v in bb) for i in range(3)))-c)/2
        hit,loc,nrm,idx,ob,_ = scene.ray_cast(depsgraph, cam.matrix_world.translation, (c-cam.matrix_world.translation).normalized())
        blocker = ob.name if ob and ob.name not in (target,) else None
        print(f"  {target:14s} {'BLOCKED by '+str(blocker) if blocker else 'clear'}")
