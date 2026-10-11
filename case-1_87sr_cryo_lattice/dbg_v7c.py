import bpy, mathutils, math
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v7.blend")
o=bpy.data.objects['dichroic_mir']
print("dichroic_mir rotation_euler(deg):",[round(math.degrees(v),1) for v in o.rotation_euler])
print("loc:",[round(v,3) for v in o.location])
# 期望: 法向 n=(1,0,-1)/sqrt2 -> to_track_quat('Z','Y') 让 +Z 指向 n
n=mathutils.Vector((1,0,-1)).normalized()
q=n.to_track_quat('Z','Y')
print("expected quat:",q, "-> euler(deg)",[round(math.degrees(v),1) for v in q.to_euler()])
# 实际: local z in world
lz=o.matrix_world.to_quaternion() @ mathutils.Vector((0,0,1))
print("actual local z (world):",[round(v,3) for v in lz])
# 检查 n 是否确实让 d_in 反射成 d_out
d_in=mathutils.Vector((0,0,-1)); d_out=mathutils.Vector((-1,0,0))
d_ref=d_in-2*(d_in.dot(n))*n
print("reflect(d_in)=", [round(v,3) for v in d_ref], "应=(-1,0,0)")
