import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v5.blend")
scene=bpy.context.scene
deps=bpy.context.evaluated_depsgraph_get()
shell=bpy.data.objects['vac_shell']
# 在右壁区域 (x≈0.055-0.065, z=0.02, y=0) 密集发射射线，检测是否存在孔洞
# 从 +x 外侧向 -x 射，若某个位置没有 shell 阻挡（即射线穿过 wall 区域仍命中其他东西或什么都没命中），说明有孔
import numpy as np
xs=np.arange(0.054,0.066,0.002)
zs=np.arange(0.0,0.04,0.002)
hits=[]
for x in xs:
    for z in zs:
        origin=mathutils.Vector((x+0.004, 0.0, z))
        d=mathutils.Vector((-1,0,0))
        hit,loc,nrm,idx,ob,_=scene.ray_cast(deps,origin,d)
        if not hit or ob.name!='vac_shell':
            hits.append((round(x,3),round(z,3)))
print("右壁区域未命中 vac_shell 的 (x,z) 网格点数量:", len(hits), "/", len(xs)*len(zs))
if hits:
    xs_h=[h[0] for h in hits]; zs_h=[h[1] for h in hits]
    print("未命中区域 x∈[%.3f,%.3f] z∈[%.3f,%.3f]" % (min(xs_h),max(xs_h),min(zs_h),max(zs_h)))
# 顶壁
xs2=np.arange(-0.02,0.06,0.004)
ys2=np.arange(-0.03,0.04,0.004)
hits2=[]
for x in xs2:
    for y in ys2:
        origin=mathutils.Vector((x,y,0.095))
        d=mathutils.Vector((0,0,-1))
        hit,loc,nrm,idx,ob,_=scene.ray_cast(deps,origin,d)
        if not hit or ob.name!='vac_shell':
            hits2.append((round(x,3),round(y,3)))
print("顶壁区域未命中 vac_shell 的网格点数量:", len(hits2), "/", len(xs2)*len(ys2))
if hits2:
    print("顶壁未命中点示例:", hits2[:12])
