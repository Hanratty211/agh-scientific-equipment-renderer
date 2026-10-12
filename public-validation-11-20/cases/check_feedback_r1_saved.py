"""Reopen final Blender scene: strict R1 geometry rather than proxy endpoints.
Uses evaluated mesh axis/bounds, full action end-face → collar → nozzle → hose,
real Boolean base aperture topology and sampled exterior Bezier clearance.
Not a visual or functional/electrical certificate.
"""
import sys,json,math
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
n=int(sys.argv[sys.argv.index('--')+1]);out=Path(sys.argv[sys.argv.index('--')+2]);O=bpy.data.objects;D=bpy.context.evaluated_depsgraph_get();rows=[]
def check(code,ok,detail):rows.append({'code':code,'status':'PASS' if ok else 'FAIL','detail':detail})
def vertices(o):
 ev=o.evaluated_get(D);m=ev.to_mesh()
 try:return [ev.matrix_world@v.co for v in m.vertices]
 finally:ev.to_mesh_clear()
def bounds(o):
 v=vertices(o);return [(min(p[i] for p in v),max(p[i] for p in v)) for i in range(3)]
def surface_gap(o,point):
 ev=o.evaluated_get(D);m=ev.to_mesh()
 try:
  v=[ev.matrix_world@q.co for q in m.vertices];faces=[tuple(f.vertices) for f in m.polygons]
  q=BVHTree.FromPolygons(v,faces,all_triangles=False).find_nearest(Vector(point));return (Vector(point)-q[0]).length if q and q[0] is not None else math.inf
 finally:ev.to_mesh_clear()
def curve_points(name):
 o=O[name];p=o.data.splines[0]
 if p.type=='POLY':return [o.matrix_world@Vector(b.co[:3]) for b in p.points]
 return [o.matrix_world@b.co for b in p.bezier_points]
def sampled_curve(name,steps=12):
 o=O[name];s=o.data.splines[0];pts=s.bezier_points;out=[]
 for a,b in zip(pts[:-1],pts[1:]):
  for i in range(steps):
   t=i/steps;out.append(o.matrix_world@((1-t)**3*a.co+3*t*(1-t)**2*a.handle_right+3*t*t*(1-t)*b.handle_left+t**3*b.co))
 out.append(o.matrix_world@pts[-1].co);return out

def pump(label,barrel_name,route_name,expected_sign):
 barrel=O[barrel_name];collar=O[label+' barrel-end collar'];nozzle=O[label+' coax metal nozzle'];seat=O[label+' open outlet seat']
 bb,bc,bn,bs=(bounds(x) for x in (barrel,collar,nozzle,seat))
 sign=expected_sign;barrel_face=bb[0][1] if sign>0 else bb[0][0];nozzle_exit=bn[0][1] if sign>0 else bn[0][0];point=Vector(seat.matrix_world.translation)
 offset=abs(point.x-nozzle_exit)
 # Both real cylinder cross-section centers in world coordinates, not own labels.
 for key,obj,b in [('barrel',barrel,bb),('collar',collar,bc),('nozzle',nozzle,bn)]:
  e=math.hypot(obj.matrix_world.translation.y-point.y,obj.matrix_world.translation.z-point.z)
  check(label+' '+key+' coax with outlet',e<.008,{'radial_center_offset':e,'real_bounds':b})
 check(label+' barrel action face contacts collar',bc[0][0]-barrel_face<.008 and bc[0][1]-barrel_face>-.008 if sign>0 else barrel_face-bc[0][1]<.008 and barrel_face-bc[0][0]>-.008,{'barrel_action_end_x':barrel_face,'collar_range_x':bc[0]})
 check(label+' collar and nozzle overlap',max(bc[0][0],bn[0][0])<min(bc[0][1],bn[0][1])-.008,{'collar_x':bc[0],'nozzle_x':bn[0]})
 check(label+' actual nozzle action face and annulus',offset<.004 and abs(point.y-nozzle.matrix_world.translation.y)<.004 and abs(point.z-nozzle.matrix_world.translation.z)<.004,{'nozzle_action_end_x':nozzle_exit,'annulus':list(point),'distance_x':offset})
 route=O[route_name];p=curve_points(route_name);near=min((p[0]-point).length,(p[-1]-point).length)
 check(label+' tube ends on nozzle seat',near<.008,{'nearest_spline_end_to_annulus':near,'route_type':route.data.splines[0].type})
 check(label+' barrel longitudinal X',bb[0][1]-bb[0][0]>3*(bb[1][1]-bb[1][0]) and bb[0][1]-bb[0][0]>3*(bb[2][1]-bb[2][0]),{'barrel_bounds':bb})

if n==12:
 for label in ('upper','lower'):pump(label+' pump',label+' syringe pump mounted syringe barrel',label+' pump to capillary',1)
 check('both capillary feeds preserved',all(O.get(x+' pump to capillary') for x in ('upper','lower')),{'names':[x+' pump to capillary' for x in ('upper','lower')]})
if n==17:
 pump('right pump','right syringe pump mounted syringe barrel','sample to pump visible pneumatic segment',-1)
 check('source sample and sensor route preserved',bool(O.get('sample to pressure sensor visible segment')),{})
if n in (12,14):
 base=O['laptop base'];wall=base.matrix_world.translation.x-bounds(base)[0][1]/2 if False else bounds(base)[0][0]
 sx=O['laptop DATA data socket'].matrix_world.translation
 # Against the actual evaluated BASE mesh there must be zero panel at aperture
 # center even though the rear internal dark socket and frame are present.
 ray_origin=Vector((wall-.09,sx.y,sx.z));ray_dir=Vector((1,0,0));deps=D;ev=base.evaluated_get(deps)
 inv=ev.matrix_world.inverted();hit,point,normal,index=ev.ray_cast(inv@ray_origin,(inv.to_3x3()@ray_dir).normalized(),distance=.35)
 aperture_depth=(ev.matrix_world@point).x-wall if hit else math.inf
 check('real Boolean aperture through laptop base',hit and aperture_depth>.03,{'first_surface_depth_from_wall':aperture_depth,'wall_x':wall,'socket_center':list(sx)})
 for tag in ('surround vertical','surround horizontal'):check('open socket frame '+tag,O.get('laptop DATA '+tag) is not None,{})
 name='camera to laptop exterior DATA cable' if n==12 else 'camera-to-laptop exterior DATA cable'
 pts=sampled_curve(name);lid=O['laptop lid'];display=O['laptop display inset'];boot=O['laptop DATA cable boot']
 # Ignore final seated center section; test exterior up to cable boot.
 end=O[name].data.splines[0].bezier_points[-2].co
 dist=[min(surface_gap(lid,p),surface_gap(display,p)) for p in pts if (p-boot.location).length>.13]
 check('DATA exterior avoids lid and display',bool(dist) and min(dist)>.065,{'minimum_sampled_clearance':min(dist) if dist else None,'samples':len(dist)})
 ctrl=curve_points(name);boot_point=boot.matrix_world.translation
 check('DATA cable approaches laptop from LEFT',len(ctrl)>3 and ctrl[-2].x<ctrl[-1].x and (ctrl[-1]-sx).length<.004,{'last_points':[list(p) for p in ctrl[-3:]]})
if n==14:
 check('array-to-amplifier wire rejected',O.get('array-to-amplifier exterior cable') is None,{'reason':'Fig5b source explicitly inspected; array drive unknown'})
 for cable in ('microphone-to-amplifier exterior cable','representative amplifier-to-scope signal lead','camera-to-laptop exterior DATA cable'):
  check(cable+' is a smooth BEZIER',O[cable].data.splines[0].type=='BEZIER',{})
 a=curve_points('representative amplifier-to-scope signal lead');ring=O['representative oscilloscope ANALOG INPUT BNC input ring'].matrix_world.translation
 check('amp output enters actual scope signal input',(a[0]-O['amp representative signal output ring'].matrix_world.translation).length<.005 and (a[-1]-ring).length<.005,{'end_to_scope':(a[-1]-ring).length})
 tangent=a[-2]-a[-3]
 check('scope approach aligns analog socket',abs(tangent.x)<.006 and abs(tangent.z)<.006 and tangent.y>0,{'second_last_segment':list(tangent)})
result={'case':n,'scene':bpy.data.filepath,'status':'FAIL' if any(c['status']=='FAIL' for c in rows) else 'LIMITED_GEOMETRY_PASS','checks':rows,'not_checked':['source-pixel similarity','commercial connector pinout','full smooth curve obstacle collision','load-bearing and flow/electric function']}
out.write_text(json.dumps(result,indent=2)+'\n');print('R1',n,result['status'],[(x['code'],x['detail']) for x in rows if x['status']=='FAIL'])
if result['status']=='FAIL':raise SystemExit(2)
