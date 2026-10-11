import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v5.blend")
scene=bpy.context.scene
deps=bpy.context.evaluated_depsgraph_get()
shell=bpy.data.objects['vac_shell']
# 顶壁开孔圆心应在 (CLK_HOLE_X=0.010, y=0, z=0.075 顶壁面)
# 围绕 (0.010, 0) 密集采样
import numpy as np
xs=np.arange(-0.01,0.05,0.004)
ys=np.arange(-0.04,0.04,0.004)
hits=[]
for x in xs:
    for y in ys:
        origin=mathutils.Vector((x,y,0.095))
        d=mathutils.Vector((0,0,-1))
        hit,loc,nrm,idx,ob,_=scene.ray_cast(deps,origin,d)
        if not hit or ob.name!='vac_shell':
            hits.append((x,y))
print("围绕(0.010,0)的顶壁网格未命中点数:",len(hits),"共",len(xs)*len(ys))
if hits:
    xs_h=[h[0] for h in hits]; ys_h=[h[1] for h in hits]
    print("未命中带: x∈[%.3f,%.3f] y∈[%.3f,%.3f]"%(min(xs_h),max(xs_h),min(ys_h),max(ys_h)))
# 检查 vac_shell 里是否残留早期布尔切割产生的错误斜向开孔面
o=shell
print("vac_shell 顶点数:",len(o.data.vertices))
