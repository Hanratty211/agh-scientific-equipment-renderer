"""Read-only v05 saved-scene sample: 17 ordered layers in illustrative world Y,
true gasket normal-Y center aperture; 12–14 four-bar frames + contrasting real face.
This does NOT prove screen pixel visibility; Codex must read PNGs.
"""
import bpy,json,sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
out=Path(sys.argv[-1]);deps=bpy.context.evaluated_depsgraph_get();rows=[]
def y_of(n):return -4+(n-1)*.50 + max(0,n-11)*.37
def x_of(n):return -2.10 + max(0,n-9)*1.78
def hit(objects,n):
 verts=[];faces=[]
 for obj in objects:
  ev=obj.evaluated_get(deps);mesh=ev.to_mesh()
  try:
   base=len(verts);verts.extend(ev.matrix_world@v.co for v in mesh.vertices)
   faces.extend(tuple(base+i for i in poly.vertices) for poly in mesh.polygons)
  finally:ev.to_mesh_clear()
 if not faces:return None
 return BVHTree.FromPolygons(verts,faces,all_triangles=False).ray_cast(Vector((x_of(n),y_of(n)-.18,.66)),Vector((0,1,0)),.36)[0] is not None
for n in range(1,18):
 name=f'position {n:02d} ';objects=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith(name)]
 bars=[o for o in objects if any(o.name.endswith(' '+k) for k in ('left','right','top','bottom'))]
 panel=[o for o in objects if 'inner panel' in o.name]
 basic=[o for o in objects if o not in bars and not any(q in o.name for q in ('flow rib','interior field line','fastener'))]
 expected='SOLID' if n in (1,4,7,8,15,16,17) else 'FRAME_WITH_FACE' if n in (12,13,14) else 'OPEN_FRAME'
 frame_ray=hit(bars,n);center=hit(panel if expected=='FRAME_WITH_FACE' else basic,n)
 if expected=='FRAME_WITH_FACE':valid=len(bars)==4 and len(panel)==1 and frame_ray is False and center is True
 elif expected=='OPEN_FRAME':valid=len(bars)==4 and frame_ray is False and center in (None,False)
 else:valid=len(bars)==0 and center is True
 rows.append({'position':n,'world_x':x_of(n),'world_y':y_of(n),'expected':expected,'bars':len(bars),'face_panels':len(panel),
  'frame_center_ray_hit':frame_ray,'panel_or_base_ray_hit':center,'status':'PASS' if valid else 'FAIL'})
spacings=[round(y_of(n+1)-y_of(n),5) for n in range(1,17)];ordered=all(g>0 for g in spacings)
status='FAIL' if not ordered or any(r['status']=='FAIL' for r in rows) else 'UNVERIFIED'
result={'status':status,'scene':bpy.data.filepath,'rows':rows,'ordered':ordered,
 'adjacent_exploded_display_spacings_world_units':spacings,
 'sampling_limit':'one center ray per position; no seal, out-of-center channel, true assembly distance, or image occlusion proof',
 'ambiguous':['position15 unresolved','position16 caption conflict']}
out.write_text(json.dumps(result,indent=2)+'\n');print('MESH_V05',status,'layers',len(rows),'ordered',ordered);raise SystemExit(2 if status=='FAIL' else 3)
