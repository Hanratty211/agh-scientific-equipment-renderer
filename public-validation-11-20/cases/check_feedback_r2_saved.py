"""R2 independent reopened-scene checks for 16/19 and six-case render readiness.
Actual saved scene geometry; no pixel approval, CAD identity or functional claim.
blender --background scene.blend --python this.py -- case result.json
"""
import sys,json,math
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
n=int(sys.argv[sys.argv.index('--')+1]);dest=Path(sys.argv[sys.argv.index('--')+2]);O=bpy.data.objects;D=bpy.context.evaluated_depsgraph_get();rows=[]
def check(code,ok,detail):rows.append({'code':code,'status':'PASS' if ok else 'FAIL','detail':detail})
def coords(name):
 o=O[name];sp=o.data.splines[0];return [o.matrix_world@p.co for p in sp.bezier_points]
def nearest(o,pt):
 ev=o.evaluated_get(D);mesh=ev.to_mesh()
 try:
  pts=[ev.matrix_world@v.co for v in mesh.vertices];faces=[tuple(f.vertices) for f in mesh.polygons];q=BVHTree.FromPolygons(pts,faces,all_triangles=False).find_nearest(pt);return (q[0]-pt).length if q and q[0] is not None else math.inf
 finally:ev.to_mesh_clear()
def tangent_end(name):
 b=O[name].data.splines[0].bezier_points;return (b[-1].co-b[-1].handle_left).normalized()
def shape(name):
 o=O.get(name);check(name+' BEZIER',bool(o and o.type=='CURVE' and len(o.data.splines)==1 and o.data.splines[0].type=='BEZIER'),{'type':o.type if o else None})
if n==16:
 for name,mat,z,endname in [('positive HV','red',.81,'chamber red boundary'),('return/ground','mint',.51,'chamber green boundary')]:
  cable=name+' visible external lead';shape(cable);pts=coords(cable)
  plug=O[name+' insulated source plug'];boot=O[name+' short strain relief'];chamber=O[endname]
  check(name+' source plug and cable',(plug.location-pts[0]).length<.03 and nearest(plug,pts[0])<.065,{'plug_center_gap':(plug.location-pts[0]).length,'surface_gap':nearest(plug,pts[0])})
  check(name+' boot seated',(boot.location-pts[0]).length<.075 and (boot.location-pts[1]).length<.075,{'boot_center':list(boot.location),'first_pair':[list(pts[0]),list(pts[1])]})
  check(name+' source tangent axial',abs((pts[1]-pts[0]).x)<.002 and abs((pts[1]-pts[0]).z)<.002 and pts[1].y<pts[0].y,{'axial_departure':list(pts[1]-pts[0])})
  check(name+' ends at existing chamber boundary',(pts[-1]-chamber.location).length<.004,{'dist':(pts[-1]-chamber.location).length})
  check(name+' final axis enters boundary',tangent_end(cable).x>.1 and tangent_end(cable).y>.1,{'final_tangent':list(tangent_end(cable))})
 check('two HV exterior leads only',all(O.get(n+' visible external lead') for n in ('positive HV','return/ground')),{})
if n==19:
 for cable,start,end in [('glass to resistance exterior lead','QA glass left contact','resistance actual terminal ring'),('glass to analog input exterior coax','QA glass right contact','representative Keysight DSOX1204A front ANALOG INPUT BNC input ring')]:
  shape(cable);pts=coords(cable);s=O[start];e=O[end]
  check(cable+' on actual film contact',(pts[0]-s.location).length<.005 and nearest(O['TeRC transparent coating'],pts[0])<.022,{'film_start_gap':nearest(O['TeRC transparent coating'],pts[0])})
  check(cable+' on actual device input',(pts[-1]-e.location).length<.005,{'end_gap':(pts[-1]-e.location).length})
  check(cable+' source-facing final tangent',tangent_end(cable).y>.70 and abs(tangent_end(cable).x)<.02 and abs(tangent_end(cable).z)<.02,{'tangent':list(tangent_end(cable))})
 check('resistor boot exists',O.get('resistance plug strain relief') is not None,{})
 scope=O['representative Keysight DSOX1204A front'];ring=O['representative Keysight DSOX1204A front ANALOG INPUT BNC input ring'];plug=O['representative Keysight DSOX1204A front ANALOG INPUT coax mating shell']
 check('scope ring and plug coaxial',math.hypot(ring.location.x-plug.location.x,ring.location.z-plug.location.z)<.002,{'ring':list(ring.location),'plug':list(plug.location)})
result={'case':n,'scene':bpy.data.filepath,'status':'FAIL' if any(x['status']=='FAIL' for x in rows) else 'LIMITED_GEOMETRY_PASS','checks':rows,'not_checked':['pixel legibility','full path-to-all-body collision','manufacturer terminal pinout','HV clearance safety','electrical operation','hidden flow/electrical paths']}
dest.write_text(json.dumps(result,indent=2)+'\n');print('R2',n,result['status'],[(r['code'],r['detail']) for r in rows if r['status']=='FAIL'])
if result['status']=='FAIL':raise SystemExit(2)
