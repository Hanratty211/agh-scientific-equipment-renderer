import bpy, mathutils, math
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v12.blend")
for nm in ['cuo_lining','ap_ring','sapph_window','sapph_seat_ring','interrogation_vol']:
    o=bpy.data.objects.get(nm)
    if not o: print(f"  {nm}: 缺失"); continue
    b=[o.matrix_world @ mathutils.Vector((v.co.x,v.co.y,v.co.z)) for v in o.data.vertices]
    rmax=max(math.hypot(v.y,v.z-0.020) for v in b)
    print(f"  {nm}: x∈[{min(v.x for v in b):.4f},{max(v.x for v in b):.4f}] 半径≈{rmax*1000:.2f}mm")
