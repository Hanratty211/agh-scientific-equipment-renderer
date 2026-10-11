import bpy, mathutils
bpy.ops.wm.open_mainfile(filepath="render-output/scene_v4.blend")
cam=bpy.data.objects['cam_cut']
print('cam_cut loc',[round(v,3) for v in cam.location],'lens',cam.data.lens)
# 视锥半宽角：36mm 传感器，水平半宽 = 18mm / lens
import math
for lens in [35,28,22,18]:
    half_h_mm = 18.0/lens*1000  # 半宽(米) 在 1m 距离上 = (18/lens) m... 实际: FOV水平 = 2*atan(18/lens)
    dist = mathutils.Vector((-0.08,0,0.02)) - cam.location
    dist_y = dist.length
    half_w = dist_y * (18.0/lens)
    print(f"lens {lens}: at dist {dist_y:.3f} m, half-width in scene = {half_w:.4f} m  (need >=0.162)")
