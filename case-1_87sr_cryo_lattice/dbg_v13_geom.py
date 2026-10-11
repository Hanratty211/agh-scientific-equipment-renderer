import bpy, mathutils, math
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v12.blend")
AX=0.02
# 关键 x 位置
print("铜管前端 x=0.0; 内衬前端(x=+0.012)=突出; 线圈R中心 x=+0.040 R=32mm 内缘 x=+0.008; 线圈L中心 x=-0.040")
print("MOT 汇聚点应在线圈中心 x=0(两线圈中点), 铜管前端在 x=0.0")
# 当前冷却光束端点 x 范围
for cn in ['cool_bm_1','cool_bm_2','cool_bm_3','cool_bm_4']:
    o=bpy.data.objects.get(cn)
    b=[o.matrix_world @ mathutils.Vector((v.co.x,v.co.y,v.co.z)) for v in o.data.vertices]
    print(f"  {cn}: x∈[{min(v.x for v in b)*1000:.1f},{max(v.x for v in b)*1000:.1f}] mm")
# 线圈内缘(线圈 R=32mm 内径 = 32-3=29mm? 实际 torus R=0.032 主环, 线圈内缘距轴 ~0.032)
print("线圈 torus R=0.032 -> 线圈环中心距轴 32mm, 线径 3mm -> 线圈实体半径带 29~35mm")
