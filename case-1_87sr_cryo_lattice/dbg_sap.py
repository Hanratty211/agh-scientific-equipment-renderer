import bpy, mathutils, math, bmesh
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v11.blend")
sc=bpy.context.scene; deps=bpy.context.evaluated_depsgraph_get()
sw=bpy.data.objects['sapph_window']; fr=bpy.data.objects['sapph_flange']
b=[sw.matrix_world @ mathutils.Vector((v.co.x,v.co.y,v.co.z)) for v in sw.data.vertices]
AX=0.02
rmax=max(math.hypot(v.y,v.z-AX) for v in b)
print(f"镜盘实体外缘(距轴最远)={rmax*1000:.2f} mm; 法兰通孔半径=5.4mm")
t1=bpy.data.objects.new('a',sw.data.copy()); sc.collection.objects.link(t1); t1.matrix_world=sw.matrix_world
t2=bpy.data.objects.new('b',fr.data.copy()); sc.collection.objects.link(t2); t2.matrix_world=fr.matrix_world
md=t1.modifiers.new('b','BOOLEAN'); md.operation='INTERSECT'; md.object=t2
bpy.context.view_layer.objects.active=t1; bpy.ops.object.modifier_apply(modifier='b')
bm=bmesh.new(); bm.from_mesh(t1.data); vol=abs(bm.calc_volume()); bm.free()
print(f"镜盘∩法兰 INTERSECT = {len(t1.data.vertices)} 顶点 {vol*1e9:.3f} mm³")
zc=sorted(set(round(v.co.z,4) for v in t1.data.vertices))
if zc: print(f"  交集顶点 z 范围=[{zc[0]:.4f},{zc[-1]:.4f}]")
bpy.data.objects.remove(t2,do_unlink=True); bpy.data.objects.remove(t1,do_unlink=True)
