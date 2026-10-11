"""Codex independent read-only mesh/route probes. No AGH execution attribution."""
import bpy,json,bmesh
from mathutils import Vector
from pathlib import Path
root=Path(__file__).resolve().parents[1]
results={'reviewer':'Codex','version':'v03','units':'illustrative Blender world units (not metres/mm)','checks':[],'limitations':'targeted checks only; not physics/collision/complete visual acceptance'}
def load(case):
 bpy.ops.wm.open_mainfile(filepath=str(root/'cases'/case/'scene_v03.blend'))
def closest(obj,point):
 eo=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());mw=eo.matrix_world
 ok,co,n,ix=eo.closest_point_on_mesh(mw.inverted()@Vector(point))
 return (mw@co-Vector(point)).length if ok else None
def ends(o):
 s=o.data.splines[0];ps=s.bezier_points if s.type=='BEZIER' else s.points
 return [list(o.matrix_world@Vector(tuple(q.co)[:3])) for q in (ps[0],ps[-1])]
def extents(o):
 vs=[o.matrix_world@v.co for v in o.data.vertices]
 return [max(v[i] for v in vs)-min(v[i] for v in vs) for i in range(3)]
load('11_optical_binding');obj=bpy.data.objects['tilted dichroic active plate'];eo=obj.evaluated_get(bpy.context.evaluated_depsgraph_get());me=eo.to_mesh();face=max(me.polygons,key=lambda p:p.area);n=(eo.matrix_world.to_3x3().inverted().transposed()@face.normal).normalized();di=Vector((-1,0,0));ref=di-2*di.dot(n)*n
results['checks'].append({'case':11,'check':'actual largest dichroic mesh face reflection','normal':list(n),'reflected_minus_x':list(ref),'error_to_plus_z':(ref-Vector((0,0,1))).length});eo.to_mesh_clear()
for line,a,b in [('laser-HWP1 axis','laser output face','half wave plate 1'),('lens2-dichroic axis','collimating lens 2','tilted dichroic active plate'),('dichroic to objective axis','tilted dichroic active plate','objective')]:
 e=ends(bpy.data.objects[line]);results['checks'].append({'case':11,'check':'real endpoint to owner mesh distance','route':line,'owners':[a,b],'endpoints':e,'distances':[closest(bpy.data.objects[a],e[0]),closest(bpy.data.objects[b],e[1])]})
load('15_retractable_sensor')
for o in bpy.data.objects:
 if 'spiral' in o.name.lower() and o.type=='MESH':results['checks'].append({'case':15,'check':'spring actual world extents','object':o.name,'extents':extents(o)})
load('18_electrochemical_stack')
for group in bpy.data.objects:
 if group.type!='EMPTY' or not group.children:continue
 if 'gasket' not in group.name.lower():continue
 pts=[o.matrix_world@v.co for o in group.children if o.type=='MESH' for v in o.data.vertices];center=Vector([sum(p[i] for p in pts)/len(pts) for i in range(3)]);origin=center-Vector((0,2,0));hits=[];topology=[]
 for o in group.children:
  if o.type!='MESH':continue
  mw=o.matrix_world;ok,*_=o.ray_cast(mw.inverted()@origin,(mw.inverted().to_3x3()@Vector((0,1,0))).normalized());
  if ok:hits.append(o.name)
  bm=bmesh.new();bm.from_mesh(o.data);topology.append({'object':o.name,'nonmanifold_edges':sum(not e.is_manifold for e in bm.edges)});bm.free()
 results['checks'].append({'case':18,'check':'gasket center along Y opening and child mesh topology','group':group.name,'center_ray_hit_objects':hits,'topology':topology});break
load('20_thermoelectric_measurement')
for o in bpy.data.objects:
 if 'peltier' in o.name.lower() and o.type=='MESH':results['checks'].append({'case':20,'check':'actual Peltier world extents','object':o.name,'extents':extents(o)})
p=root/'codex-review/probe_v03_results.json';p.write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
