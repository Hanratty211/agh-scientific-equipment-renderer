import bpy, mathutils, math, bmesh
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v11.blend")
sc=bpy.context.scene; deps=bpy.context.evaluated_depsgraph_get()
def inter(a,b):
    t1=bpy.data.objects.new('A',a.data.copy()); sc.collection.objects.link(t1); t1.matrix_world=a.matrix_world
    t2=bpy.data.objects.new('B',b.data.copy()); sc.collection.objects.link(t2); t2.matrix_world=b.matrix_world
    md=t1.modifiers.new('b','BOOLEAN'); md.operation='INTERSECT'; md.object=t2
    bpy.context.view_layer.objects.active=t1; bpy.ops.object.modifier_apply(modifier='b')
    bm=bmesh.new(); bm.from_mesh(t1.data); v=abs(bm.calc_volume()); bm.free()
    bpy.data.objects.remove(t2,do_unlink=True); bpy.data.objects.remove(t1,do_unlink=True)
    return v*1e9
print("v11 实际对象: 镜盘∩ 各相邻部件")
sap=bpy.data.objects['sapph_window']
for nm in ['cav_outer','cuo_lining','sapph_flange']:
    o=bpy.data.objects.get(nm)
    print(f"  镜盘 ∩ {nm}: {inter(sap,o):.3f} mm³")
# 铜管末端 x 端面位置 vs 镜盘 x 范围
b=[sap.matrix_world @ mathutils.Vector((v.co.x,v.co.y,v.co.z)) for v in sap.data.vertices]
print(f"镜盘 x∈[{min(v.x for v in b):.4f},{max(v.x for v in b):.4f}]")
