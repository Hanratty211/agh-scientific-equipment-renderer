import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v5.blend")
scene=bpy.context.scene
deps=bpy.context.evaluated_depsgraph_get()
# 顶壁开孔圆心预期 (0.010, 0)，半径 5mm。做圆周一圈射线检测：
# 在圆心 5mm 半径的圆周上取 36 点，从上方射 -z，检查是否命中 vac_shell
# 若圆周上多数点未命中 → 开孔真实且大小接近 5mm；若全命中 → 开孔没切掉
import math
cx,cy = 0.010, 0.0
top_z = 0.095
miss=0; total=36
for i in range(total):
    a = 2*math.pi*i/total
    x = cx + 0.005*math.cos(a)
    y = cy + 0.005*math.sin(a)
    hit,loc,nrm,idx,ob,_ = scene.ray_cast(deps, mathutils.Vector((x,y,top_z)), mathutils.Vector((0,0,-1)))
    if not hit or ob.name!='vac_shell':
        miss+=1
print("圆周(半径5mm) 36 点中未命中 vac_shell 的点数:", miss)
# 再测 10mm 半径圆周（应为实心，全部命中）
miss2=0
for i in range(total):
    a=2*math.pi*i/total
    x=cx+0.010*math.cos(a); y=cy+0.010*math.sin(a)
    hit,loc,nrm,idx,ob,_=scene.ray_cast(deps,mathutils.Vector((x,y,top_z)),mathutils.Vector((0,0,-1)))
    if not hit or ob.name!='vac_shell': miss2+=1
print("圆周(半径10mm) 36 点中未命中点数:", miss2, "(预期接近 0)")
# 开孔中心 1 点
hit,loc,nrm,idx,ob,_=scene.ray_cast(deps,mathutils.Vector((cx,cy,top_z)),mathutils.Vector((0,0,-1)))
print("开孔中心(0.010,0) 射线命中:", ob.name if ob else 'nothing(empty)')
