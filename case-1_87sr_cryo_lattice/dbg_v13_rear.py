import bpy, mathutils, math
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v13.blend")
V=lambda o:[bpy.data.objects[o].matrix_world @ mathutils.Vector((v.co.x,v.co.y,v.co.z)) for v in bpy.data.objects[o].data.vertices]
for cn in ['cav_outer','cuo_lining','sapph_flange','sapph_seat_ring','sapph_window']:
    try:
        w=V(cn); r=lambda L: (max(v[L] for v in w)-min(v[L] for v in w))
        import math
        cx=math.sqrt(max(v.y**2+(v.z-0.02)**2 for v in w))
        print(f"  {cn}: x∈[{min(v.x for v in w)*1e3:.1f},{max(v.x for v in w)*1e3:.1f}] 最大径向={cx*1e3:.2f}mm")
    except Exception as e: print(cn,"err",e)
def inter(a,b):
    for m in [bpy.data.objects[a].modifiers]:
        if m.type=='BOOLEAN': m.operation='INTERSECT'; m.object=bpy.data.objects[b]; m.solver='EXACT'
    dg=bpy.context.evaluated_depsgraph_get(); m=bpy.data.objects[a].evaluated_get(dg)
    w=[m.matrix_world @ mathutils.Vector((v.co.x,v.co.y,v.co.z)) for v in m.data.vertices]
    if not w: return 0.0
    from mathutils import BBox
    bb=mathutils.geometry.bounding_box(w)
    vol=0.0
    xs=sorted(set(round(v.x,5) for v in w))
    import math as M
    # 粗略: 顶点数*特征
    return len(w)
for a,b in [('sapph_seat_ring','cav_outer'),('sapph_seat_ring','sapph_flange'),('sapph_window','cav_outer'),('sapph_window','sapph_seat_ring')]:
    print(f"  {a} ∩ {b}: {inter(a,b)} 顶点")
