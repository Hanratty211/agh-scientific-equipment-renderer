"""Independent-ish geometry interrogation of saved batch scenes.
Blender command: blender --background scene.blend --python this.py -- record.json report.json
No hidden physical function or visual acceptance claims. Computation reopens a .blend.
"""
import sys,json,math
from pathlib import Path
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree
args=sys.argv[sys.argv.index('--')+1:];record=json.loads(Path(args[0]).read_text());out=Path(args[1]);checks=[]
scene=bpy.context.scene;deps=bpy.context.evaluated_depsgraph_get();objs=bpy.data.objects

def check(code,item,ok,detail):checks.append(dict(check=code,item=item,status='PASS' if ok else 'FAIL',detail=detail))
def bbox(obj):
 return [obj.matrix_world@Vector(c) for c in obj.bound_box]
def nearest(pt,obj):
 ev=obj.evaluated_get(deps);mesh=ev.to_mesh()
 try:
  vert=[ev.matrix_world@v.co for v in mesh.vertices];poly=[tuple(p.vertices) for p in mesh.polygons]
  q=BVHTree.FromPolygons(vert,poly,all_triangles=False).find_nearest(Vector(pt));return (q[0]-Vector(pt)).length if q and q[0] is not None else None
 finally:ev.to_mesh_clear()
# Bounding boxes are broad-phase only; exact mesh nearest distances for key interfaces.
for c in record['components']:
 name=c['object'];o=objs.get(name);check('component_exists',c['id'],o is not None,{'object':name})
for p in record['ports']:
 o=objs.get(p['object']);check('port_exists',p['id'],o is not None,{'object':p['object']})
# Mechanical hinge/lid root and base bounds, source owner ties.
for prefix in ('laptop','adjacent laptop'):
 base=objs.get(prefix+' base');lid=objs.get(prefix+' lid');axle=objs.get(prefix+' full hinge axle')
 if not base and not lid:continue
 check('clamshell_presence',prefix,bool(base and lid and axle),{'base':bool(base),'lid':bool(lid),'axle':bool(axle)})
 if base and lid and axle:
  lo=min(v.z for v in bbox(lid));xlo=min(v.x for v in bbox(base));xhi=max(v.x for v in bbox(base))
  hinge=axle.matrix_world.translation
  check('hinge_root_height',prefix,abs(lo-hinge.z)<.085,{'lid_min_z':lo,'axle_z':hinge.z,'delta':lo-hinge.z})
  check('hinge_on_base',prefix,xlo<=hinge.x<=xhi and nearest(hinge,base)<.10,{'axle_point':list(hinge),'gap_to_base':nearest(hinge,base)})
  check('keys_touchpad_display',prefix,bool(objs.get(prefix+' key') and objs.get(prefix+' touchpad') and objs.get(prefix+' display inset')),{})
  if objs.get(prefix+' representative DATA receptacle'):
   socket=objs[prefix+' representative DATA receptacle'];plug=objs.get(prefix+' DATA seated data plug')
   check('laptop_seated_plug_exists',prefix,plug is not None,{'socket':socket.name,'plug':plug.name if plug else None})
   if plug:
    check('socket_plug_proximity',prefix,nearest(socket.matrix_world.translation,plug)<.027,{'mesh_gap':nearest(socket.matrix_world.translation,plug)})
# Verify analog input/plug alignment on actual meshes, not name/role alone.
for c in record['components']:
 name=c['object'];name_signal=name+' ANALOG INPUT';ring=objs.get(name_signal+' BNC input ring');plug=objs.get(name_signal+' coax mating shell');boot=objs.get(name_signal+' plug strain relief')
 if not ring:continue
 check('analog_parts',name,bool(plug and boot),{'ring':ring.name,'plug':plug.name if plug else None})
 if not plug or not boot:continue
 p,q=ring.matrix_world.translation,plug.matrix_world.translation
 v=q-p;rad=abs(v.y);lateral=math.hypot(v.x,v.z)
 check('analog_coaxial',name,lateral<.002 and rad<.085,{'axial':rad,'lateral':lateral})
 front=name.rsplit(' ANALOG INPUT',1)[0];body=objs.get(front)
 if body:
  f=min(v.y for v in bbox(body));check('input_at_front_not_screen',front,abs(p.y-f)<.065,{'input_y':p.y,'body_front_y':f})
 route_name='representative amplifier-to-scope signal lead' if 'oscilloscope' in name else 'glass to analog input exterior coax'
 route=objs.get(route_name)
 if route and route.type=='CURVE':
  points=[route.matrix_world@Vector(k.co[:3]) for k in route.data.splines[0].points];delta=points[-2]-points[-3];branch=points[-1]-points[-2]
  check('coax_approaches_input_axis',name,abs(delta.y)>max(abs(delta.x),abs(delta.z))*.7 and branch.y>0,{'approach':list(delta),'final_to_socket':list(branch)})
# Numeric/mesh test does not claim image pixels, exact CAD, ground/current, or connection function.
result={'scene':bpy.data.filepath,'record':str(Path(args[0]).resolve()),'status':'FAIL' if any(c['status']=='FAIL' for c in checks) else 'LIMITED_GEOMETRY_PASS','checks':checks,'not_checked':['actual pixels','hidden circuits','manufacturer CAD','electrical or pneumatic functionality','unmodeled support contacts']}
out.write_text(json.dumps(result,indent=2)+'\n');print('PHYSICAL',result['status'],'FAIL',sum(c['status']=='FAIL' for c in checks))
if result['status']=='FAIL':raise SystemExit(2)
