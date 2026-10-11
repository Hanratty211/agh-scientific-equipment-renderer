"""Independent saved-scene optical check: evaluated dichroic active mesh world normal,
incident -X and reflected +Z. Also checks visible beam endpoints via v0.6 audit separately.
No Fresnel, power control, ray tracing or sample trapping proof.
blender --background scene_v03.blend --python check_reflection_v03.py -- reflection_audit_v03.json
"""
import bpy,sys,json,math
from pathlib import Path
from mathutils import Vector
out=Path(sys.argv[-1]);o=bpy.data.objects.get('tilted dichroic active plate');deps=bpy.context.evaluated_depsgraph_get();checks=[]
if not o or o.type!='MESH':checks.append({'status':'FAIL','detail':'missing dichroic mesh'})
else:
 ev=o.evaluated_get(deps);mesh=ev.to_mesh()
 try:
  # The optical plate's broad local-YZ face has four vertices and normal predominantly local +/-X.
  broad=max(mesh.polygons,key=lambda p:p.area)
  n=(ev.matrix_world.to_3x3().inverted().transposed()@broad.normal).normalized()
  incident=Vector((-1,0,0));desired=Vector((0,0,1));reflected=incident-2*incident.dot(n)*n
  if reflected.dot(desired)<0:n=-n;reflected=incident-2*incident.dot(n)*n
  dot=reflected.dot(desired);checks.append({'status':'PASS' if dot>.995 else 'FAIL','normal_world':[round(x,6) for x in n],
    'incident_world':list(incident),'computed_reflection_world':[round(x,6) for x in reflected],
    'desired_world':list(desired),'dot':round(dot,6),'face_area_evaluated':broad.area,
    'scope':'one broad evaluated panel face only; no beam propagation through remaining optics'})
 finally:ev.to_mesh_clear()
status='FAIL' if any(c['status']=='FAIL' for c in checks) else 'UNVERIFIED';out.write_text(json.dumps({'status':status,'scene':bpy.data.filepath,'checks':checks},indent=2)+'\n')
print('REFLECTION',status,checks);raise SystemExit(2 if status=='FAIL' else 3)
