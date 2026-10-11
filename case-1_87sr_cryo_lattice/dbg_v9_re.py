import bpy, mathutils, math
bpy.ops.wm.read_factory_settings(use_empty=True)
# 复刻 build 里的关键几何, 验证 cam5a 能否同框 (开孔, 顶壁墙厚, 入射段, 二向色镜),
# 以及 cam_cavo 能否把铜腔右端拉进框
import math as m
def make_cam(name, loc, look_at, lens=50, clip_start=0.001, clip_end=2.0):
    d = mathutils.Vector(look_at) - mathutils.Vector(loc)
    quat = (-d).to_track_quat('Z','Y')
    rot = quat.to_euler()
    bpy.ops.object.camera_add(location=loc, rotation=rot)
    c = bpy.context.object; c.name=name
    c.data.lens = lens; c.data.clip_start=clip_start; c.data.clip_end=clip_end
    return c
CHAM_CZ=0.0; CHAM_H=0.150; T=0.003
CLK_TOP_Z = CHAM_CZ + CHAM_H/2 - T/2
CLK_HOLE_X=0.0; AXIS_Z=0.020; CAV_X=-0.080
# 建目标
bpy.ops.mesh.primitive_cube_add(size=1,location=(CLK_HOLE_X,0,CLK_TOP_Z))
hole=bpy.context.object; hole.scale=(0.01,0.01,0.003); bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); hole.name='clock_top_hole'
bpy.ops.mesh.primitive_cube_add(size=1,location=(CLK_HOLE_X,0,AXIS_Z))
mir=bpy.context.object; mir.scale=(0.02,0.012,0.0006); bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); mir.name='dichroic_mir'
# 入射段(垂直光束)
bpy.ops.mesh.primitive_cylinder_add(radius=0.0012,depth=0.03+0.05,location=(CLK_HOLE_X,0,(CLK_TOP_Z+AXIS_Z)/2+0.005))
bm=bpy.context.object; bm.name='clock_bm'
# cam5a (v9 修正后)
cam5a = make_cam("cam_port_top",(CLK_HOLE_X + 0.020, -0.055, AXIS_Z + 0.075),
                 look_at=(CLK_HOLE_X, 0.0, (CLK_TOP_Z + AXIS_Z)/2), lens=45)
SW=18.0
for tgt in ['clock_top_hole','dichroic_mir','clock_bm']:
    o=bpy.data.objects[tgt]; b=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    cx=(min(v[0] for v in b)+max(v[0] for v in b))/2
    cy=(min(v[1] for v in b)+max(v[1] for v in b))/2
    cz=(min(v[2] for v in b)+max(v[2] for v in b))/2
    p=cam5a.matrix_world.inverted() @ mathutils.Vector((cx,cy,cz))
    nx=(p.x/abs(p.z))*(45/SW*0.5); ny=(p.y/abs(p.z))*(45/(SW*9/16)*0.5)
    print(f"cam5a -> {tgt}: 中心 nx={nx:+.2f} ny={ny:+.2f} in_frame={abs(nx)<0.5 and abs(ny)<0.5}")
# cam_cavo 右端: 铜腔右端 x = CAV_X + CAV_LEN/2 = 0.0; 左端 = -0.160
cam6 = make_cam("cam_cavo", (CAV_X + 0.085, -0.130, AXIS_Z + 0.045),
                look_at=(CAV_X - 0.020, 0.0, AXIS_Z), lens=32)
for xpt in [0.0, -0.08, -0.16]:  # 铜腔右端/中部/左端(后窗)
    p=cam6.matrix_world.inverted() @ mathutils.Vector((xpt,0,AXIS_Z))
    nx=(p.x/abs(p.z))*(32/SW*0.5); ny=(p.y/abs(p.z))*(32/(SW*9/16)*0.5)
    print(f"cam_cavo -> 铜腔 x={xpt}: nx={nx:+.2f} ny={ny:+.2f} in_frame={abs(nx)<0.5 and abs(ny)<0.5}")
