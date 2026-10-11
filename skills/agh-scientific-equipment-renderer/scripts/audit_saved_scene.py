#!/usr/bin/env python3
"""Audit the ALREADY SAVED .blend against an optional v0.6 JSON record.
blender --background final.blend --python audit_saved_scene.py -- record.json --report audit.json
Uses evaluated mesh geometry and actual curve/beam ends. No occlusion, collisions, seals,
physics, transport or image clarity verdict. Exit 0 PASS, 2 FAIL, 3 UNVERIFIED.
"""
import bpy, json, sys, math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

sys.path.insert(0,str(Path(__file__).resolve().parent))
from validate_project_record import validate

args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
if not args:raise SystemExit('record.json required after --')
record=Path(args[0]);out=Path(args[args.index('--report')+1]) if '--report' in args else None
try:data=json.loads(record.read_text(encoding='utf-8'))
except (OSError,ValueError) as e:raise SystemExit(f'record read failed: {e}')
static=validate(data);scene=bpy.context.scene;deps=bpy.context.evaluated_depsgraph_get()
checks=[];unverified=[];failures=[]
def report(code,status,subject,detail):
 checks.append({'code':code,'status':status,'subject':subject,'detail':detail})
 if status=='FAIL':failures.append(code+':'+subject)
 elif status=='UNVERIFIED':unverified.append(code+':'+subject)
def mesh_vertices(obj):
 if obj is None or obj.type!='MESH':return None
 ev=obj.evaluated_get(deps);me=ev.to_mesh()
 try:return [ev.matrix_world@v.co for v in me.vertices]
 finally:ev.to_mesh_clear()
def surface_gap(point,owner):
 """Closest actual evaluated mesh *surface* point, not object origin/bbox.
 BVH nearest face in world coordinates (object transform applied); no contact-normal/force inference.
 """
 from mathutils.bvhtree import BVHTree
 if not owner or owner.type!='MESH':return None
 ev=owner.evaluated_get(deps);me=ev.to_mesh()
 try:
  verts=[ev.matrix_world@v.co for v in me.vertices]
  faces=[tuple(p.vertices) for p in me.polygons]
  if not faces:return None
  tree=BVHTree.FromPolygons(verts,faces,all_triangles=False)
  q=tree.find_nearest(point)
  return (q[0]-point).length if q and q[0] is not None else None
 finally:ev.to_mesh_clear()
def portpoint(name):
 o=bpy.data.objects.get(name)
 if not o:return None
 # Evaluated mesh centroid: transformed real vertices; do not trust arbitrary self-authored anchor properties.
 pts=mesh_vertices(o)
 if not pts:return None
 return sum(pts,Vector())/len(pts)
def endpoint(obj):
 if not obj:return None
 if obj.type=='CURVE':
  if len(obj.data.splines)!=1:return None
  sp=obj.data.splines[0]
  if sp.type=='POLY' and len(sp.points)>1:return (obj.matrix_world@Vector(sp.points[0].co[:3]),obj.matrix_world@Vector(sp.points[-1].co[:3]))
  if sp.type=='BEZIER' and len(sp.bezier_points)>1:return (obj.matrix_world@sp.bezier_points[0].co,obj.matrix_world@sp.bezier_points[-1].co)
  return None
 if obj.type=='MESH':
  # Only a straight cylinder-like mesh with two equal-sized planar caps; no bbox/origin substitute.
  ev=obj.evaluated_get(deps);me=ev.to_mesh()
  try:
   if not me.vertices:return None
   zs=[v.co.z for v in me.vertices];lo=min(zs);hi=max(zs)
   if hi-lo<1e-8:return None
   a=[v.co for v in me.vertices if abs(v.co.z-lo)<1e-6];b=[v.co for v in me.vertices if abs(v.co.z-hi)<1e-6]
   if len(a)<8 or len(a)!=len(b) or len(a)+len(b)!=len(me.vertices):return None
   p=sum(a,Vector())/len(a);q=sum(b,Vector())/len(b)
   # Nonzero equal cap radius and axial separation reject arbitrary box/flat mesh.
   ra=[(v-p).length for v in a];rb=[(v-q).length for v in b]
   if not .000001<sum(ra)/len(ra) or max(ra)-min(ra)>1e-5 or max(rb)-min(rb)>1e-5:return None
   if abs(sum(ra)/len(ra)-sum(rb)/len(rb))>1e-5:return None
   return ev.matrix_world@p,ev.matrix_world@q
  finally:ev.to_mesh_clear()
 return None

components={x['id']:x for x in data.get('components',[]) if isinstance(x,dict) and x.get('id')}
ports={x['id']:x for x in data.get('ports',[]) if isinstance(x,dict) and x.get('id')}
for id_,c in components.items():
 o=bpy.data.objects.get(c.get('object',''))
 report('COMPONENT_OBJECT','PASS' if o else 'FAIL',id_,{'object':c.get('object'),'renders':bool(o and not o.hide_render)})
 if o and o.hide_render:report('COMPONENT_RENDER','FAIL',id_,'hide_render=True')
 elif o:report('COMPONENT_RENDER','PASS',id_,'hide_render=False')
 parent=components.get(c.get('parent')) if c.get('parent') else None
 if parent:
  po=bpy.data.objects.get(parent.get('object',''))
  # Declared parent is assembly identity; do not require Blender parenting, but parent object must exist.
  report('PARENT_OBJECT','PASS' if po else 'FAIL',id_,{'parent':c['parent']})
for id_,p in ports.items():
 a=bpy.data.objects.get(p.get('object',''));owner=components.get(p.get('owner'));obj=bpy.data.objects.get(owner.get('object','')) if owner else None
 if not a or not obj:report('PORT_BINDING','FAIL',id_,{'anchor':bool(a),'owner':bool(obj)});continue
 if a.hide_render:report('PORT_RENDER','FAIL',id_,'hide_render=True')
 point=portpoint(p['object'])
 if point is None:report('PORT_BINDING','UNVERIFIED',id_,'anchor must be an actual mesh with vertices');continue
 tolerance=p.get('surface_tolerance',.03)
 if not isinstance(tolerance,(int,float)) or tolerance<0:report('PORT_BINDING','FAIL',id_,'invalid surface_tolerance');continue
 gap=surface_gap(point,obj)
 report('PORT_OWNER_SURFACE','UNVERIFIED' if gap is None else 'PASS' if gap<=tolerance else 'FAIL',id_,{'gap':gap,'tolerance':tolerance,'point':list(point)})

for conn in data.get('connections',[]):
 if not isinstance(conn,dict) or not conn.get('id'):continue
 id_=conn['id'];a,b=ports.get(conn.get('a')),ports.get(conn.get('b'))
 if not a or not b:continue
 if conn.get('kind') in ('logical','field','temporal'):
  report('NONPHYSICAL_ROUTE','UNVERIFIED',id_,'logical/field/temporal relation not physical endpoint QA');continue
 obj=bpy.data.objects.get(conn.get('object',''))
 if not obj:report('ROUTE_OBJECT','FAIL' if conn.get('required') else 'UNVERIFIED',id_,'route object missing');continue
 report('ROUTE_RENDER','FAIL' if obj.hide_render else 'PASS',id_,{'hide_render':obj.hide_render})
 e=endpoint(obj);pa=portpoint(a.get('object',''));pb=portpoint(b.get('object',''))
 if e is None or pa is None or pb is None:report('ENDPOINTS','UNVERIFIED',id_,'unsupported curve/straight mesh or anchor');continue
 tol=conn.get('tolerance',.03)
 if not isinstance(tol,(float,int)) or tol<0:report('ENDPOINTS','FAIL',id_,'invalid tolerance');continue
 direct=((e[0]-pa).length,(e[1]-pb).length);reverse=((e[1]-pa).length,(e[0]-pb).length)
 gaps=direct if max(direct)<=max(reverse) else reverse
 report('ENDPOINTS','PASS' if max(gaps)<=tol else 'FAIL',id_,{'gaps':gaps,'tolerance':tol,'actual_world_endpoints':[list(x) for x in e]})

for s in data.get('supports',[]):
 if not isinstance(s,dict) or not s.get('id'):continue
 c=components.get(s.get('child'));p=components.get(s.get('parent'))
 if not c or not p:continue
 child=bpy.data.objects.get(c.get('object',''));parent=bpy.data.objects.get(p.get('object',''))
 if not child or not parent:report('SUPPORT_OBJECT','FAIL',s['id'],'missing child/parent');continue
 tol=s.get('tolerance');
 if not isinstance(tol,(int,float)) or tol<0:report('SUPPORT','UNVERIFIED',s['id'],'tolerance absent');continue
 # Evaluate actual child mesh VERTICES vs nearest evaluated parent triangle surface.
 # A mesh vertex may be far from a face interior: passing is limited evidence of contact only.
 pts=mesh_vertices(child)
 if not pts:report('SUPPORT','UNVERIFIED',s['id'],'unsupported child geometry');continue
 gaps=[surface_gap(v,parent) for v in pts];g=min((x for x in gaps if x is not None),default=None)
 report('SUPPORT','UNVERIFIED' if g is None else 'PASS' if g<=tol else 'FAIL',s['id'],{'sampled_vertex_to_surface_min':g,'tolerance':tol,'limitation':'only sampled vertices; no load-bearing proof'})

cam=scene.camera
if not cam:report('CAMERA','UNVERIFIED','scene','no active camera')
else:
 for id_,c in components.items():
  obj=bpy.data.objects.get(c.get('object',''))
  pts=mesh_vertices(obj)
  if not pts:report('PROJECTION','UNVERIFIED',id_,'unsupported/nonmesh geometry');continue
  projections=[world_to_camera_view(scene,cam,v) for v in pts]
  x=[q.x for q in projections];y=[q.y for q in projections]
  depth=[-(cam.matrix_world.inverted()@v).z for v in pts]
  projections_checks=[('CLIP_DEPTH',all(cam.data.clip_start<=d<=cam.data.clip_end for d in depth),[min(depth),max(depth)]),
          ('HORIZONTAL',all(0<=v<=1 for v in x),[min(x),max(x)]),('VERTICAL',all(0<=v<=1 for v in y),[min(y),max(y)])]
  for name,ok,bounds in projections_checks:report(name,'PASS' if ok else 'FAIL',id_,{'bounds':bounds,'camera':cam.name})

if not bpy.data.filepath:unverified.append('SCENE_NOT_SAVED')
if static['status']=='FAIL':failures.append('STATIC_RECORD')
elif static['status']=='UNKNOWN':unverified.append('STATIC_RECORD')
status='FAIL' if failures else 'UNVERIFIED' if unverified or not components or not ports or not data.get('connections') or not data.get('supports') else 'PASS'
result={'status':status,'scene':bpy.data.filepath,'record':str(record),'record_status':static['status'],
        'record_issues':{'errors':static['errors'],'unknown':static['unknown']},'dependent_records':static['dependent_records'],
        'checks':checks,'failures':failures,'unverified':unverified,
        'not_covered':['occlusion','collision','force','fluid_seal','signal_integrity','physical_transport','material_identity','visual_quality'],
        'meaning':'PASS only for declared checks; no scientific/visual acceptance'}
text=json.dumps(result,ensure_ascii=False,indent=2)
if out:out.write_text(text+'\n',encoding='utf-8')
print('AUDIT',status,'FAIL',len(failures),'UNVERIFIED',len(unverified))
raise SystemExit(0 if status=='PASS' else 2 if status=='FAIL' else 3)
