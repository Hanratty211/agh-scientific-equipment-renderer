import bpy, bmesh
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v13.blend")
scene=bpy.context.scene
def inter_mm3(oA,oB):
    # 与 build 脚本 _solid_inter_mm3 完全一致: 对象拷贝 + 布尔 INTERSECT + bmesh.calc_volume
    tA=bpy.data.objects.new('tA', oA.data.copy()); scene.collection.objects.link(tA); tA.matrix_world=oA.matrix_world
    tB=bpy.data.objects.new('tB', oB.data.copy()); scene.collection.objects.link(tB); tB.matrix_world=oB.matrix_world
    md=tA.modifiers.new('b','BOOLEAN'); md.operation='INTERSECT'; md.object=tB; md.solver='EXACT'
    bpy.context.view_layer.objects.active=tA; bpy.ops.object.modifier_apply(modifier='b')
    bm=bmesh.new(); bm.from_mesh(tA.data); v=bm.calc_volume(); bm.free()
    bpy.data.objects.remove(tB,do_unlink=True); bpy.data.objects.remove(tA,do_unlink=True)
    return abs(v)*1e9
pairs=[('sapph_window','cav_outer'),('sapph_window','cuo_lining'),('sapph_window','sapph_seat_ring'),
       ('sapph_seat_ring','cav_outer'),('sapph_seat_ring','cuo_lining'),('sapph_seat_ring','sapph_flange'),
       ('cool_bm_1','cav_outer'),('cool_bm_1','cuo_lining'),('cool_bm_1','mot_coil_R'),
       ('cool_bm_2','cav_outer'),('cool_bm_2','cuo_lining'),('cool_bm_2','mot_coil_L'),
       ('cool_bm_4','cav_outer'),('cool_bm_4','cuo_lining')]
print("=== v13 实体相交体积(对 saved .blend, 用 build 同款 copy+boolean+calc_volume) ===")
bad=0
for a,b in pairs:
    if a not in bpy.data.objects or b not in bpy.data.objects:
        print(f"   {a} ∩ {b}: 对象缺失"); continue
    v=inter_mm3(bpy.data.objects[a],bpy.data.objects[b])
    tag='不穿透' if v<0.05 else ('接触fuzz' if v<0.06 else '穿透!')
    if v>=0.05: bad+=1
    print(f"   {a} ∩ {b} = {v:.3f} mm³  ({tag})")
print(f"=== 结果: {'全部 OK(无穿透)' if bad==0 else f'{bad} 对仍穿透, 需继续修'} ===")
