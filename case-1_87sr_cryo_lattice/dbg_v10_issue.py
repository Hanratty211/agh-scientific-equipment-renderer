import bpy, mathutils, math, bmesh
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v10.blend")
sc=bpy.context.scene; deps=bpy.context.evaluated_depsgraph_get()
sw=bpy.data.objects['sapph_window']; fr=bpy.data.objects['sapph_flange']
def bmvol(me):
    bm=bmesh.new(); bm.from_mesh(me); v=bm.calc_volume(); bm.free(); return v
t1=bpy.data.objects.new('t_sw',sw.data.copy()); sc.collection.objects.link(t1); t1.matrix_world=sw.matrix_world
t2=bpy.data.objects.new('t_fr',fr.data.copy()); sc.collection.objects.link(t2); t2.matrix_world=fr.matrix_world
md=t1.modifiers.new('b','BOOLEAN'); md.operation='INTERSECT'; md.object=t2
bpy.context.view_layer.objects.active=t1; bpy.ops.object.modifier_apply(modifier='b')
print(f"sapph_window ∩ sapph_flange 顶点={len(t1.data.vertices)} 体积≈{abs(bmvol(t1.data))*1e9:.2f} mm³")
# 镜盘半径/法兰通孔
print(f"镜盘半径 SAPH_R≈{sw.data.vertices[0].co.length if sw.data.vertices else 0:.4f}; "
      f"法兰通孔半径 FR_HOLE_R=0.0054")
bpy.data.objects.remove(t2,do_unlink=True); bpy.data.objects.remove(t1,do_unlink=True)
