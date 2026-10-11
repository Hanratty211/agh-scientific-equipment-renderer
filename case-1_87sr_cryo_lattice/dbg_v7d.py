import bpy, mathutils, math
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v7.blend")
o=bpy.data.objects['dichroic_mir']
me=o.data
ws=[o.matrix_world @ v.co for v in me.vertices]
import numpy as np
arr=np.array([tuple(v) for v in ws])
c=arr.mean(0)
print("二向色镜 真实世界中心:",[round(v,4) for v in c])
lz=o.matrix_world.to_quaternion() @ mathutils.Vector((0,0,1))
n_exp=mathutils.Vector((1,0,-1)).normalized()
print("世界法向(local z):",[round(v,3) for v in lz])
print("期望法向:",[round(v,3) for v in n_exp],"  点积=",round(lz.dot(n_exp),3))
d_in=mathutils.Vector((0,0,-1)); d_ref=d_in-2*(d_in.dot(lz))*lz
print("reflect(d_in)=", [round(v,3) for v in d_ref], "应=(-1,0,0)")
