import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v3.blend")
scene=bpy.context.scene
# 场景包围盒
mn=mathutils.Vector((1e9,1e9,1e9)); mx=mathutils.Vector((-1e9,-1e9,-1e9))
for o in bpy.data.objects:
    if o.type in ('MESH','CURVE') and not o.hide_render:
        for c in o.bound_box:
            w=o.matrix_world @ mathutils.Vector(c)
            for i in range(3):
                mn[i]=min(mn[i],w[i]); mx[i]=max(mx[i],w[i])
# 每个相机：验证关键目标是否在视锥内（用相机矩阵投影测试）
targets = {
    'mot_coil_L': (-0.040, 0.0, 0.02),
    'mot_coil_R': ( 0.040, 0.0, 0.02),
    'cav_outer' : (-0.080, 0.0, 0.02),
    'ap_ring'   : (-0.080, 0.0, 0.02),
    'sapph_window':(-0.163, 0.0, 0.02),
    'lat_fiber' : ( 0.060, 0.0, 0.02),
}
for cam_name in ['cam_overview','cam_cavity','cam_cut']:
    cam=bpy.data.objects[cam_name]
    m=cam.matrix_world.inverted()
    aspect=1600/900
    f=cam.data.lens/50.0
    print(f"--- {cam_name} (lens {cam.data.lens}) ---")
    for tname, pos in targets.items():
        p=m @ mathutils.Vector(pos)
        # 相机坐标系：z<0 是前方；归一化 x,y 需 |y|/|x| <= aspect 且在 z 对应焦平面内
        in_front = p.z < 0
        if in_front:
            nx = p.x / abs(p.z) / f
            ny = p.y / abs(p.z) / f
            in_view = abs(nx) < 0.5 and abs(ny) < 0.5/aspect
            print(f"  {tname:14s} in_view={in_view}  nx={nx:+.2f} ny={ny:+.2f}")
        else:
            print(f"  {tname:14s} BEHIND_CAMERA")
