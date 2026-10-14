"""02 v03: fix v02 audit failure where upper specimen ended below actual upper jaw z.
Starts only from saved v02. Old v01/v02 render/audit retained.
"""
import bpy
from pathlib import Path
root=Path(__file__).resolve().parent
s=bpy.data.objects['Soft_coupon_upper_clamped']
# v02 upper specimen z=2.07 ±.39 = [1.68,2.46], jaw body centred z=2.51.
# Extend upward so coupon enters jaw depth; represent segment continuity, no clamp-force proof.
s.location.z=2.11;s.dimensions.z=.90
s['v03_reason']='upper tip z=2.56 overlaps upper circular grip; shaft still overlaps lower coupon segment'
bpy.context.scene['revision_version']='v03';bpy.context.scene['visual_review']='external_human_review_pending';bpy.context.view_layer.update()
out=root/'cases/02_robotics/v03';out.mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(out/'scene.blend'));print('ROBOT_V03_SAVED',out/'scene.blend',flush=True)
