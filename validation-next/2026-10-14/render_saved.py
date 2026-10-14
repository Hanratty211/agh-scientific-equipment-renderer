"""Separate process: reload saved blend, update depsgraph, verify basic status, render.
Usage: blender -b scene.blend --python render_saved.py -- overview.png
No image-quality judgement is made here.
"""
import bpy,sys,json,hashlib
from pathlib import Path
args=sys.argv[sys.argv.index('--')+1:]
if len(args)!=1:raise SystemExit('expected output PNG')
scene=bpy.context.scene
bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();dg.update()
if not scene.camera:raise RuntimeError('missing camera')
objs=[o for o in scene.objects if o.type in ('MESH','CURVE') and o.name!='Backdrop']
if not objs:raise RuntimeError('no physical objects')
if any(o.hide_render for o in objs):raise RuntimeError('critical objects explicitly hide_render')
output=Path(args[0]).resolve();output.parent.mkdir(parents=True,exist_ok=True)
scene.render.filepath=str(output);bpy.ops.render.render(write_still=True)
if not output.exists() or output.stat().st_size<1000:raise RuntimeError('render not written')
file=Path(bpy.data.filepath)
report={'scene':str(file),'scene_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'png':str(output),'png_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'objects':len(objs),'camera':scene.camera.name,'source_basis':scene.get('source_basis'),'render_engine':scene.render.engine,'image_size':[scene.render.resolution_x,scene.render.resolution_y],'visual_review':'NOT_YET_REVIEWED'}
(output.parent/'render_report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False));print('RELOAD_RENDER_OK',json.dumps(report),flush=True)
