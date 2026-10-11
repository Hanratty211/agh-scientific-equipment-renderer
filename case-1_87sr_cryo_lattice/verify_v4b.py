import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v4.blend")
scene=bpy.context.scene
SW, SH = 18.0, 10.125
def ndc(cam, world_pt):
    m=cam.matrix_world.inverted()
    p=m @ world_pt
    if p.z>0: return None
    f_x=cam.data.lens/SW*0.5; f_y=cam.data.lens/SH*0.5
    return (p.x/abs(p.z))*f_x, (p.y/abs(p.z))*f_y

# MOT线圈环的完整外径端点
for cam_name in ['cam_overview']:
    cam=bpy.data.objects[cam_name]
    for coil in ['mot_coil_L','mot_coil_R']:
        o=bpy.data.objects[coil]
        bb=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
        lo=mathutils.Vector((min(v[i] for v in bb) for i in range(3)))
        hi=mathutils.Vector((max(v[i] for v in bb) for i in range(3)))
        for corner in [lo,hi,(lo+hi)/2]:
            r=ndc(cam,corner)
            if r: print(f"{cam_name} {coil} pt={[round(v,3) for v in corner]} ndc=({r[0]:+.2f},{r[1]:+.2f}) in={abs(r[0])<0.5 and abs(r[1])<0.5}")
            else: print(f"{cam_name} {coil} BEHIND")
# 腔体外径端点
o=bpy.data.objects['cav_outer']
bb=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
lo=mathutils.Vector((min(v[i] for v in bb) for i in range(3)))
hi=mathutils.Vector((max(v[i] for v in bb) for i in range(3)))
cam=bpy.data.objects['cam_overview']
for corner,label in [(lo,'cav_outer lo'),(hi,'cav_outer hi')]:
    r=ndc(cam,corner)
    print(f"{label} pt={[round(v,3) for v in corner]} ndc=({r[0]:+.2f},{r[1]:+.2f}) in={abs(r[0])<0.5 and abs(r[1])<0.5}")
