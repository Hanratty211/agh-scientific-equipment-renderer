"""Render a detail camera of UNCHANGED saved 13 v07 geometry in a fresh Blender process.
Never save the .blend or alter objects/materials. Output is a separate detail PNG/report only.
Usage blender -b cases/13_biomed_optics/v07/scene.blend --python render_scope_detail.py -- detail.png
"""
import bpy,sys,hashlib,json,math
from pathlib import Path
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:];out=Path(args[0]).resolve()
if out.exists():raise RuntimeError('refusing to overwrite detail '+str(out))
source=Path(bpy.data.filepath);source_hash=hashlib.sha256(source.read_bytes()).hexdigest();scene=bpy.context.scene
assert scene.get('revision_version')=='v07'
assert all(n in bpy.data.objects for n in ('Distal_long_scope_head','Distal_scope_shaft_sleeve','Distal_tapered_optic_nose','Distal_visible_clear_optical_face'))
# Camera points approximately along distal -Y to expose the end window and left side taper.
# No object is hidden or changed; nearby cable segment and sleeve remain within view.
bpy.ops.object.camera_add(location=(3.77,-1.23,1.20));detail=bpy.context.object;detail.name='TEMP_Detail_Camera'
look=Vector((2.92,.25,.50));detail.rotation_euler=(look-detail.location).to_track_quat('-Z','Y').to_euler()
detail.data.type='ORTHO';detail.data.ortho_scale=1.55;scene.camera=detail
scene.render.resolution_x=1200;scene.render.resolution_y=840;scene.render.resolution_percentage=100
out.parent.mkdir(parents=True,exist_ok=True);scene.render.filepath=str(out);bpy.context.view_layer.update();bpy.context.evaluated_depsgraph_get().update()
bpy.ops.render.render(write_still=True)
if not out.exists() or out.stat().st_size<1000:raise RuntimeError('detail render failed')
if hashlib.sha256(source.read_bytes()).hexdigest()!=source_hash:raise RuntimeError('source scene was changed')
rep={'source_blend':str(source),'source_sha256_before_and_after':source_hash,'detail_png':str(out),'detail_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'image_size':[1200,840],'visual_review':'NOT_YET_REVIEWED','scope':'local shape view of the SAME v07 scene geometry; NOT whole-machine or optical validation','view_geometry':'orthographic temporary camera; all existing scene objects/materials unchanged; no blend saved'}
(out.parent/'detail_report.json').write_text(json.dumps(rep,indent=2,ensure_ascii=False));print('DETAIL_RELOAD_RENDER_OK',json.dumps(rep),flush=True)
