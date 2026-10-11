import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v3.blend")
scene=bpy.context.scene
ray=bpy.context.scene.raycaster if hasattr(bpy.context.scene,'raycaster') else None
import math
# 用 BVH 射线检测：对每个相机→目标连线，检测是否有实体遮挡
depsgraph=bpy.context.evaluated_depsgraph_get()
for cam_name in ['cam_overview','cam_cavity','cam_cut']:
    cam=bpy.data.objects[cam_name]
    print(f"--- {cam_name} ---")
    for target in ['mot_coil_L','mot_coil_R','cav_outer','ap_ring','sapph_window']:
        o=bpy.data.objects.get(target)
        if not o: continue
        c=o.matrix_world.translation
        orig=c.copy()
        c=cam.matrix_world.translation
        hit,loc,nrm,idx,ob,_ = scene.ray_cast(depsgraph, c, (o.matrix_world.translation-c).normalized())
        blocker = ob.name if ob and ob.name not in (target,) else None
        print(f"  {target:14s} {'BLOCKED by '+blocker if blocker else 'clear'}")
