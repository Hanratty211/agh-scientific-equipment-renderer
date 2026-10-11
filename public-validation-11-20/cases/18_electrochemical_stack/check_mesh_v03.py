"""Independent check on SAVED case-18 .blend: polygon topology/open center along Y,
real evaluated mesh versus stage labels. Not a seal, fluid pathway or functional check.
blender --background scene_v03.blend --python check_mesh_v03.py -- mesh_audit_v03.json
"""
import bpy,sys,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
scene=bpy.context.scene;deps=bpy.context.evaluated_depsgraph_get();out=Path(sys.argv[-1]);rows=[]
for n in range(1,18):
 stem=f'position {n:02d} ';objects=[o for o in bpy.data.objects if o.name.startswith(stem) and o.type=='MESH']
 # Exclude decorative channel bars for fundamental central-window membership.
 bars=[o for o in objects if 'visible flow rib' not in o.name];verts=[];faces=[]
 for o in bars:
  ev=o.evaluated_get(deps);mesh=ev.to_mesh()
  try:
   base=len(verts);verts += [ev.matrix_world@v.co for v in mesh.vertices];faces += [tuple(base+i for i in poly.vertices) for poly in mesh.polygons]
  finally:ev.to_mesh_clear()
 if not faces:
  rows.append({'position':n,'status':'UNVERIFIED','reason':'no evaluated mesh polygons'});continue
 tree=BVHTree.FromPolygons(verts,faces,all_triangles=False)
 # Along Y, at visible opening center x=-2.1,z=.66; long ray intersects any falsely solid plate.
 center=Vector((-2.1,-4.3+(n-1)*.455,.66));hit=tree.ray_cast(center,Vector((0,1,0)),1.4)
 expected='SOLID' if n in (1,4,7,8,15,16,17) else 'OPEN'
 actual='SOLID' if hit[0] is not None else 'OPEN'
 rows.append({'position':n,'expected':expected,'actual':actual,'status':'PASS' if actual==expected else 'FAIL',
              'evaluated_mesh_objects':len(bars),'vertices':len(verts),'polygons':len(faces),
              'ray_origin':[round(x,3) for x in center],
              'meaning':'central Y ray only; no crack/seal, noncentral channels or contact verified'})
result={'status':'FAIL' if any(r['status']=='FAIL' for r in rows) else 'UNVERIFIED',
        'scene':bpy.data.filepath,'rows':rows,'not_checked':['physical_layer_identity_15_16','complete_fluid_window_topology','seals','functional_contact','visual_similarity']}
out.write_text(json.dumps(result,indent=2)+'\n');print('MESH_CHECK',result['status'],[(r['position'],r['status']) for r in rows]);raise SystemExit(2 if result['status']=='FAIL' else 3)
