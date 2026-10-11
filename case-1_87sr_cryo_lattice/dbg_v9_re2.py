import bpy, mathutils, math
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v9.blend")
scene=bpy.context.scene
deps=bpy.context.evaluated_depsgraph_get()
SW=18.0
# 1. cam_cavo: 铜腔右端是否入框
cam=bpy.data.objects['cam_cavo']; lens=cam.data.lens
for xpt in [0.0,-0.08,-0.16]:
    p=cam.matrix_world.inverted() @ mathutils.Vector((xpt,0,0.02))
    nx=(p.x/abs(p.z))*(lens/SW*0.5); ny=(p.y/abs(p.z))*(lens/(SW*9/16)*0.5)
    print(f"cam_cavo -> 铜腔 x={xpt}: nx={nx:+.2f} ny={ny:+.2f} in_frame={abs(nx)<0.5 and abs(ny)<0.5}")
# 2. cam_port_top: 顶壁开孔+墙厚 是否入框
cam=bpy.data.objects['cam_port_top']; lens=cam.data.lens
CHK_TOP_Z=0.0735
for pt,lab in [((0.0,0,CHK_TOP_Z),"顶壁开孔中心"),((0.0,0,CHK_TOP_Z+0.0015),"墙厚上表面"),(0.0,0,0.020) and ((0.0,0,0.020),"晶格轴")]:
    if isinstance(pt,tuple):
        p=cam.matrix_world.inverted() @ mathutils.Vector(pt)
    else: continue
    nx=(p.x/abs(p.z))*(lens/SW*0.5); ny=(p.y/abs(p.z))*(lens/(SW*9/16)*0.5)
    print(f"cam_port_top -> {lab}: nx={nx:+.2f} ny={ny:+.2f} in_frame={abs(nx)<0.5 and abs(ny)<0.5}")
# 3. cam_port_top_mirror: 二向色镜
cam=bpy.data.objects['cam_port_top_mirror']; lens=cam.data.lens
o=bpy.data.objects['dichroic_mir']; b=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
cx=(min(v.x for v in b)+max(v.x for v in b))/2
cz=(min(v.z for v in b)+max(v.z for v in b))/2
p=cam.matrix_world.inverted() @ mathutils.Vector((cx,0,cz))
nx=(p.x/abs(p.z))*(lens/SW*0.5); ny=(p.y/abs(p.z))*(lens/(SW*9/16)*0.5)
print(f"cam_port_top_mirror -> 二向色镜中心: nx={nx:+.2f} ny={ny:+.2f} in_frame={abs(nx)<0.5 and abs(ny)<0.5}")
