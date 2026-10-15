"""Independent evaluated-mesh shape probes and unchanged-object checks against v07."""
import bpy,sys,json,hashlib,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
scene=Path(bpy.data.filepath).resolve();out=Path(sys.argv[sys.argv.index('--')+1]).resolve()
baseline=Path(__file__).resolve().parent.parent/'robotics/scene.blend'
def snapshot():
 bpy.context.view_layer.update()
 result={}
 for o in bpy.context.scene.objects:
  if o.type!='MESH':continue
  data={'vertices':[list(v.co) for v in o.data.vertices],'polygons':[list(p.vertices) for p in o.data.polygons],'matrix':[list(r) for r in o.matrix_world],'materials':[m.name for m in o.data.materials if m],'visible':not o.hide_render,'bevels':[(m.name,m.width,m.segments) for m in o.modifiers if m.type=='BEVEL']}
  result[o.name]=hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()
 s=bpy.context.scene;c=s.camera
 visual={'camera':[list(r) for r in c.matrix_world],'ortho':c.data.ortho_scale,'engine':s.render.engine,'size':[s.render.resolution_x,s.render.resolution_y,s.render.resolution_percentage],'lights':[(o.name,[list(r) for r in o.matrix_world],o.data.energy,list(o.data.color)) for o in s.objects if o.type=='LIGHT']}
 return result,visual
before_hash=hashlib.sha256(baseline.read_bytes()).hexdigest();after_hash=hashlib.sha256(scene.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(baseline));old,old_visual=snapshot()
bpy.ops.wm.open_mainfile(filepath=str(scene));new,new_visual=snapshot()
bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();dg.update();checks=[]
def check(id,ok,**kwargs):checks.append({'id':id,'status':'PASS' if ok else 'FAIL',**kwargs})
def radii(name,plane):
 o=bpy.data.objects[name];ev=o.evaluated_get(dg);m=ev.to_mesh();verts=[v.co.copy() for v in m.vertices];tree=BVHTree.FromPolygons(verts,[list(p.vertices) for p in m.polygons]);ev.to_mesh_clear();center=o.matrix_world.translation;rs=[]
 for i in range(24):
  angle=2*math.pi*i/24;d=Vector((math.cos(angle),0,math.sin(angle))) if plane=='XZ' else Vector((math.cos(angle),math.sin(angle),0))
  inv=o.matrix_world.inverted();origin=inv@(center+d*2);direction=inv.to_3x3()@(-d)
  hit=tree.ray_cast(origin,direction.normalized(),3)[0];rs.append((o.matrix_world@hit-center).length if hit is not None else None)
 return rs
for lab in ['lower','upper']:
 rs=radii(lab+'_circular_grip_body','XZ');check(lab+'.round_front_section',all(x is not None for x in rs) and max(rs)-min(rs)<.004,radii=rs)
 check(lab+'.larger_grip',all(x is not None for x in rs) and min(rs)>.42,before_radius=.35,minimum_after_radius=min((x for x in rs if x is not None),default=None),radii=rs,scope='User-directed illustrative size increase, not manufacturer measurement')
 rs=radii(lab+'_mount_shaft','XY');check(lab+'.thicker_support',all(x is not None for x in rs) and min(rs)>.165,before_radius=.115,minimum_after_radius=min((x for x in rs if x is not None),default=None),radii=rs)
 rs=radii(('Lower' if lab=='lower' else 'Upper')+'_jaw_carriage','XY');check(lab+'.round_collar_section',all(x is not None for x in rs) and max(rs)-min(rs)<.004,radii=rs)
allowed={f'{lab}_{suffix}' for lab in ['lower','upper'] for suffix in ['circular_grip_body','mount_shaft']}|{'Lower_jaw_carriage','Upper_jaw_carriage'}
changed=[n for n in old if new.get(n)!=old[n]];added=[n for n in new if n not in old]
check('unchanged_non_target_meshes',set(changed)==allowed and not added,changed=changed,added=added)
check('unchanged_camera_lights_render',old_visual==new_visual)
assert hashlib.sha256(scene.read_bytes()).hexdigest()==after_hash and hashlib.sha256(baseline.read_bytes()).hexdigest()==before_hash
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps({'scene':str(scene),'sha256':after_hash,'baseline_sha256':before_hash,'checks':checks,'counts':{s:sum(c['status']==s for c in checks) for s in ['PASS','FAIL']},'scope':'Finite exterior section probes and unchanged-object checks, not physical force or final user acceptance'},indent=2)+'\n')
print({s:sum(c['status']==s for c in checks) for s in ['PASS','FAIL']})

if any(c["status"]=="FAIL" for c in checks):raise SystemExit(1)
