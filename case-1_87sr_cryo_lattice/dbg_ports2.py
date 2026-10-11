import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v4.blend")
scene=bpy.context.scene
deps=bpy.context.evaluated_depsgraph_get()

def bb(name):
    o=bpy.data.objects.get(name)
    if not o: return None,None
    bb=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    lo=mathutils.Vector((min(v[i] for v in bb) for i in range(3)))
    hi=mathutils.Vector((max(v[i] for v in bb) for i in range(3)))
    return lo,hi

lo,hi=bb('vac_shell')
print('vac_shell bbox: x',[round(lo.x,3),round(hi.x,3)],'y',[round(lo.y,3),round(hi.y,3)],'z',[round(lo.z,3),round(hi.z,3)])

# 关键检查对象：lat_fiber 是否伸入 vac_shell 的 x 范围
for k in ['lat_fiber','clock_bm','cool_bm_1','cool_bm_2','cool_bm_3','cool_bm_4']:
    lo2,hi2=bb(k)
    in_x = (lo2.x < hi.x) and (hi2.x > lo.x)
    print(f"{k:14s} x∈[{lo2.x:+.3f},{hi2.x:+.3f}]  y∈[{lo2.y:+.3f},{hi2.y:+.3f}]  z∈[{lo2.z:+.3f},{hi2.z:+.3f}]  x-overlaps-shell={in_x}")
