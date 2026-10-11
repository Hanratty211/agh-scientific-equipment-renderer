"""Read-only v04 saved-stack geometry probe (Blender headless).
Expected: end/film SOLID, gasket/flow aperture OPEN, 12–14 OPEN frame with a
separate *real* contrast panel covering the center. BVH rays follow world +Y.
No identity, membrane permeability, channels away from center or seal proof.
"""
import bpy,json,sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
out=Path(sys.argv[-1]);deps=bpy.context.evaluated_depsgraph_get();rows=[]
def ray(objects,at_y):
 verts=[];faces=[]
 for obj in objects:
  ev=obj.evaluated_get(deps);me=ev.to_mesh()
  try:
   base=len(verts);verts.extend(ev.matrix_world@v.co for v in me.vertices)
   faces.extend(tuple(base+i for i in poly.vertices) for poly in me.polygons)
  finally:ev.to_mesh_clear()
 if not faces:return None
 hit=BVHTree.FromPolygons(verts,faces,all_triangles=False).ray_cast(Vector((-2.1,at_y-.18,.66)),Vector((0,1,0)),.36)
 return hit[0] is not None
for n in range(1,18):
 prefix=f'position {n:02d} ';items=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith(prefix)]
 frame=[o for o in items if any(k in o.name for k in (' left',' right',' top',' bottom')) and 'interior' not in o.name]
 panel=[o for o in items if 'inner panel' in o.name]
 basic=[o for o in items if o not in frame and 'flow rib' not in o.name and 'interior field line' not in o.name and 'fastener' not in o.name]
 y=-3.63+(n-1)*.455;expected='SOLID' if n in (1,4,7,8,15,16,17) else 'FRAME+PANEL' if n in (12,13,14) else 'OPEN'
 open_frame=(ray(frame,y) is False) if frame else None
 center=ray(basic if expected!='FRAME+PANEL' else panel,y)
 if expected=='FRAME+PANEL':
  correct=(len(frame)==4 and len(panel)==1 and open_frame and center is True)
 elif expected=='OPEN':correct=(len(frame)==4 and open_frame and center in (False,None))
 else:correct=(len(frame)==0 and center is True)
 rows.append({'position':n,'expected':expected,'status':'PASS' if correct else 'FAIL',
              'frame_bars':len(frame),'contrast_panels':len(panel),'frame_center_open':open_frame,
              'base_or_panel_center_hit':center,'sampled_world_y':round(y,3),
              'limit':'one center ray, not all hole geometry or seals'})
status='FAIL' if any(r['status']=='FAIL' for r in rows) else 'UNVERIFIED'
result={'status':status,'scene':bpy.data.filepath,'rows':rows,
        'not_covered':['identity_15_16','all_out-of-center_channels','fluid_sealing','visual_similarity']}
out.write_text(json.dumps(result,indent=2)+'\n');print('MESH_V04',status,[(r['position'],r['status']) for r in rows]);raise SystemExit(2 if status=='FAIL' else 3)
