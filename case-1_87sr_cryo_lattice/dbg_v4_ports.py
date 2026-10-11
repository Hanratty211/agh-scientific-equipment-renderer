import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v4.blend")
def bb_center(name):
    o=bpy.data.objects.get(name)
    if not o: return None
    bb=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    lo=mathutils.Vector((min(v[i] for v in bb) for i in range(3)))
    hi=mathutils.Vector((max(v[i] for v in bb) for i in range(3)))
    return lo,hi
# 真空室壳体（已布尔切掉前壁+顶部前1/4）实际剩余占哪些空间
lo,hi=bb_center('vac_shell')
print('vac_shell bbox lo',[round(v,3) for v in lo],'hi',[round(v,3) for v in hi])
for k in ['lat_fiber','clock_bm','cool_bm_1','cool_bm_2','cool_bm_3','cool_bm_4','dichroic_mir','cav_outer','ap_ring','sapph_window']:
    r=bb_center(k)
    if r:
        lo,hi=r
        # 判断对象是否延伸到真空室外壳包围盒范围之外（x 方向）
        print(f"{k:14s} x∈[{lo.x:+.3f},{hi.x:+.3f}]  y∈[{lo.y:+.3f},{hi.y:+.3f}]  z∈[{lo.z:+.3f},{hi.z:+.3f}]")
