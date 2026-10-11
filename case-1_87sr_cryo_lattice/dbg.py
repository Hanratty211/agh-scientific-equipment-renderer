import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v4.blend")
for k in ['mot_coil_L','mot_coil_R','cav_outer','ap_ring','sapph_window','vac_shell']:
    o=bpy.data.objects.get(k)
    if o: print(k,[round(v,3) for v in o.matrix_world.translation])
cam=bpy.data.objects['cam_cut']
print('cam_cut loc',[round(v,3) for v in cam.location],'look_at used at build: CAV_X=-0.08, z=0.02')
