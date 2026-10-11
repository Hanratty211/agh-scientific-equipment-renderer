import bpy, mathutils, math, bmesh
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v11.blend")
sc=bpy.context.scene; deps=bpy.context.evaluated_depsgraph_get()
def inter_vol(A,B):
    t1=bpy.data.objects.new('A',A.data.copy()); sc.collection.objects.link(t1); t1.matrix_world=A.matrix_world
    t2=bpy.data.objects.new('B',B.data.copy()); sc.collection.objects.link(t2); t2.matrix_world=B.matrix_world
    md=t1.modifiers.new('b','BOOLEAN'); md.operation='INTERSECT'; md.object=t2
    bpy.context.view_layer.objects.active=t1; bpy.ops.object.modifier_apply(modifier='b')
    bm=bmesh.new(); bm.from_mesh(t1.data); v=abs(bm.calc_volume()); bm.free()
    bpy.data.objects.remove(t2,do_unlink=True); bpy.data.objects.remove(t1,do_unlink=True)
    return v*1e9
sap=bpy.data.objects['sapph_window']
pairs=[('sapph_window','cav_outer'), ('sapph_window','cuo_lining'), ('sapph_window','sapph_flange')]
print("=== 镜盘 vs 相邻部件实体相交(mm³) ===")
for a,b in pairs:
    ob=bpy.data.objects.get(b)
    if ob is None: print(f"  {a} ∩ {b}: 对象缺失"); continue
    print(f"  {a} ∩ {b}: {inter_vol(bpy.data.objects[a],ob):.3f} mm³")
# 镜盘 bbox
b=[sap.matrix_world @ mathutils.Vector((v.co.x,v.co.y,v.co.z)) for v in sap.data.vertices]
print(f"镜盘 x 范围=[{min(v.x for v in b):.4f},{max(v.x for v in b):.4f}]  铜管末端/cuo_lining 末端 x 需核对")
# 铜管末端位置
for nm in ['cav_outer','cuo_lining']:
    o=bpy.data.objects.get(nm)
    if o:
        bb=[o.matrix_world @ mathutils.Vector((v.co.x,v.co.y,v.co.z)) for v in o.data.vertices]
        print(f"  {nm}: x∈[{min(v.x for v in bb):.4f},{max(v.x for v in bb):.4f}]")
