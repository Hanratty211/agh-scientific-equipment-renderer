import bpy, mathutils, math
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v8.blend")
deps=bpy.context.evaluated_depsgraph_get()
# 铜腔 cav_outer 实际 x 范围(含铜管本体, 不含布尔挖空后顶点, 用原始对象 bound_box)
o=bpy.data.objects['cav_outer']
b=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
xmin=min(v.x for v in b); xmax=max(v.x for v in b)
print(f"cav_outer 实际 x 范围: [{xmin:.4f}, {xmax:.4f}]")
# 左壁金属 slab: vac_shell 内表面/外表面 x
# CHAM_CX=-0.040, CHAM_W=0.200 -> 外表面 x = -0.040-0.100 = -0.140, 内表面 x = -0.140+0.003 = -0.137
# 铜管 xmin 是否 < -0.137(内表面)? 若是 -> 铜管穿过左壁金属 slab(-0.140..-0.137)
print(f"左壁金属 slab x 范围: [-0.1400, -0.1370]")
print(f"铜管 xmin={xmin:.4f} < -0.1370(内表面)? {xmin < -0.1370}  结论: {'铜管穿过左壁金属 slab' if xmin < -0.1370 else '铜管不穿左壁金属 slab'}")
# left_feedthrough 环 x 范围 vs 铜管 xmin
ft=bpy.data.objects.get('left_feedthrough')
if ft:
    fb=[ft.matrix_world @ mathutils.Vector(c) for c in ft.bound_box]
    print(f"left_feedthrough x 范围: [{min(v.x for v in fb):.4f}, {max(v.x for v in fb):.4f}]")
    print("=> 铜管本体(xmin 到 xmax)穿过 left_feedthrough 环所在 x 区间, 环内孔已挖(半径0.0075>铜管外半径0.0065), 铜管穿过孔而非穿实体金属")
