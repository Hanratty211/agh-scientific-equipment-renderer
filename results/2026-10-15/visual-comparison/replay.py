"""Post-freeze replay of a trial scene. Does not alter design or feed candidates new images."""
import bpy,sys,json,hashlib,time
from pathlib import Path
args=sys.argv[sys.argv.index('--')+1:];out=Path(args[0]).resolve();out.mkdir(parents=True,exist_ok=False)
s=bpy.context.scene;src=Path(bpy.data.filepath).resolve();before=hashlib.sha256(src.read_bytes()).hexdigest()
settings={'engine':s.render.engine,'device':s.cycles.device,'samples':s.cycles.samples,'seed':s.cycles.seed,'denoise':s.cycles.use_denoising,'width':s.render.resolution_x,'height':s.render.resolution_y,'percentage':s.render.resolution_percentage}
expected={'engine':'CYCLES','device':'CPU','samples':64,'seed':7,'denoise':True,'width':1800,'height':1280,'percentage':100}
report={'scene':str(src),'scene_sha256':before,'settings':settings,'settings_match':settings==expected,'started_at':time.time(),'objects':len(s.objects),'geometry_mutated':False}
(out/'settings.json').write_text(json.dumps(report,indent=2)+'\n')
if settings!=expected:raise RuntimeError('Trial render settings differ from frozen protocol; retained, not silently corrected')
bpy.context.view_layer.update();bpy.context.evaluated_depsgraph_get().update();s.render.filepath=str(out/'reloaded.png');bpy.ops.render.render(write_still=True)
report.update(seconds=time.time()-report['started_at'],scene_unchanged=before==hashlib.sha256(src.read_bytes()).hexdigest(),png_sha256=hashlib.sha256((out/'reloaded.png').read_bytes()).hexdigest());(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');assert report['scene_unchanged']
