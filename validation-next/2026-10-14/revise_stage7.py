"""Stage7: only 13 v06->v07 and 18 Fig18 v04->v05; old versions untouched.
Run Blender -b saved-parent.blend --python revise_stage7.py -- CASE_ID
No inner light path, measured optics, actual weave bonds, or dimensional CAD.
"""
import bpy,sys,math
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parent;sys.path.insert(0,str(root))
import render_core as r
r.M.clear()
for m in bpy.data.materials:
 if m.name.startswith('MAT_'):r.M[m.name[4:]]=m
for k,c in {'dark':(.09,.14,.20),'metal':(.43,.52,.59),'glass':(.46,.72,.78),'soft':(.85,.60,.37),'blue':(.16,.48,.78),'white':(.79,.85,.86)}.items():
 if k not in r.M:
  m=bpy.data.materials.new('MAT_'+k);m.diffuse_color=(*c,1);m.use_nodes=True
  bs=m.node_tree.nodes.get('Principled BSDF')
  if bs:bs.inputs['Base Color'].default_value=(*c,1)
  r.M[k]=m

def rm(n):
 ob=bpy.data.objects.get(n)
 if ob:bpy.data.objects.remove(ob,do_unlink=True)
def smooth_curve(name,pts,rad,mat):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=32;cu.bevel_depth=rad;cu.bevel_resolution=3
 sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(pts)-1)
 for p,co in zip(sp.bezier_points,pts):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 ob=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(ob);cu.materials.append(r.M[mat]);return r.tag(ob,'assumption')

def scope():
 # Preserve three rear fiber curves, rear plug sockets, main flexible shaft and saved v06 probe.
 body=bpy.data.objects['Distal_long_scope_head'];body['source']='Fig1a/g distal exterior identity only; dimensions illustrative'
 # Replace v06 tiny flat glass disk with a face proud of a tapered nose and a visible multilayer bezel.
 for n in ('Distal_front_bezel','Distal_optical_front_window'):rm(n)
 # The v06 physical cylinder points toward -Y; keep long shaft/collar insertion unchanged.
 # Tapered ring via editable conical mesh, not a black decal; larger rear rim fits body.
 from mathutils import Vector
 cx,cz=body.location.x,body.location.z
 # Ring sections at y=-.056 (rear) and -.17 (front): slightly narrower toward viewing face.
 verts=[];faces=[];N=48
 for y,rad in ((-.052,.095),(-.17,.080)):
  for j in range(N):
   a=2*math.pi*j/N;verts.append((cx+rad*math.cos(a),y,cz+rad*math.sin(a)))
 for j in range(N):faces.append((j,(j+1)%N,N+(j+1)%N,N+j))
 mesh=bpy.data.meshes.new('Probe_nose_taper_mesh');mesh.from_pydata(verts,[],faces);mesh.update()
 nose=bpy.data.objects.new('Distal_tapered_optic_nose',mesh);bpy.context.collection.objects.link(nose);nose.data.materials.append(r.M['metal']);r.tag(nose,'assumption')
 nose.modifiers.new('Thin editable housing','SOLIDIFY').thickness=.015
 nose['owner']=body.name;nose['limit']='cone angle and radius illustrative, no internal optical geometry'
 # Optically distinct, concentric protruding outer rim / dark barrel throat / clear visible front face.
 r.cyl('Distal_window_black_throat',(cx,-.174,cz),.078,.030,'dark',axis='Y',evidence='assumption')['owner']=nose.name
 bezel=r.torus('Distal_window_outer_lens_ring',(cx,-.197,cz),.074,.013,'metal',axis='Y',evidence='assumption');bezel['owner']=nose.name
 inner=r.torus('Distal_window_inner_lens_ring',(cx,-.204,cz),.051,.007,'white',axis='Y',evidence='assumption');inner['owner']=nose.name
 glass=r.cyl('Distal_visible_clear_optical_face',(cx,-.210,cz),.057,.016,'glass',axis='Y',evidence='source-visible')
 glass['owner']=nose.name;glass['limit']='visible interface only; transmission/illumination spectrum not claimed'
 body['front_window']='Distal_visible_clear_optical_face';body['rear_connector']='Distal_scope_tapered_neck'
 for i in range(3):
  bpy.data.objects[f'Flexible_fiber_source_to_probe_{i}']['retained']='three independent fibers terminate at existing rear plug; no hidden merge asserted'

def fig18():
 # v04 front weave looked like disconnected rope knots. Remove ONLY fourteen display strands.
 # Plates, compression mounts and Z100 representation remain exactly from saved v04.
 for j in range(7):
  rm(f'PIM_wavy_visible_strand_{j}');rm(f'CIM_wavy_cross_strand_{j}')
 x0,x1=-.67,.67;z0,z1=1.42,2.76;center=.22;count=13
 # Fixed inter-layer offset; no abrupt y flips per point (which made v04 apparent knots).
 # Wavelength keeps curves continuous in front view while visually suggesting a dense weave.
 for j in range(count):
  x=x0+j*(x1-x0)/(count-1);pts=[]
  for k in range(73):
   t=k/72;z=z0+(z1-z0)*t
   xx=x+.019*math.sin(2*math.pi*5*t+j*math.pi/2)
   pts.append((xx,center-.024,z))
  ob=smooth_curve(f'PIM_dense_wavy_{j}',pts,.009,'blue')
  ob['source']='Supplementary Fig18 left dense wavy front-face interwoven PIM/CIM silhouette'
  ob['unknown']='single smooth lane at fixed representative depth; junction bonding and thickness unknown'
 for j in range(count):
  z=z0+j*(z1-z0)/(count-1);pts=[]
  for k in range(73):
   t=k/72;x=x0+(x1-x0)*t
   zz=z+.019*math.sin(2*math.pi*5*t+(j+1)*math.pi/2)
   pts.append((x,center+.024,zz))
  ob=smooth_curve(f'CIM_dense_wavy_{j}',pts,.009,'soft')
  ob['source']='Fig18 left dense smooth front texture, not Fig19/20'
  ob['unknown']='crossing order is representative fixed y layer, not true weave node architecture'
 bpy.context.scene['stage7_note']='13+13 thin continuous waved strands, nearly square 20x20mm visible face only; full thickness and bonds UNVERIFIED'

CASES={'13_biomed_optics':('v06','v07',scope),'18_mechanical_nature':('v04_fig18_woven','v05_fig18_dense_weave',fig18)}
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
if len(args)!=1 or args[0] not in CASES:raise SystemExit('one supported CASE_ID')
case=args[0];parent,version,fix=CASES[case]
if bpy.context.scene.get('revision_version')!=parent:raise RuntimeError('wrong parent version')
out=root/'cases'/case/version
if out.exists():raise RuntimeError('refuse overwrite '+str(out))
fix();bpy.context.view_layer.update();sc=bpy.context.scene;sc['revision_version']=version;sc['visual_review']='pending_external_review';sc['revision_basis']='fifth user-reported external human visual review of saved parent PNG';sc['limits']='Geometry illustrative; no optical propagation, node bonding or functional validation'
out.mkdir(parents=True);bpy.ops.wm.save_as_mainfile(filepath=str(out/'scene.blend'));print('STAGE7_SAVED',case,version,flush=True)
