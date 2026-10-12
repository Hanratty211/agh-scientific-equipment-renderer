"""Read-only v06 saved-scene scope + normal-Y gasket aperture checks, and
camera first-hits for each real inner panel with other primary layers visible.
Main overview is not expected to reveal every interior; supplements are isolated.
No operation/seal/quality claim.
"""
import bpy,json,sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
out=Path(sys.argv[-1]);s=bpy.context.scene;deps=bpy.context.evaluated_depsgraph_get();rows=[]
def ray(objs,origin,direction,dist):
 verts=[];faces=[]
 for o in objs:
  ev=o.evaluated_get(deps);mesh=ev.to_mesh()
  try:
   base=len(verts);verts.extend(ev.matrix_world@v.co for v in mesh.vertices)
   faces.extend(tuple(base+i for i in face.vertices) for face in mesh.polygons)
  finally:ev.to_mesh_clear()
 if not faces:return None
 return BVHTree.FromPolygons(verts,faces,all_triangles=False).ray_cast(Vector(origin),Vector(direction),dist)[0] is not None
for n in range(1,18):
 prefix=f'position {n:02d} ';parts=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith(prefix)]
 frame=[o for o in parts if any(o.name.endswith(' '+q) for q in ('left','right','top','bottom'))]
 inner=[o for o in parts if 'inner panel' in o.name]
 basic=[o for o in parts if o not in frame and not any(q in o.name for q in ('flow rib','interior field line','fastener'))]
 y=-3.63+(n-1)*.455;target='SOLID' if n in (1,4,7,8,15,16,17) else 'FRAMED_PANEL' if n in (12,13,14) else 'OPEN_FRAME'
 fh=ray(frame,(-2.10,y-.18,.66),(0,1,0),.36)
 ch=ray(inner if target=='FRAMED_PANEL' else basic,(-2.10,y-.18,.66),(0,1,0),.36)
 valid= (len(frame)==0 and ch is True) if target=='SOLID' else (len(frame)==4 and fh is False and len(inner)==1 and ch is True) if target=='FRAMED_PANEL' else (len(frame)==4 and fh is False and ch in (None,False))
 rows.append({'position':n,'expected':target,'frame_bars':len(frame),'inner_panels':len(inner),'center_frame_hit':fh,'center_base_hit':ch,'status':'PASS' if valid else 'FAIL'})
visible=[o for o in bpy.data.objects if o.name.startswith('position ') or o.name.startswith('assembled ')]
hidden=[o.name for o in visible if o.hide_render];assembled=[o.name for o in visible if o.name.startswith('assembled ')]
cam=s.camera;basis={'location':list(cam.location),'rotation':list(cam.rotation_euler),'ortho_scale':cam.data.ortho_scale,'name':cam.name}
status='FAIL' if hidden or len(rows)!=17 or not assembled or any(r['status']=='FAIL' for r in rows) else 'UNVERIFIED'
out.write_text(json.dumps({'status':status,'scene':bpy.data.filepath,'active_overview_camera':basis,'sampled_layers':rows,'assembled_object_count':len(assembled),'hidden_primary_in_saved_main':hidden,'limits':['one center Y ray per layer','no pixel visibility proof','same meshes but separate detail render states not saved','material identity/assembled sealing unknown']},indent=2)+'\n');print('V06_SAVED_SCOPE',status,'17layers',len(rows),'hidden',len(hidden),'assembled',len(assembled));raise SystemExit(2 if status=='FAIL' else 3)
