"""Independent read-only screen-space overlap probe of actual v05 saved mesh.
Projects each layer onto overview camera and evaluates whether face sample rays from the
camera hit OWN inner panel first vs another layer. Sampling cannot certify visual clarity.
"""
import bpy,json,sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
out=Path(sys.argv[-1]);scene=bpy.context.scene;cam=scene.camera;deps=bpy.context.evaluated_depsgraph_get()
# The probe tests intersections of real evaluated surfaces, not guessed face location.
verts=[];faces=[];names=[]
for obj in bpy.data.objects:
 if obj.type!='MESH' or not obj.name.startswith('position '):continue
 ev=obj.evaluated_get(deps);me=ev.to_mesh()
 try:
  base=len(verts);verts.extend(ev.matrix_world@v.co for v in me.vertices)
  faces.extend(tuple(base+i for i in poly.vertices) for poly in me.polygons)
  names.extend([obj.name]*len(me.polygons))
 finally:ev.to_mesh_clear()
bvh=BVHTree.FromPolygons(verts,faces,all_triangles=False);rows=[]
for n in (12,13,14):
 y=-4+(n-1)*.50+max(0,n-11)*.37
 x0=-2.10+max(0,n-9)*1.78
 samples=[]
 for x in (x0-.24,x0-.04,x0+.16):
  for z in (.42,.63,.85):
   target=Vector((x,y-.1075,z));screen=world_to_camera_view(scene,cam,target)
   # Sample ray slightly BEHIND near front surface (front is y-.1075). Using a
   # target before the face silently returns None because ray length stops early.
   ray=target-cam.location;face=bvh.ray_cast(cam.location,ray.normalized(),ray.length+.5)
   owner=names[face[2]] if face[2] is not None else None
   samples.append({'target_world':[x,y-.119,z],'screen_uv':[screen.x,screen.y],
     'nearest_mesh':owner,'same_module':bool(owner and owner.startswith(f'position {n:02d} '))})
 count=sum(s['same_module'] for s in samples)
 inside=sum(s['same_module'] and 0<=s['screen_uv'][0]<=1 and 0<=s['screen_uv'][1]<=1 for s in samples)
 rows.append({'position':n,'same_module_first_hit':count,'inside_overview_frame':inside,
  'sample_count':len(samples),'samples':samples,'status':'PASS' if count>=5 and inside>=5 else 'FAIL'})
status='FAIL' if any(r['status']=='FAIL' for r in rows) else 'UNVERIFIED'
out.write_text(json.dumps({'status':status,'scene':bpy.data.filepath,'camera':cam.name,'rows':rows,
 'limits':'mesh-ray sample visibility only, not pixels, contrast, source identity or reader approval'},indent=2)+'\n')
print('VISIBILITY_SAMPLE',status,[(r['position'],r['same_module_first_hit'],r['inside_overview_frame']) for r in rows]);raise SystemExit(2 if status=='FAIL' else 3)
