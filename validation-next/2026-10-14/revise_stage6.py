"""Stage6 targeted fixes from fourth external visual review; preserve prior saved scenes.
Run Blender -b <parent scene> --python revise_stage6.py -- 13_biomed_optics|14_acoustic_alt|18_mechanical_nature
"""
import bpy,sys,math
from mathutils import Vector
from pathlib import Path
root=Path(__file__).resolve().parent;sys.path.insert(0,str(root))
import render_core as r
r.M.clear()
for mat in bpy.data.materials:
 if mat.name.startswith('MAT_'):r.M[mat.name[4:]]=mat
for k,c in {'dark':(.09,.14,.20),'metal':(.43,.52,.59),'glass':(.46,.72,.78),'soft':(.85,.60,.37),'blue':(.16,.48,.78),'white':(.79,.85,.86)}.items():
 if k not in r.M:
  m=bpy.data.materials.new('MAT_'+k);m.diffuse_color=(*c,1);m.use_nodes=True
  bs=m.node_tree.nodes.get('Principled BSDF')
  if bs:bs.inputs['Base Color'].default_value=(*c,1)
  r.M[k]=m

def rm(n):
 o=bpy.data.objects.get(n)
 if o:bpy.data.objects.remove(o,do_unlink=True)
def bbox(n,axis):
 o=bpy.data.objects[n];a=[(o.matrix_world@Vector(c))[axis] for c in o.bound_box];return min(a),max(a)
def tube(n,pts,rad=.026,mat='blue',evidence='assumption'):
 cu=bpy.data.curves.new(n,'CURVE');cu.dimensions='3D';cu.resolution_u=40;cu.bevel_depth=rad;cu.bevel_resolution=4
 sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(pts)-1)
 for p,xyz in zip(sp.bezier_points,pts):p.co=xyz;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 ob=bpy.data.objects.new(n,cu);bpy.context.collection.objects.link(ob);cu.materials.append(r.M[mat]);return r.tag(ob,evidence)

def optics():
 # Only distal physical silhouette. Keep three separately identified fibers and their rear coupler intact.
 tip=Vector((2.93,.83,.50));shaft=bpy.data.objects['Flexible_scope_outer_tube']
 # v04 short dark cap and annulus were visually rejected, but retain as old version on disk.
 for n in ('Distal_endoscope_head_housing','Distal_optical_end_window','Distal_head_outer_rim'):rm(n)
 # Shaft meets a tapered neck and long slender tip; components overlap at actual world meshes.
 r.cyl('Distal_scope_shaft_sleeve',(2.93,.91,.50),.125,.20,'metal',axis='Y',evidence='assumption')['owner']='Flexible_scope_outer_tube'
 neck=r.cyl('Distal_scope_tapered_neck',(2.93,.73,.50),.106,.28,'dark',axis='Y',evidence='assumption');neck['connector_role']='outer coupling from flexible shaft to distal endoscope housing'
 body=r.cyl('Distal_long_scope_head',(2.93,.45,.50),.095,.42,'dark',axis='Y',evidence='source-visible')
 body['source']='Fig.1a external distal probe silhouette; length/radius illustrative, not exact manufacturer geometry'
 bezel=r.cyl('Distal_front_bezel',(2.93,.225,.50),.105,.045,'metal',axis='Y',evidence='assumption');bezel['owner']=body.name
 win=r.cyl('Distal_optical_front_window',(2.93,.194,.50),.074,.023,'glass',axis='Y',evidence='source-visible');win['owner']=body.name;win['limit']='external optical face only; no rays/internal lens'
 shaft['terminates_in']='Distal_scope_shaft_sleeve';body['back_connector']='Distal_scope_tapered_neck'
 # Keep all distinct Fig1c rear coupler ferrules; no blend with distal optical path.
 for i in range(3):
  fib=bpy.data.objects[f'Flexible_fiber_source_to_probe_{i}'];fib['rear_port_owner']=f'MLE_fiber_plug_{i}'

def acoustics():
 # Fig1b caption explicitly notes drilled hole through Tiny-Lev TOP plate.
 upper=bpy.data.objects['TinyLev_upper_plate'];sample=bpy.data.objects['Levitated_sample_noncontact'];top=bbox('TinyLev_upper_plate',2)
 beam=bpy.data.objects['LDV_to_levitated_sample_sampling_path'];path=beam.data.splines[0]
 x=sample.location.x;y=sample.location.y
 # Cut cylinder spans the actual plate z thickness; boolean applied to editable mesh, not dark decal.
 bpy.ops.mesh.primitive_cylinder_add(vertices=40,radius=.155,depth=.45,location=(x,y,sum(top)/2));cut=bpy.context.object;cut.name='TEMP_top_plate_bore_cutter'
 mod=upper.modifiers.new('Measured_sample_line_of_sight_hole','BOOLEAN');mod.operation='DIFFERENCE';mod.object=cut
 bpy.context.view_layer.objects.active=upper;bpy.context.view_layer.update();bpy.ops.object.modifier_apply(modifier=mod.name);bpy.data.objects.remove(cut,do_unlink=True)
 upper['opening_evidence']='Fig.1b caption drilled hole in Tiny-Lev top plate; radius/shape approximate'
 beam['line_of_sight']='LDV lens → drilled plate aperture → levitated sample top; optical scatter/actual focus unknown'
 ring=r.torus('Top_plate_bore_visible_rim',(x,y,top[1]),.155,.014,'metal',evidence='assumption');ring['physical_owner']=upper.name

def woven():
 # Fig18 left about 20x20 mm visible front silhouette; v03 straight grid was rejected by external pixel review.
 for j in range(7):
  rm(f'PIM_vertical_visible_strand_{j}');rm(f'CIM_cross_visible_strand_{j}')
 x0=-.67;x1=.67;z0=1.42;z1=2.76;ybase=.22
 # Each strand is continuous and sinusoidal IN THE FRONT VIEW; an alternating shallow y-offset
 # lets one strand pass in front of its counterpart at crossings, not a claim of bonded joints.
 for j in range(7):
  x0j=x0+j*(x1-x0)/6
  pts=[]
  for k in range(49):
   t=k/48;z=z0+(z1-z0)*t
   x=x0j+.047*math.sin(2*math.pi*3*t+(j%2)*math.pi)
   yy=ybase+(.037 if ((k//4+j)%2) else -.037)
   pts.append((x,yy,z))
  ob=tube(f'PIM_wavy_visible_strand_{j}',pts,.020,'blue','assumption')
  ob['source']='Supplementary Fig18 left visibly wavy interwoven PIM/CIM face; waveform/pitch illustrative'
  ob['unknown']='third-dimensional depth and crossing linkage not established by photo'
 for j in range(7):
  zj=z0+j*(z1-z0)/6
  pts=[]
  for k in range(49):
   t=k/48;x=x0+(x1-x0)*t
   z=zj+.046*math.sin(2*math.pi*3*t+(j%2)*math.pi)
   yy=ybase+(-.037 if ((k//4+j)%2) else .037)
   pts.append((x,yy,z))
  ob=tube(f'CIM_wavy_cross_strand_{j}',pts,.021,'soft','assumption')
  ob['source']='Fig18 front weave impression, not orthogonal rigid lattice'
  ob['unknown']='crossings are unjoined graphic depth alternations; true joints unknown'
 sc=bpy.context.scene;sc['fig18_domain']='20x20 mm face outline only; internal depth/mesh pitch schematic; Fig19/20 excluded'

CASES={'13_biomed_optics':('v04','v05',optics),'14_acoustic_alt':('v04','v05',acoustics),'18_mechanical_nature':('v03_fig18_PIM_CIM','v04_fig18_woven',woven)}
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
if len(args)!=1 or args[0] not in CASES:raise SystemExit('one supported CASE ID expected')
case=args[0];parent,version,fix=CASES[case]
if bpy.context.scene.get('revision_version')!=parent:raise RuntimeError('unexpected parent scene version')
out=root/'cases'/case/version
if out.exists():raise RuntimeError('refusing overwrite '+str(out))
fix();bpy.context.view_layer.update();sc=bpy.context.scene;sc['revision_version']=version;sc['visual_review']='pending_external_pixel_review';sc['revision_basis']='fourth external human visual review of parent PNG';sc['limit']='illustrative exterior geometry, no internal function or accepted pixel quality'
out.mkdir(parents=True);bpy.ops.wm.save_as_mainfile(filepath=str(out/'scene.blend'));print('STAGE6_SAVED',case,version,flush=True)
