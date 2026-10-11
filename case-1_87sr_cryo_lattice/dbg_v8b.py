import bpy, mathutils, math
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v7.blend")
print("win_left exists?", bool(bpy.data.objects.get('win_left')))
print("left_feedthrough exists?", bool(bpy.data.objects.get('left_feedthrough')))
# 列出左壁附近所有对象
for o in bpy.data.objects:
    b=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    xmin=min(v.x for v in b)
    if xmin<-0.145: print(" ", o.name, "x_min=",round(xmin,4))
