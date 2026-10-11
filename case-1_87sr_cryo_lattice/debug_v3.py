import bpy, mathutils, math
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v3.blend")
scene=bpy.context.scene
mn=mathutils.Vector((1e9,1e9,1e9)); mx=mathutils.Vector((-1e9,-1e9,-1e9))
for o in bpy.data.objects:
    if o.type in ('MESH','CURVE') and not o.hide_render:
        for c in o.bound_box:
            w=o.matrix_world @ mathutils.Vector(c)
            for i in range(3):
                mn[i]=min(mn[i],w[i]); mx[i]=max(mx[i],w[i])
print("bounds mn", [round(v,4) for v in mn], "mx", [round(v,4) for v in mx])
print("centre", [round(v,4) for v in (mn+mx)/2], "diag", round((mx-mn).length,4))
for c in ("cam_overview","cam_cavity","cam_cut"):
    o=bpy.data.objects.get(c)
    if o:
        d=[round(v,3) for v in o.location]
        print(c,"loc",d,"lens",o.data.lens, "fwd", [round(v,2) for v in (-(o.matrix_world.to_3x3() @ mathutils.Vector((0,0,-1))))])
# 相机是否朝向目标？计算 overview 相机到 MOT/腔体的距离
