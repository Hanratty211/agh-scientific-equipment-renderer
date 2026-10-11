"""Codex independent saved-scene geometry probe, not AGH execution evidence."""
import bpy,json
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parents[1]
results={'reviewer':'Codex','scene':bpy.data.filepath,'limitations':'geometry only; no optical physics or pixel verdict'}
dg=bpy.context.evaluated_depsgraph_get()
objects=[(o.name,o.type) for o in bpy.data.objects if 'dichroic' in o.name.lower()]
results['objects']=objects
for name,typ in objects:
 if typ!='MESH' or 'face' not in name:continue
 o=bpy.data.objects[name];eo=o.evaluated_get(dg);me=eo.to_mesh();faces=sorted(me.polygons,key=lambda f:f.area,reverse=True)
 f=faces[0];n=(eo.matrix_world.to_3x3().inverted().transposed()@f.normal).normalized();di=Vector((-1,0,0));ref=di-2*di.dot(n)*n
 results['actual_surface']={'object':name,'normal':list(n),'reflected_minus_x':list(ref),'desired_plus_z':list(Vector((0,0,1))),'direction_error':(ref-Vector((0,0,1))).length}
 eo.to_mesh_clear()
print(json.dumps(results,indent=2));(root/'codex-review/probe_v02_optics_results.json').write_text(json.dumps(results,indent=2))
