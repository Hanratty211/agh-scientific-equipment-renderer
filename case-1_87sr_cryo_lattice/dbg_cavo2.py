import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v6.blend")
SW=18.0
def bb(name):
    o=bpy.data.objects.get(name)
    b=[o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
    lo=mathutils.Vector((min(v[i] for v in b) for i in range(3)))
    hi=mathutils.Vector((max(v[i] for v in b) for i in range(3)))
    return (lo+hi)/2, lo, hi

CAV_X=-0.08; AXIS_Z=0.02
import itertools, math
best=None
for dx in [0.005,0.008,0.012]:
    for dy in [0.025,0.035,0.045]:
        for dz in [0.008,0.012,0.016]:
            for lx in [CAV_X-0.03, CAV_X, CAV_X+0.03]:
                loc=mathutils.Vector((CAV_X+0.015, dy, AXIS_Z+dz))
                look=mathutils.Vector((lx,0,AXIS_Z))
                d=look-loc
                cam_loc=loc
                # 模拟 make_cam: 朝向 = -d 方向作为 -Z
                fwd=(-d).normalized()
                # 计算各目标在相机空间的归一化坐标
                m=mathutils.Matrix()
                # 构建相机矩阵: 位置 loc, 朝向 fwd
                zvec=(-fwd)
                xvec=fwd.cross(mathutils.Vector((0,0,1))).normalized()
                if xvec.length<0.01: xvec=mathutils.Vector((1,0,0))
                yvec=zvec.cross(xvec)
                rot=mathutils.Matrix((xvec,yvec,zvec)).to_4x4()
                mat=mathutils.Matrix.Translation(loc) @ rot
                minv=mat.inverted()
                ok=True
                nx_list=[]
                for tgt in ['ap_ring','interrogation_vol','sapph_window']:
                    c,_,_=bb(tgt)
                    p=minv @ c
                    if p.z>0: ok=False; break
                    nx=(p.x/abs(p.z))*(40/SW*0.5)
                    nx_list.append((tgt,nx))
                    if abs(nx)>0.45: ok=False
                if ok and len(nx_list)==3:
                    score=max(abs(n[1]) for n in nx_list)
                    if best is None or score<best[0]:
                        best=(score,loc,look,40)
                        print(f"候选 loc={[round(v,3) for v in loc]} look_x={look.x} dz={dz} lens=40  max|nx|={score:.2f}  {nx_list}")
print("\n最佳:", best)
