import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v12.blend")
for nm in ['cav_outer','cuo_lining','sapph_flange','sapph_seat_ring','sapph_window']:
    o=bpy.data.objects.get(nm)
    b=[o.matrix_world @ mathutils.Vector((v.co.x,v.co.y,v.co.z)) for v in o.data.vertices]
    print(f"  {nm}: x∈[{min(v.x for v in b):.4f},{max(v.x for v in b):.4f}]")
# 铜管末端端面在 x=-0.1600, 内衬末端在 x=-0.1584(比铜管末端多 1.6mm 伸向腔内)
# 镜盘/承座环若要嵌入铜管末端, 需在 x=-0.1600 以内(腔内侧)
