"""Frozen, finite evaluated-mesh probes for the schematic gripping assembly. Not force/FEA."""
import bpy,sys,json,hashlib,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
out=Path(sys.argv[sys.argv.index('--')+1]);sc=bpy.context.scene;O=bpy.data.objects
bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();dg.update();trees={};bs={};checks=[]
for o in sc.objects:
 if o.type!='MESH' or o.hide_render:continue
 ev=o.evaluated_get(dg);m=ev.to_mesh();vs=[ev.matrix_world@v.co for v in m.vertices]
 trees[o.name]=BVHTree.FromPolygons(vs,[list(p.vertices) for p in m.polygons]);bs[o.name]=[(min(v[k] for v in vs),max(v[k] for v in vs)) for k in range(3)];ev.to_mesh_clear()
def check(id,ok,**data):checks.append({'id':id,'status':'PASS' if ok else 'FAIL',**data})
def hit(n,origin,direction,distance=10):
 t=trees.get(n)
 return t.ray_cast(Vector(origin),Vector(direction),distance)[0] if t else None
def interface(id,a,b,x,y,z,tolerance=.015):
 # Probe actual bottom surface of upper object and top surface of lower object.
 low=hit(a,(x,y,z+5),(0,0,-1));high=hit(b,(x,y,z-5),(0,0,1))
 gap=float(high.z-low.z) if low is not None and high is not None else None
 check(id,gap is not None and -.13<=gap<=tolerance,surface_gap=gap,allowed_schematic_overlap=.13,max_gap=tolerance,method='opposite evaluated-mesh surface rays at declared contact section')
required=['Testing_machine_lower_frame','Testing_machine_upper_frame','Linear_guide_-1','Linear_guide_1','Lower_jaw_carriage','Upper_jaw_carriage','lower_circular_grip_body','upper_circular_grip_body','Soft_coupon_lower_clamped','Soft_coupon_upper_clamped']+[f'{lab}_jaw_at_{y}' for lab in ['lower','upper'] for y in [-.13,.13]]
check('required_original_components',all(n in trees for n in required),required=required)
for lab in ['lower','upper']:
 name=f'{lab}_circular_grip_body';o=O.get(name)
 axis=(o.matrix_world.to_3x3()@Vector((0,0,1))).normalized() if o else Vector((0,0,0))
 check(lab+'.disc_faces_front',abs(axis.y)>.99,axis=list(axis),source='round grip face visible in photo, plane XZ')
 coupon=f'Soft_coupon_{lab}_clamped';cb=bs[coupon]
 for side,y in [('front',-.13),('back',.13)]:
  jaw=f'{lab}_jaw_at_{y}';jb=bs[jaw];overlap=min(cb[2][1],jb[2][1])-max(cb[2][0],jb[2][0]);check(f'{lab}.{side}.axial_insertion',overlap>.15,overlap=overlap,min_required=.15)
  z=(max(cb[2][0],jb[2][0])+min(cb[2][1],jb[2][1]))/2
  gaps=[]
  for x in [-.025,0,.025]:
   sign=-1 if side=='front' else 1
   cp=hit(coupon,(x,sign*2,z),(0,-sign,0));jp=hit(jaw,(x,0,z),(0,sign,0))
   gaps.append(float(sign*(jp.y-cp.y)) if cp is not None and jp is not None else None)
  check(f'{lab}.{side}.working_surface',all(g is not None and -.01<=g<=.01 for g in gaps),sampled_gaps=gaps,tolerance=.01,method='3 actual mesh rays, small schematic interference permitted, no clamping force claim')
  # Mesh collision at mounting region demonstrates finite solid attachment, not mere bbox overlap.
  candidates=[jaw,name]+[f'{lab}_jaw_outer_rail_{i}' for i in (0,1)]
  candidates=[n for n in candidates if n in trees];edges=[]
  for i,a in enumerate(candidates):
   for b in candidates[i+1:]:
    if trees[a].overlap(trees[b]):edges.append([a,b])
  reachable={jaw}
  for _ in candidates:
   for a,b in edges:
    if a in reachable or b in reachable:reachable.update((a,b))
  check(f'{lab}.{side}.jaw_body_attachment',name in reachable,mesh_intersection_edges=edges,scope='actual finite solid attachment path directly or via existing outer rails; no force/fastening proof')
 mount='Lower_jaw_carriage' if lab=='lower' else 'Upper_jaw_carriage'
 collision=trees[mount].overlap(trees[name]);check(lab+'.body_carriage_attachment',bool(collision),intersecting_face_pairs=len(collision))
interface('coupon.join','Soft_coupon_lower_clamped','Soft_coupon_upper_clamped',0,0,1.25,tolerance=.001)
# Reject hidden 0.135-unit overlapping slabs instead of accepting any overlap.
l=bs['Soft_coupon_lower_clamped'];u=bs['Soft_coupon_upper_clamped'];check('coupon.no_double_layer',abs(u[2][0]-l[2][1])<=.001,gap=u[2][0]-l[2][1],tolerance=.001)
check('coupon.upper_segment_longer',u[2][1]-u[2][0]>1.5*(l[2][1]-l[2][0]),scope='qualitative photo proportion; not exact length')
for lab,low,high in [('lower','Testing_machine_lower_frame','Lower_jaw_carriage'),('upper','Upper_jaw_carriage','Testing_machine_upper_frame')]:
 mount=lab+'_mount_shaft';check(lab+'.mount_exists',mount in trees)
 interface(lab+'.mount_bottom',low,mount,0,.20,1)
 interface(lab+'.mount_top',mount,high,0,.20,1)
for x in [-1,1]:
 guide=f'Linear_guide_{x}'
 interface(f'guide{x}.lower_frame','Testing_machine_lower_frame',guide,x,0,0)
 interface(f'guide{x}.upper_frame',guide,'Testing_machine_upper_frame',x,0,3)
check('all_required_visible',all(O[n].hide_render is False for n in required))
check('no_unverified_model_or_force_label',not any(o.type=='FONT' for o in O),scope='no numerical/manufacturer label added; not semantic scan')
path=Path(bpy.data.filepath).resolve();counts={s:sum(c['status']==s for c in checks) for s in ['PASS','FAIL']}
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps({'scene':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'checks':checks,'counts':counts,'scope':'Finite schematic geometry probes, evaluated meshes; excludes strength, sealing, manufacturer identity and exact dimensions'},indent=2)+'\n');print(counts)
