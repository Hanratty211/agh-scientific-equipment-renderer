import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v3.blend")
scene=bpy.context.scene
deps=bpy.context.evaluated_depsgraph_get()
ray=scene.ray_cast
def blocked_between(cam, target, name):
    c=mathutils.Vector(cam)
    t=mathutils.Vector(target)
    hit,loc,nrm,idx,ob,_=ray(deps, c, (t-c).normalized())
    if hit and ob and ob.name not in (''+name,):
        return ob.name
    return None
cams={'cam_overview':('cav_outer',(-0.08,0,0.02),0),
      }
# 检查 aperture 通孔是否真的空心：沿轴从 +x 端穿入 ap_ring 位置
import math
ap_pos=(mathutils.Vector((-0.08,0,0.02)))
# 从 ap 中心 +x 方向 1cm 处向 -x 发射射线，若穿过 ap_ring 表面后进入空腔
hit,loc,nrm,idx,ob,_=ray(deps, ap_pos+mathutils.Vector((0.02,0,0)), mathutils.Vector((-1,0,0)))
print("ray through aperture hole hits:", ob.name if ob else 'nothing (empty space)')
# 相机视锥验证（用 make_cam 的朝向逻辑复核）
for cam_name,pos,lens in [('cam_overview',(0.10,-0.20,0.14),55),
                          ('cam_cavity',(-0.22,0.0,0.02),60),
                          ('cam_cut',(-0.08,-0.20,0.02),60)]:
    look={'cam_overview':(-0.045,0,0.02),'cam_cavity':(-0.03,0,0.02),'cam_cut':(-0.08,0,0.02)}[cam_name]
    d=mathutils.Vector(look)-mathutils.Vector(pos)
    fwd=d.normalized()
    print(f"{cam_name}: looking {fwd.round(2)} from {pos}")
