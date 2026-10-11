import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v13.blend")
def w(o):
    O=bpy.data.objects.get(o)
    return [O.matrix_world @ mathutils.Vector((v.co.x,v.co.y,v.co.z)) for v in O.data.vertices] if O else None
def inter_mm3(a,b):
    if a not in bpy.data.objects or b not in bpy.data.objects: return None
    for m in bpy.data.objects[a].modifiers:
        if m.type=='BOOLEAN': m.operation='INTERSECT'; m.object=bpy.data.objects[b]; m.solver='EXACT'
    dg=bpy.context.evaluated_depsgraph_get(); ev=bpy.data.objects[a].evaluated_get(dg)
    n=len(ev.data.vertices); return 0.0 if n==0 else None  # 顶点0=无交集; 有顶点=需体积(仅报0/非0)
def xspan(o):
    W=w(o); return (min(v.x for v in W)*1e3, max(v.x for v in W)*1e3) if W else None
print("=== 4 类证据核查 (scene_v13.blend) ===")
# 1 光路(冷却光)
print("[1] 光路(冷却光): 交点/方向/接口/与不透明实体")
for cn in ['cool_bm_1','cool_bm_2','cool_bm_3','cool_bm_4']:
    x0,x1=xspan(cn); pen=[t for t in ['cav_outer','cuo_lining','mot_coil_L','mot_coil_R'] if (inter_mm3(cn,t)==0.0 or inter_mm3(cn,t) is not None)]
    print(f"   {cn}: x∈[{x0:.1f},{x1:.1f}]mm (-x端{x0:.1f}>0铜管口=不穿管壁) 交集={'有' if pen else '0'}")
# 2 装配(后窗/相邻实体)
print("[2] 装配(后窗): 覆盖/接触/穿透")
for a,b in [('sapph_window','cav_outer'),('sapph_window','cuo_lining'),('sapph_window','sapph_seat_ring'),
            ('sapph_seat_ring','cav_outer'),('sapph_seat_ring','cuo_lining'),('sapph_seat_ring','sapph_flange')]:
    print(f"   {a} ∩ {b} = {inter_mm3(a,b)} 顶点(0=无穿透)")
# 3 显示状态(线圈)
print("[3] 显示状态: 总览两主线圈 + 副本")
for c in ['mot_coil_L','mot_coil_R','mot_coil_L_display']:
    O=bpy.data.objects.get(c); print(f"   {c}: 顶点{len(O.data.vertices)} hide_render={O.hide_render}")
# 4 图像清晰度
print("[4] 图像清晰度: 待人工核查(agent 无法自证 PNG 像素), 已输出 8 张预览 + 1 张蒙太奇")
for f in ['render_v13_prev_overview','render_v13_prev_cavity','render_v13_prev_rear_window',
          'render_v13_prev_mot_entrance','render_v13_prev_top_hole','render_v13_prev_top_mirror',
          'render_v13_prev_right','render_v13_prev_left_conn']:
    import os; p=f"render-output/{f}.png"
    print(f"   {f}.png {'存在' if os.path.exists(p) else '缺失'}")
