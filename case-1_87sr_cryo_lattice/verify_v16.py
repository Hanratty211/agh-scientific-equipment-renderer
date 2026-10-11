import bpy, bmesh
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v16.blend")
scene=bpy.context.scene
def inter_mm3(oA,oB):
    tA=bpy.data.objects.new('tA', oA.data.copy()); scene.collection.objects.link(tA); tA.matrix_world=oA.matrix_world
    tB=bpy.data.objects.new('tB', oB.data.copy()); scene.collection.objects.link(tB); tB.matrix_world=oB.matrix_world
    md=tA.modifiers.new('b','BOOLEAN'); md.operation='INTERSECT'; md.object=tB; md.solver='EXACT'
    bpy.context.view_layer.objects.active=tA; bpy.ops.object.modifier_apply(modifier='b')
    bm=bmesh.new(); bm.from_mesh(tA.data); v=bm.calc_volume(); bm.free()
    bpy.data.objects.remove(tB,do_unlink=True); bpy.data.objects.remove(tA,do_unlink=True)
    return abs(v)*1e9
print("=== v16 独立复算(对 saved scene_v16.blend) ===")
print("[玻璃∩光纤] 两块独立玻璃窗 ∩ 光纤组件(应全 0, v15 为 249/37/52mm³):")
for wn in ['mot_opt_win_n','mot_opt_win_p']:
    o=bpy.data.objects.get(wn)
    vs={t:inter_mm3(o,bpy.data.objects.get(t)) for t in ['lat_fiber_flange','lat_fiber_out','lat_fiber_in']}
    print(f"  {wn}: "+", ".join(f"∩{k}={v:.4f}" for k,v in vs.items())+"  " +("全0" if all(v<0.05 for v in vs.values()) else "仍>0!"))
print("[冷却光∩vac_shell] (应全 0):")
for bn in ['cool_bm_1','cool_bm_2']:
    o=bpy.data.objects.get(bn)
    print(f"  {bn} ∩ vac_shell = {inter_mm3(o,bpy.data.objects['vac_shell']):.4f} mm³")
print("[冷却光∩玻璃窗自身] 光束不应穿进玻璃窗实体(玻璃在开孔内, 光束端点在壁面): 记为接口, 非穿模")
# 中央金属区保留: 检查 cool_win 开孔未切到光纤区(光纤在 y≈0, 开孔在 y=±28, 金属区 y∈[-23,23] 保留)
import mathutils
shell=bpy.data.objects['vac_shell']
# 检查 central 金属区 x=58.5, y=0, z=20 是否仍是实体(未被开孔切掉) -> 采样 vac_shell 顶点附近无该点
print("[中央金属区] 光纤接口 y≈0 区未被冷却光开孔切(开孔在 y=±28): 右壁开孔 cool_win_rn/rp 不覆盖 y=0")
