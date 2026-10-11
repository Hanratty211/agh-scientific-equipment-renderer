import bpy, bmesh, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v13.blend")
scene=bpy.context.scene
def inter_mm3(oA,oB):
    tA=bpy.data.objects.new('tA', oA.data.copy()); scene.collection.objects.link(tA); tA.matrix_world=oA.matrix_world
    tB=bpy.data.objects.new('tB', oB.data.copy()); scene.collection.objects.link(tB); tB.matrix_world=oB.matrix_world
    md=tA.modifiers.new('b','BOOLEAN'); md.operation='INTERSECT'; md.object=tB; md.solver='EXACT'
    bpy.context.view_layer.objects.active=tA; bpy.ops.object.modifier_apply(modifier='b')
    bm=bmesh.new(); bm.from_mesh(tA.data); v=bm.calc_volume(); bm.free()
    bpy.data.objects.remove(tB,do_unlink=True); bpy.data.objects.remove(tA,do_unlink=True)
    return abs(v)*1e9
def zspan(o):
    W=[o.matrix_world @ mathutils.Vector(v.co) for v in o.data.vertices]
    return (min(v.z for v in W)*1e3, max(v.z for v in W)*1e3)
def yspan(o):
    W=[o.matrix_world @ mathutils.Vector(v.co) for v in o.data.vertices]
    return (min(v.y for v in W)*1e3, max(v.y for v in W)*1e3)
def xspan(o):
    W=[o.matrix_world @ mathutils.Vector(v.co) for v in o.data.vertices]
    return (min(v.x for v in W)*1e3, max(v.x for v in W)*1e3)
vac=bpy.data.objects['vac_shell']
print("=== vac_shell bbox ===")
print("  x",xspan(vac),"y",yspan(vac),"z",zspan(vac))
print("=== 冷却光 ∩ vac_shell (v13 实际布尔) ===")
for b in ['cool_bm_1','cool_bm_2','cool_bm_3','cool_bm_4']:
    o=bpy.data.objects[b]
    v=inter_mm3(o,vac)
    print(f"  {b} ∩ vac_shell = {v:.3f} mm³  光束x∈{xspan(o)} z∈{zspan(o)} y∈{yspan(o)}")
print("=== 窗口对象(玻璃) 位置 ===")
for w in ['win_top','win_right','mot_opt_win','mot_win_top','mot_win_bot']:
    o=bpy.data.objects.get(w)
    if o: print(f"  {w}: x∈{xspan(o)} y∈{yspan(o)} z∈{zspan(o)}")
    else: print(f"  {w}: 不存在")
