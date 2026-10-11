import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v5.blend")
deps=bpy.context.evaluated_depsgraph_get()
o=bpy.data.objects['cav_outer']; oev=o.evaluated_get(deps); me=oev.data
in_wall=[]; total=len(me.vertices)
for v in me.vertices:
    w=oev.matrix_world @ v.co
    if -0.145 <= w.x <= -0.130:
        in_wall.append((round(w.x,4),round(w.y,4),round(w.z,4)))
print(f"cav_outer 顶点 x∈[-0.145,-0.130] (左壁±5mm 邻域) 数量: {len(in_wall)}/{total}")
for p in in_wall[:8]: print("  ",p)
xs=sorted({p[0] for p in in_wall})
print("这些顶点的 x 分布:", xs[:6], "...", xs[-6:] if len(xs)>6 else "")
# vac_shell 左壁 x 范围确认：从 vac_shell 顶点直接看左壁实体
o2=bpy.data.objects['vac_shell']; o2ev=o2.evaluated_get(deps); me2=o2ev.data
shell_left=[ (o2ev.matrix_world @ v.co).x for v in me2.vertices ]
import collections
print("vac_shell 顶点 x 分布(左端):", sorted(round(x,4) for x in shell_left)[:10])
