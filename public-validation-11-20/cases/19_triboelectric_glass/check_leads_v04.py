"""Read-only saved-scene check of both v04 glass lead origins against actual film mesh,
plus route endpoint checks left to v0.6 auditor. Geometry only, no circuit validation.
"""
import bpy,json,sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
out=Path(sys.argv[-1]);film=bpy.data.objects['TeRC transparent coating'];deps=bpy.context.evaluated_depsgraph_get();ev=film.evaluated_get(deps);me=ev.to_mesh()
try:
 verts=[ev.matrix_world@v.co for v in me.vertices];faces=[tuple(p.vertices) for p in me.polygons]
 tree=BVHTree.FromPolygons(verts,faces,all_triangles=False)
 rows=[]
 for side,route in [('left','visible signal to resistance socket'),('right','visible signal to scope socket')]:
  obj=bpy.data.objects[route];sp=obj.data.splines[0];end=obj.matrix_world@Vector(sp.points[0].co[:3]);found=tree.find_nearest(end)
  gap=found[3] if found else None;rows.append({'side':side,'route':route,'actual_world_endpoint':list(end),
   'owner_surface_gap':gap,'status':'PASS' if gap is not None and gap<=.02 else 'FAIL',
   'limit':'distance to finite evaluated film mesh, not optical visibility or signal integrity'})
finally:ev.to_mesh_clear()
status='FAIL' if any(x['status']=='FAIL' for x in rows) else 'UNVERIFIED'
out.write_text(json.dumps({'status':status,'scene':bpy.data.filepath,'rows':rows,'tolerance_world_units':.02},indent=2)+'\n')
print('LEADS',status,[(x['side'],x['owner_surface_gap']) for x in rows]);raise SystemExit(2 if status=='FAIL' else 3)
