import bpy, mathutils, math
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v7.blend")
scene=bpy.context.scene
deps=bpy.context.evaluated_depsgraph_get()
# 真实场景: 实心铜管 vs left_feedthrough 密封环 —— 应为"环套住管"而非"管插穿实体"
bpy.ops.mesh.primitive_cylinder_add(radius=0.0065, depth=0.160, location=(-0.080,0,0.020),
    rotation=(0,math.radians(90),0), vertices=64)
solid=bpy.context.object; solid.name="ts2"
ft=bpy.data.objects['left_feedthrough']
# 布尔 INTERSECT 实心铜管 ∩ 密封环(实体, 未镂空) -> 看是否重叠
md=solid.modifiers.new("b",'BOOLEAN'); md.operation='INTERSECT'; md.object=ft
bpy.context.view_layer.objects.active=solid
bpy.ops.object.modifier_apply(modifier="b")
print(f"实心铜管 ∩ left_feedthrough(实体环) 顶点数: {len(solid.data.vertices)}")
print("说明: 若>0 表示铜管与密封环实体相交(管穿过环本体), 需把环做成'套环'(内孔>管径)让管穿过孔而非穿实体")
# 检查 left_feedthrough 本身是否镂空(有内孔)
ft_ev=ft.evaluated_get(deps)
print("left_feedthrough 面数:", len(ft_ev.data.polygons), " 顶点:", len(ft_ev.data.vertices))
# 环的半径 0.010 > 管外半径 0.0065 -> 环内孔应包住管; 但 cyl() 默认实心(无内孔)!
# cyl helper 不挖内孔, 所以 left_feedthrough 是实心圆柱 -> 铜管确实插穿它
bpy.data.objects.remove(solid,do_unlink=True)
