import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v6.blend")
SW=18.0
def bb(name):
    o=bpy.data.objects.get(name)
    b=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    lo=mathutils.Vector((min(v[i] for v in b) for i in range(3)))
    hi=mathutils.Vector((max(v[i] for v in b) for i in range(3)))
    return (lo+hi)/2

CAV_X=-0.08; AXIS_Z=0.02
targets=[bb(k) for k in ['ap_ring','interrogation_vol','sapph_window']]
# 直接用 Blender 的 to_track_quat 逻辑（和 make_cam 完全一致），网格搜索
import math
best=None
for y in [v/1000 for v in range(200,500,50)]:
    for z in [v/1000 for v in range(80,200,40)]:
        loc=mathutils.Vector((CAV_X+0.015, y, AXIS_Z+z))
        look=mathutils.Vector((CAV_X-0.02, 0.0, AXIS_Z))
        d=look-loc
        quat=(-d).to_track_quat('Z','Y')
        rot=quat.to_matrix().to_4x4()
        mat=mathutils.Matrix.Translation(loc) @ rot
        minv=mat.inverted()
        nx_list=[]
        ok=True
        for c in targets:
            p=minv @ c
            if p.z>0: ok=False; break
            nx=(p.x/abs(p.z))*(45/SW*0.5)
            nx_list.append(round(nx,2))
            if abs(nx)>0.45: ok=False
        if ok and len(nx_list)==3:
            score=max(abs(n) for n in nx_list)
            if best is None or score<best[0]:
                best=(score,(y,z),nx_list)
                print(f"loc y={y} z={z}: max|nx|={score:.2f}  nx={nx_list}")
print("最佳(相对当前Cavity中心):", best)
