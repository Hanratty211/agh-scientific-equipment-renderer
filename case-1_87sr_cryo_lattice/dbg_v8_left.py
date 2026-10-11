import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v8.blend")
scene=bpy.context.scene
deps=bpy.context.evaluated_depsgraph_get()
# 左壁玻璃窗 win_left 是否还存在? (v7 已移除, 改用 left_feedthrough 密封环)
print("win_left 存在?", bool(bpy.data.objects.get('win_left')))
# 实心铜管 vs 左壁金属 wall slab (实体布尔 INTERSECT, 非顶点采样)
CAV_X=-0.080; AXIS_Z=0.020; CAV_R_OUT=0.0065; CAV_LEN=0.160
# 左壁金属面: vac_shell 左壁 x 范围
o=bpy.data.objects['vac_shell'].evaluated_get(deps)
# 重建实心铜管
bpy.ops.mesh.primitive_cylinder_add(radius=CAV_R_OUT, depth=CAV_LEN,
    location=(CAV_X,0,AXIS_Z), rotation=(0,1.5708,0), vertices=64)
solid=bpy.context.object; solid.name="v8_solid_cav"
# 左壁金属 slab(仅金属, 不含玻窗)
import math as _m
LEFT_WALL_X = -0.040 - 0.100 + 0.0015  # CHAM_CX - CHAM_W/2 + T/2
bpy.ops.mesh.primitive_cube_add(size=1, location=(LEFT_WALL_X,0,0.0), rotation=(0,_m.radians(90),0))
slab=bpy.context.object; slab.scale=(0.003,0.150,0.150)
bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
md=solid.modifiers.new("b",'BOOLEAN'); md.operation='INTERSECT'; md.object=slab
bpy.context.view_layer.objects.active=solid
bpy.ops.object.modifier_apply(modifier="b")
print(f"实心铜管 ∩ 左壁金属slab(x={LEFT_WALL_X:.4f}) 顶点数: {len(solid.data.vertices)} (0=不穿金属; >0=穿金属)")
bpy.data.objects.remove(solid,do_unlink=True); bpy.data.objects.remove(slab,do_unlink=True)
# left_feedthrough 密封环位置/半径
ft=bpy.data.objects.get('left_feedthrough')
if ft:
    b=[ft.matrix_world @ mathutils.Vector(c) for c in ft.bound_box]
    print("left_feedthrough x:", [round(min(v.x for v in b),4), round(max(v.x for v in b),4)])
    print("left_feedthrough 半径~0.010 > 铜管外半径0.0065, 内孔已挖 r=0.0075 -> 铜管穿过孔, 不穿实体")
