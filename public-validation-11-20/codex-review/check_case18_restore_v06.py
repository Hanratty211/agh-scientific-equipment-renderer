"""Codex independent saved-scene restore comparison and genuine pixel bytes digest."""
import bpy,hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parents[1];case=root/'cases/18_electrochemical_stack'
def snapshot(v):
 bpy.ops.wm.open_mainfile(filepath=str(case/f'scene_{v}.blend'))
 rows={}
 for o in bpy.data.objects:
  if o.type not in ('MESH','CURVE','EMPTY'):continue
  raw={'type':o.type,'world':[list(row) for row in o.matrix_world],'hide_render':o.hide_render}
  if o.type=='MESH':raw.update(vertices=[list(x.co) for x in o.data.vertices],faces=[list(x.vertices) for x in o.data.polygons])
  rows[o.name]=hashlib.sha256(json.dumps(raw,sort_keys=True).encode()).hexdigest()
 return rows,bpy.context.scene.camera.name if bpy.context.scene.camera else None
before,cam0=snapshot('v04');after,cam1=snapshot('v06');changed=[n for n in before if after.get(n)!=before[n]];missing=sorted(set(before)-set(after));new=sorted(set(after)-set(before))
r={'reviewer':'Codex','geometry_and_render_state_reference':'scene_v04.blend','final':'scene_v06.blend','matched_physical_objects':len(before)-len(changed),'changed_or_missing_objects':changed,'missing':missing,'extra_non_camera_objects':new,'camera_before':cam0,'camera_after':cam1,'output_hashes':{n:hashlib.sha256((case/n).read_bytes()).hexdigest() for n in ('overview_v04.png','overview_v06.png','cell_12_detail_v06.png','cell_13_detail_v06.png','cell_14_detail_v06.png')},'limitations':'equal physical mesh/transform/hide_render inventory is not materials/functional/occlusion certification; actual PNGs externally inspected separately'}
(root/'codex-review/case18_restore_v06_results.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));assert not changed and not missing and not new
