"""Independent saved-scene audit; explicit limited scope, no scene mutation."""
import bpy,sys,json,math,hashlib,datetime
import numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.geometry import interpolate_bezier
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
out=Path(sys.argv[sys.argv.index('--')+1]);out.parent.mkdir(parents=True,exist_ok=True)
sc=bpy.context.scene;O=bpy.data.objects;bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();dg.update();checks=[]
def check(id,ok,**data):checks.append(dict(id=id,status='PASS' if ok else 'FAIL',**data))
def bounds(o):
 pts=[o.matrix_world@Vector(v) for v in o.bound_box];return np.array([[min(p[k] for p in pts),max(p[k] for p in pts)] for k in range(3)])
def points(o):
 ps=o.data.splines[0].bezier_points;result=[]
 for a,b in zip(ps,ps[1:]):result.extend(o.matrix_world@v for v in interpolate_bezier(a.co,a.handle_right,b.handle_left,b.co,257)[:-1])
 result.append(o.matrix_world@ps[-1].co);return np.array(result)
def angle(a,b):return math.degrees(math.acos(float(np.clip(np.dot(a,b)/np.linalg.norm(a)/np.linalg.norm(b),-1,1))))
# Evaluated world meshes, not object origins or metadata.
meshes={}
for o in sc.objects:
 if o.type!='MESH' or o.hide_render or o.name.startswith('QA_'):continue
 ev=o.evaluated_get(dg);m=ev.to_mesh();verts=[o.matrix_world@v.co for v in m.vertices];polys=[list(p.vertices) for p in m.polygons]
 meshes[o.name]=BVHTree.FromPolygons(verts,polys,all_triangles=False);ev.to_mesh_clear()
check('six_port_pairs',all(O.get(f'{prefix}_{i}') for prefix in ['Right_panel_fitting','Left_outlet_fitting'] for i in range(6)),expected_pairs=6)
check('unsupported_screens_removed',not any(O.get(f'Pump_{i}_display') for i in range(5)))
rs={n:points(o) for n,o in O.items() if n.startswith(('Blue_inlet_exterior_','Green_outlet_exterior_'))}
check('ten_external_routes',len(rs)==10,actual=len(rs),required=10)
for i in range(5):
 x=.62+.63*i;y=-.69-.18*i
 for col,prefix,start,end,ds,de in [('blue','Blue_inlet_exterior',(x,.09,.85),(-.415,y,.145),(0,-1,0),(-1,0,0)),('green','Green_outlet_exterior',(-1.985,y,.145),(-2.58,y,.145),(-1,0,0),(-1,0,0))]:
  name=f'{prefix}_{i}';p=rs[name];errors=[float(np.linalg.norm(p[0]-start)),float(np.linalg.norm(p[-1]-end))]
  check(name+'.endpoints',max(errors)<.00001,errors=errors,tolerance=.00001,meaning='Coordinates at declared schematic interfaces, not functional connection')
  aa=[angle(p[1]-p[0],np.array(ds)),angle(p[-1]-p[-2],np.array(de))]
  check(name+'.sampled_tangents',max(aa)<2,degrees=aa,tolerance_deg=2)
  # Independent actual mesh nearest-surface query, excluding intended balloon insertion.
  r=O[name].data.bevel_depth;best=(999,None,None)
  skip={f'Green_balloon_schematic_{i}'} if col=='green' else set()
  for mn,tree in meshes.items():
   if mn in skip:continue
   for j,v in enumerate(p):
    hit=tree.find_nearest(Vector(v))
    if hit and hit[0] is not None and hit[3]-r<best[0]:best=(hit[3]-r,mn,j)
  # Sampling only: do not claim exhaustive collision proof.
  check(name+'.sampled_mesh_clearance',best[0]>=-.0001,minimum_surface_gap=best[0],nearest_object=best[1],sample_index=best[2],samples=len(p),tolerance=.0001)
 # Check insertion from actual sleeve bounds, not just written coordinates.
 bb=bounds(O[f'Syringe_hub_connector_{i}']);p=rs[f'Blue_inlet_exterior_{i}'][0]
 check(f'blue{i}.syringe_insertion',.015< p[1]-bb[1,0] <.025,depth=float(p[1]-bb[1,0]),target=.02)
 bb=bounds(O[f'Right_panel_fitting_{i}']);p=rs[f'Blue_inlet_exterior_{i}'][-1]
 check(f'blue{i}.chip_insertion',.015<bb[0,1]-p[0]<.025,depth=float(bb[0,1]-p[0]),target=.02)
 bb=bounds(O[f'Left_outlet_fitting_{i}']);p=rs[f'Green_outlet_exterior_{i}'][0]
 check(f'green{i}.chip_insertion',.015<p[0]-bb[0,0]<.025,depth=float(p[0]-bb[0,0]),target=.02)
 # Real planar mesh hits at the support centre.
 tree=meshes[f'Pump_{i}_frame'];bottom=tree.ray_cast(Vector((x,.6,.1)),Vector((0,0,1)),1)[0]
 top=meshes['Five_syringe_drive_chassis'].ray_cast(Vector((x,.6,.3)),Vector((0,0,-1)),1)[0]
 gap=float(bottom.z-top.z) if bottom is not None and top is not None else None
 check(f'frame{i}.base_contact',gap is not None and abs(gap)<.00001,mesh_surface_gap=gap,tolerance=.00001)
 if i<4:
  gap=float(bounds(O[f'Pump_{i+1}_frame'])[0,0]-bounds(O[f'Pump_{i}_frame'])[0,1]);check(f'frames{i}_{i+1}.clearance',gap>.05,gap=gap)
# Annular opening: axis ray must miss sleeve, offset ray must hit actual wall.
for prefix in ['Right_panel_fitting','Left_outlet_fitting','Syringe_hub_connector']:
 for i in range(6 if 'fitting' in prefix else 5):
  name=f'{prefix}_{i}'
  if name not in meshes:check(name+'.annular_wall',False,reason='missing');continue
  bb=bounds(O[name]);c=bb.mean(axis=1);axis=np.array([0,1,0]) if prefix.startswith('Syringe') else np.array([1,0,0]);origin=c-axis*.2
  hit0=meshes[name].ray_cast(Vector(origin),Vector(axis),.4)[0];hit1=meshes[name].ray_cast(Vector(origin+np.array([0,0,.04])),Vector(axis),.4)[0]
  check(name+'.annular_wall',hit0 is None and hit1 is not None,axial_hole_clear=hit0 is None,wall_hit=hit1 is not None,wall_probe_radius=.04)
# Mesh-plane contact carrier/chip and common bar/frame.
check('chip_carrier_contact',abs(float(bounds(O['Transparent_microfluidic_chip'])[2,0]-bounds(O['Chip_carrier'])[2,1]))<.00001)
check('rack_clasp_attached',bounds(O['Rack_clasp'])[1,1]>=bounds(O['Pump_0_frame'])[1,0] and bounds(O['Rack_clasp'])[1,0]<=bounds(O['Pump_0_frame'])[1,1],method='AABB attachment overlap only; no strength claim')
# Pairwise sampled tube clearance with conservative maximum step correction.
for j,(a,pa) in enumerate(rs.items()):
 for b,pb in list(rs.items())[j+1:]:
  d=float(np.sqrt(np.min(np.sum((pa[:,None,:]-pb[None,:,:])**2,axis=2))));rr=O[a].data.bevel_depth+O[b].data.bevel_depth
  step=float(np.max(np.linalg.norm(np.diff(pa,axis=0),axis=1))+np.max(np.linalg.norm(np.diff(pb,axis=0),axis=1)))/2
  check(a+'__'+b+'.pair_clearance',d-step>rr,minimum_sample_distance=d,conservative_lower_estimate=d-step,sum_radii=rr,method='dense polyline samples; curvature between samples not certified')
# Strict centreline segment crossing in final camera and top projection, blue-blue only.
def crosses(A,B):
 a=A[:-1,None,:];b=A[1:,None,:];c=B[None,:-1,:];d=B[None,1:,:]
 def cr(v,w):return v[...,0]*w[...,1]-v[...,1]*w[...,0]
 return int(np.count_nonzero((cr(b-a,c-a)*cr(b-a,d-a)<-1e-14)&(cr(d-c,a-c)*cr(d-c,b-c)<-1e-14)))
blue={n:p for n,p in rs.items() if n.startswith('Blue')}
for proj in ['top','overview']:
 P={n:p[:,:2] if proj=='top' else np.array([[v.x,v.y] for pt in p for v in [world_to_camera_view(sc,sc.camera,Vector(pt))]]) for n,p in blue.items()}
 for j,(a,pa) in enumerate(P.items()):
  for b,pb in list(P.items())[j+1:]:
   count=crosses(pa,pb);check(a+'__'+b+'.'+proj+'_crossing',count==0,crossings=count)
counts={s:sum(c['status']==s for c in checks) for s in ['PASS','FAIL']}
report={'timestamp':datetime.datetime.now().astimezone().isoformat(),'scene':bpy.data.filepath,'sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'blender':bpy.app.version_string,'counts':counts,'checks':checks,'unverified':['Internal channel connectivity, lumen, leakage/seal and pumping function','Exact manufacturer dimensions/materials/assembly and full drive/control hardware','Exhaustive continuous surface collision, load/strength and complete optical occlusion','User or external human acceptance'], 'pixel_review':'separate qa/PIXEL_REVIEW.md'}
out.write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(counts));print('FAILS',[(c['id'],{k:v for k,v in c.items() if k not in ['id','status']}) for c in checks if c['status']=='FAIL'])
