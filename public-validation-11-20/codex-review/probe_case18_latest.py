"""Codex independent camera rays to actual repeated cell-face geometry, read-only."""
import bpy,json,sys
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parents[1]
version=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'v05'
scene=root/'cases/18_electrochemical_stack'/f'scene_{version}.blend'
bpy.ops.wm.open_mainfile(filepath=str(scene));dg=bpy.context.evaluated_depsgraph_get();cam=bpy.context.scene.camera;rows=[]
for n in (12,13,14):
 target=next(o for o in bpy.data.objects if o.name.startswith(f'position {n:02d}') and o.name.endswith('inner panel'))
 mw=target.matrix_world;vs=[mw@v.co for v in target.data.vertices];center=sum(vs,Vector())/len(vs);normal=(mw.to_3x3().inverted().transposed()@Vector((0,-1,0))).normalized()
 # Face points slightly biased to camera-facing Y face, not arbitrary stored attributes.
 face_y=min(v.co.y for v in target.data.vertices)
 samples=[]
 for fx in (-.20,0,.20):
  for fz in (-.15,0,.15):
   point=mw@Vector((fx,face_y,fz));direction=(point-cam.matrix_world.translation).normalized();hit,loc,norm,idx,obj,mat=bpy.context.scene.ray_cast(dg,cam.matrix_world.translation,direction,distance=(point-cam.matrix_world.translation).length+.001)
   same=bool(hit and obj and obj.name.startswith(f'position {n:02d}') and (obj.name==target.name or 'interior field line' in obj.name))
   samples.append({'point':list(point),'first_hit':obj.name if hit and obj else None,'inner_panel_or_pattern_hit':same})
 rows.append({'position':n,'target':target.name,'visible_samples':sum(x['inner_panel_or_pattern_hit'] for x in samples),'sample_count':len(samples),'samples':samples})
r={'reviewer':'Codex','scene':str(scene),'camera':cam.name,'rows':rows,'limits':'nine sampled opaque-geometry rays per face only; transparent visibility/whole face/pixel quality not inferred'}
(root/'codex-review'/f'probe_case18_{version}_results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
