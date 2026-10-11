import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v3.blend")
o=bpy.data.objects['vac_shell']
mn=mathutils.Vector((1e9,1e9,1e9)); mx=mathutils.Vector((-1e9,-1e9,-1e9))
for c in o.bound_box:
    w=o.matrix_world @ mathutils.Vector(c)
    for i in range(3):
        mn[i]=min(mn[i],w[i]); mx[i]=max(mx[i],w[i])
print("vac_shell bbox mn",[round(v,4) for v in mn],"mx",[round(v,4) for v in mx])
print("verts:", len(o.data.vertices))
# 检查 y 方向有没有实体面（front cut 是否生效）：列出最靠 -y 的面
ys=sorted({round((o.matrix_world @ mathutils.Vector(v.co)).y,4) for v in o.data.vertices})
print("distinct y levels in shell:", ys[:8], "...", ys[-4:])
# 射线方向：从 cam_overview 指向 cavity
cam=bpy.data.objects['cam_overview'].matrix_world.translation
import math
print("cam loc:", [round(v,3) for v in cam])
