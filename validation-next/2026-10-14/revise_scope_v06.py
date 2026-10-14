"""13 v06 lengthens v05 candidate head toward viewing front.
Initial v05 audit falsely used local dimensions.y for a Y-rotated cylinder; corrected audit
passes v05 too. v06 remains an independent optional silhouette variant, NOT a proven repair.
Rear ferrules/fiber bundles and flexible shaft unchanged; dimensions illustrative.
"""
import bpy
from pathlib import Path
root=Path(__file__).resolve().parent
if bpy.context.scene.get('revision_version')!='v05':raise RuntimeError('expected v05')
body=bpy.data.objects['Distal_long_scope_head'];body.location.y=.32;body.scale.z*=2.10
# Blender cylinder local-Z rotated about X -> world-Y; scale local Z extends length only.
bezel=bpy.data.objects['Distal_front_bezel'];bezel.location.y=-.016
window=bpy.data.objects['Distal_optical_front_window'];window.location.y=-.047
body['v06_note']='length adjusted to distinguish probe barrel from former short cap; scale illustrative'
for o in (bezel,window):o['owner']=body.name
sc=bpy.context.scene;sc['revision_version']='v06';sc['visual_review']='pending_external_pixel_review';sc['v06_reason']='lengthen silhouette independently; original v05 audit used wrong local axis and was corrected (v05 now passes limited check)'
bpy.context.view_layer.update();out=root/'cases/13_biomed_optics/v06'
if out.exists():raise RuntimeError('no overwrite')
out.mkdir();bpy.ops.wm.save_as_mainfile(filepath=str(out/'scene.blend'));print('SCOPE_V06_SAVED',flush=True)
