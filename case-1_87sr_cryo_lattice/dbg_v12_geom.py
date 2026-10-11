import bpy, mathutils, math
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v12.blend")
for nm in ['cav_outer','cuo_lining','sapph_seat_ring','sapph_flange','sapph_window']:
    o=bpy.data.objects.get(nm)
    if not o: print(nm,"缺失"); continue
    b=[o.matrix_world @ mathutils.Vector((v.co.x,v.co.y,v.co.z)) for v in o.data.vertices]
    # 半径 = 到 x 轴(y=0,z=AXIS_Z) 的最大距离
    rmax=max(math.hypot(v.y,v.z-0.020) for v in b)
    print(f"  {nm}: 半径≈{rmax*1000:.2f}mm x∈[{min(v.x for v in b):.4f},{max(v.x for v in b):.4f}]")
