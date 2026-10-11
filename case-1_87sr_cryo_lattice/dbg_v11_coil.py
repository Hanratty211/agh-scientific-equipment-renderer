import bpy
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v11.blend")
for n in ['mot_coil_L','mot_coil_R','mot_coil_L_display']:
    o=bpy.data.objects.get(n)
    print(f"{n}: 顶点={len(o.data.vertices)} hide_render={o.hide_render}")
print("总览可见主线圈:", not bpy.data.objects['mot_coil_L'].hide_render,
      "| 展示副本(默认隐藏):", bpy.data.objects['mot_coil_L_display'].hide_render)
