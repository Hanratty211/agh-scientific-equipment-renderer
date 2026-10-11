import bpy, mathutils, math
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v12.blend")
o=bpy.data.objects['cuo_lining']
b=[o.matrix_world @ mathutils.Vector((v.co.x,v.co.y,v.co.z)) for v in o.data.vertices]
rmax=max(math.hypot(v.y,v.z-0.020) for v in b)
print(f"cuo_lining 半径≈{rmax*1000:.2f}mm, x∈[{min(v.x for v in b):.4f},{max(v.x for v in b):.4f}]")
xend=min(v.x for v in b)
near=[v for v in b if v.x < xend+0.0002]
rnear=sorted(set(round(math.hypot(v.y,v.z-0.020),4) for v in near))
print(f"末端面(x<{xend+0.0002:.4f}) 出现的半径值: {rnear}")
