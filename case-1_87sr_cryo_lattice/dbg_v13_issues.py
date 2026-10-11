import bpy, mathutils, math, bmesh
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v12.blend")
sc=bpy.context.scene; deps=bpy.context.evaluated_depsgraph_get()
def inter_vol(a,b):
    if a is None or b is None: return None
    t1=bpy.data.objects.new('A',a.data.copy()); sc.collection.objects.link(t1); t1.matrix_world=a.matrix_world
    t2=bpy.data.objects.new('B',b.data.copy()); sc.collection.objects.link(t2); t2.matrix_world=b.matrix_world
    md=t1.modifiers.new('b','BOOLEAN'); md.operation='INTERSECT'; md.object=t2
    bpy.context.view_layer.objects.active=t1; bpy.ops.object.modifier_apply(modifier='b')
    bm=bmesh.new(); bm.from_mesh(t1.data); v=abs(bm.calc_volume()); bm.free()
    bpy.data.objects.remove(t2,do_unlink=True); bpy.data.objects.remove(t1,do_unlink=True)
    return v*1e9
print("=== 问题1: 冷却光束 vs 铜管/内衬/线圈 实体相交(mm³) ===")
for cn in ['cool_bm_1','cool_bm_2','cool_bm_3','cool_bm_4']:
    cb=bpy.data.objects.get(cn)
    for target in ['cav_outer','cuo_lining','mot_coil_L','mot_coil_R']:
        o=bpy.data.objects.get(target)
        v=inter_vol(cb,o)
        if v is not None and v>0.01:
            print(f"  {cn} ∩ {target}: {v:.2f} mm³")
print("=== 问题4: 内衬/铜管 范围 ===")
for nm in ['cuo_lining','cav_outer']:
    o=bpy.data.objects.get(nm)
    b=[o.matrix_world @ mathutils.Vector((v.co.x,v.co.y,v.co.z)) for v in o.data.vertices]
    print(f"  {nm}: x∈[{min(v.x for v in b)*1000:.1f},{max(v.x for v in b)*1000:.1f}] mm")
print("=== 问题2: 铜腔局部线圈遮挡 (检查 mot_coil_L_display 存在性与切割状态) ===")
disp=bpy.data.objects.get('mot_coil_L_display')
if disp: print(f"  mot_coil_L_display: {len(disp.data.vertices)} 顶点, hide_render={disp.hide_render}")
