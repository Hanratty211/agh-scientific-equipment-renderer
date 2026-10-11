import bpy, mathutils, math
bpy.ops.wm.read_factory_settings(use_empty=True)
def box(name, sx, sy, sz, loc, rot=(0,0,0), m=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o=bpy.context.object; o.name=name
    o.scale=(sx,sy,sz)
    bpy.ops.object.transform_apply(scale=True)
    return o
# 复刻 v7 二向色镜
n=mathutils.Vector((1,0,-1)).normalized()
euler=n.to_track_quat('Z','Y').to_euler()
o=box("dichroic_mir",0.020,0.012,0.0006,(0.0,0.0,0.020),rot=euler)
print("box() 后 loc:",[round(v,4) for v in o.location],"rot(deg)",[round(math.degrees(v),1) for v in o.rotation_euler])
# 现在模拟 v7 场景里后续可能影响它的操作: 保存主文件+重载
bpy.ops.wm.save_mainfile(filepath="/tmp/test_box.blend")
bpy.ops.wm.open_mainfile(filepath="/tmp/test_box.blend")
o2=bpy.data.objects['dichroic_mir']
print("重载后 loc:",[round(v,4) for v in o2.location],"rot(deg)",[round(math.degrees(v),1) for v in o2.rotation_euler])
