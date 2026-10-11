import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v5.blend")
deps=bpy.context.evaluated_depsgraph_get()
o=bpy.data.objects['cav_outer']; oev=o.evaluated_get(deps); me=oev.data
xs=[ (oev.matrix_world @ v.co).x for v in me.vertices ]
print("cav_outer 顶点 x: min=%.4f max=%.4f"%(min(xs),max(xs)))
# 左壁薄壳 x∈[-0.141,-0.136]
inside=[x for x in xs if -0.142<=x<=-0.135]
print("落在左壁薄壳 x∈[-0.142,-0.135] 的顶点数:", len(inside), "值:", sorted(set(round(x,4) for x in inside))[:10])
# 检查这些顶点是否真的属于"管壁实体"（z 在铜腔半径范围内）
import math
hits=[]
for v in me.vertices:
    w=oev.matrix_world @ v.co
    if -0.142<=w.x<=-0.135:
        hits.append((round(w.x,4),round(w.y,4),round(w.z,4)))
print("左壁薄壳内的 cav 顶点 (x,y,z):", hits)
# vac_shell 左壁实体范围
o2=bpy.data.objects['vac_shell']; o2ev=o2.evaluated_get(deps)
xs2=[ (o2ev.matrix_world @ v.co).x for v in o2ev.data.vertices ]
print("vac_shell 顶点 x: min=%.4f max=%.4f"%(min(xs2),max(xs2)))
left_wall_xs=sorted(set(round(x,4) for x in xs2 if x<0))
print("vac_shell 左端 x 分布:", left_wall_xs[:10])
