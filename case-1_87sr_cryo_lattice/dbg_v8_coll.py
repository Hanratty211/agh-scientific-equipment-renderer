import bpy, mathutils, math
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v7.blend")
scene=bpy.context.scene
deps=bpy.context.evaluated_depsgraph_get()
# 左壁金属 wall slab x-range
o=bpy.data.objects['vac_shell'].evaluated_get(deps)
# 用布尔 INTERSECT: 实心铜管(含实际 CAV 半径) vs 左壁金属 slab
CAV_X=-0.080; AXIS_Z=0.020; CAV_R_OUT=0.0065; CAV_LEN=0.160
bpy.ops.mesh.primitive_cylinder_add(radius=CAV_R_OUT, depth=CAV_LEN,
    location=(CAV_X,0,AXIS_Z), rotation=(0,math.radians(90),0), vertices=64)
solid=bpy.context.object; solid.name="tsolid"
# 左壁金属 slab: x -0.142..-0.137 (左壁外表面 -0.142? 实际: CHAM_CX-CHAM_W/2=-0.140, 外表面 -0.140, 内表面 -0.137)
bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.1385,0,0.0), rotation=(0,math.radians(90),0))
slab=bpy.context.object; slab.name="tslab"
slab.scale=(0.003,0.150,0.150)
bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
md=solid.modifiers.new("b",'BOOLEAN'); md.operation='INTERSECT'; md.object=slab
bpy.context.view_layer.objects.active=solid
bpy.ops.object.modifier_apply(modifier="b")
print(f"实心铜管 ∩ 左壁金属slab(x=-0.1385±0.0015) 顶点数: {len(solid.data.vertices)} (0=不穿金属; >0=穿过左壁金属)")
# 铜管左端 x 范围
print(f"铜管 x范围: [{CAV_X-CAV_LEN/2:.4f},{CAV_X+CAV_LEN/2:.4f}]  左壁内表面x≈-0.137, 外表面≈-0.140")
# left_feedthrough 位置
ft=bpy.data.objects.get('left_feedthrough')
if ft:
    b=[ft.matrix_world @ mathutils.Vector(c) for c in ft.bound_box]
    print("left_feedthrough x:",[round(min(v.x for v in b),4),round(max(v.x for v in b),4)])
bpy.data.objects.remove(solid,do_unlink=True); bpy.data.objects.remove(slab,do_unlink=True)
