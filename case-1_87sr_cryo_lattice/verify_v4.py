import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v4.blend")
scene=bpy.context.scene
# Blender 传感器默认 36mm 宽；但 16:9 渲染会裁切上下，不裁切左右
SW=18.0
def bbox_center(name):
    o=bpy.data.objects.get(name)
    bb=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    lo=mathutils.Vector((min(v[i] for v in bb) for i in range(3)))
    hi=mathutils.Vector((max(v[i] for v in bb) for i in range(3)))
    return (lo+hi)/2
targets={k:bbox_center(k) for k in ['mot_coil_L','mot_coil_R','cav_outer','ap_ring','sapph_window']}
for cam_name in ['cam_overview','cam_cut']:
    cam=bpy.data.objects[cam_name]
    lens=cam.data.lens
    f=lens/SW*0.5
    print(f"\n--- {cam_name} (lens {lens}) 正确投影 (36mm sensor) ---")
    for name,pt in targets.items():
        m=cam.matrix_world.inverted()
        p=m @ pt
        if p.z>0:
            print(f"  {name:14s} BEHIND"); continue
        nx=(p.x/abs(p.z))*f
        full=abs(nx)<0.5
        print(f"  {name:14s} nx={nx:+.2f} in_full_frame_x={full}")
