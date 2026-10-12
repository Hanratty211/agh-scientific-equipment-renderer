"""Codex R5: preserve complete v04 overview (ordered 17 LEFT + assembled RIGHT).
Render THREE auxiliary isolated cell-face views from the SAME unchanged meshes.
Only supplementary render passes temporarily hide unrelated layers; restore all visibility
and overview camera BEFORE saving final scene. No labels, altered identities or routes.
"""
import bpy,math,sys
from pathlib import Path
from mathutils import Vector
p=Path(__file__).resolve().parent
source=p/'scene_v04.blend'
bpy.ops.wm.open_mainfile(filepath=str(source))
scene=bpy.context.scene;cam=scene.camera
assert cam and source.is_file()
# v04 whole-scene composition is retained; no selective hiding in the main view.
assert all(not o.hide_render for o in bpy.data.objects if o.name.startswith('position ') or o.name.startswith('assembled '))
assert sum(any(o.name.startswith(f'position {n:02d} ') for o in bpy.data.objects) for n in range(1,18))==17
assert any(o.name=='assembled rear endplate' for o in bpy.data.objects)
scene.render.resolution_x=1380;scene.render.resolution_y=800
scene.render.filepath=str(p/'overview_v06.png');scene.camera=cam
bpy.ops.render.render(write_still=True)
main_state={o.name:o.hide_render for o in bpy.data.objects if o.type in ('MESH','CURVE')}
# Same v04 modules, incl. their real four-bar frames/contrasting panels/flow lines.
# Camera is nearly face-on, slightly above/side for actual thickness; each detail
# is deliberately supplemental and never substituted for the complete overview.
for n in (12,13,14):
 prefix=f'position {n:02d} ';parts=[o for o in bpy.data.objects if o.name.startswith(prefix) and o.type=='MESH']
 assert len(parts)>=10 and any('inner panel' in o.name for o in parts)
 for o in bpy.data.objects:
  if o.type in ('MESH','CURVE'):
   o.hide_render=not o.name.startswith(prefix)
 y=-3.63+(n-1)*.455
 bpy.ops.object.camera_add(location=(-1.45,y-4.5,1.95));detail=bpy.context.object;detail.name=f'supplement_cell_{n:02d}_camera_v06'
 detail.rotation_euler=(Vector((-2.10,y,.66))-detail.location).to_track_quat('-Z','Y').to_euler();detail.data.type='ORTHO';detail.data.ortho_scale=1.80
 scene.camera=detail;scene.render.resolution_x=900;scene.render.resolution_y=730
 scene.render.filepath=str(p/f'cell_{n:02d}_detail_v06.png')
 bpy.ops.render.render(write_still=True)
 # Delete extra temporary camera after saving its resulting PNG: this is a
 # supplementary look into the identical final saved scene geometry, not a new device.
 bpy.data.objects.remove(detail,do_unlink=True)
 for name,hidden in main_state.items():bpy.data.objects[name].hide_render=hidden
 assert all(bpy.data.objects[name].hide_render==hidden for name,hidden in main_state.items())
# Saved scene has complete geometry with no hidden primary parts and original camera.
scene.camera=cam;scene.render.resolution_x=1380;scene.render.resolution_y=800
scene.render.filepath=str(p/'overview_v06.png')
assert all(not o.hide_render for o in bpy.data.objects if o.name.startswith('position ') or o.name.startswith('assembled '))
bpy.ops.wm.save_as_mainfile(filepath=str(p/'scene_v06.blend'))
