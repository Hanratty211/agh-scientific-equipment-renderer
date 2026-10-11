import bpy, mathutils, math
bpy.ops.wm.read_factory_settings(use_empty=True)
# 不经过 box(), 直接 primitive_cube_add
bpy.ops.mesh.primitive_cube_add(size=1, location=(0.0,0.0,0.020), rotation=(math.radians(135),0,math.radians(90)))
o=bpy.context.object; o.name="direct"
o.scale=(0.020,0.012,0.0006)
print("直接创建 未apply: loc",[round(v,4) for v in o.location],"rot",[round(math.degrees(v),1) for v in o.rotation_euler])
bpy.ops.object.transform_apply(scale=True)
print("apply scale 后: loc",[round(v,4) for v in o.location],"rot",[round(math.degrees(v),1) for v in o.rotation_euler])
# 再试: transform_apply 是否把 location 也清了?
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
print("显式 location=False 后: loc",[round(v,4) for v in o.location])
