import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v6.blend")
o=bpy.data.objects['sapph_window']
b=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
lo=mathutils.Vector((min(v[i] for v in b) for i in range(3)))
hi=mathutils.Vector((max(v[i] for v in b) for i in range(3)))
print("sapph_window bbox:", [round(v,3) for v in lo], [round(v,3) for v in hi])
cam=bpy.data.objects['cam_cavo']
print("cam_cavo loc:", [round(v,3) for v in cam.location])
m=cam.matrix_world.inverted()
c=(lo+hi)/2
p=m @ c
print("sapph_window in cam space: z=", round(p.z,4), "(>0 = 相机后方)")
