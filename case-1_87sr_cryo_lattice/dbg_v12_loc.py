import bpy, mathutils, math, bmesh
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v12.blend")
sc=bpy.context.scene
sw=bpy.data.objects['sapph_window']; li=bpy.data.objects['cuo_lining']
# 交集顶点位置
t1=bpy.data.objects.new('A',sw.data.copy()); sc.collection.objects.link(t1); t1.matrix_world=sw.matrix_world
t2=bpy.data.objects.new('B',li.data.copy()); sc.collection.objects.link(t2); t2.matrix_world=li.matrix_world
md=t1.modifiers.new('b','BOOLEAN'); md.operation='INTERSECT'; md.object=t2
bpy.context.view_layer.objects.active=t1; bpy.ops.object.modifier_apply(modifier='b')
xs=[v.co.x for v in t1.data.vertices]; ys=[v.co.y for v in t1.data.vertices]
print(f"镜盘∩内衬 交集 x∈[{min(xs):.4f},{max(xs):.4f}] (内衬末端 x=-0.1584, 镜盘中心 x={-0.160+0.0035:.4f})")
print(f"镜盘中心 x = { (min(v.x for v in [sw.matrix_world @ mathutils.Vector((v.co.x,v.co.y,v.co.z)) for v in sw.data.vertices]) + max(v.x for v in [sw.matrix_world @ mathutils.Vector((v.co.x,v.co.y,v.co.z)) for v in sw.data.vertices]))/2 :.4f}")
bpy.data.objects.remove(t2,do_unlink=True); bpy.data.objects.remove(t1,do_unlink=True)
