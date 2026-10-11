import bpy, mathutils
scene = bpy.context.scene
cam = scene.camera
cam_world = cam.matrix_world
cam_loc = cam_world.translation
cam_fwd = -(cam_world.to_3x3() @ mathutils.Vector((0,0,-1)))
print("cam at", [round(v,3) for v in cam_loc], "fwd", [round(v,3) for v in cam_fwd])
objs = [o for o in bpy.data.objects if o.type in ('MESH','CURVE') and not o.hide_render]
objs.sort(key=lambda o: (cam_loc - o.matrix_world.translation).length)
for o in objs:
    c = o.matrix_world.translation
    d = (c - cam_loc); dist = d.length
    ang = (d.normalized() @ cam_fwd)
    print(f"{o.name:22s} dist={dist:6.3f} ang={ang:+.2f}")
