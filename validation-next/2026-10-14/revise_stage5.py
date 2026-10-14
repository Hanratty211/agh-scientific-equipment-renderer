"""Third external review: small, non-destructive changes to saved scenes.
Run Blender -b CASE/parent/scene.blend --python revise_stage5.py -- CASE_ID.
Each function checks its parent revision; no old scene is overwritten.
"""
import bpy,sys,math
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parent;sys.path.insert(0,str(root))
import render_core as r
r.M.clear()
for m in bpy.data.materials:
 if m.name.startswith('MAT_'):r.M[m.name[4:]]=m

def mat(k,c):
 if k not in r.M:
  m=bpy.data.materials.new('MAT_'+k);m.diffuse_color=(*c,1);m.use_nodes=True
  bs=m.node_tree.nodes.get('Principled BSDF')
  if bs:bs.inputs['Base Color'].default_value=(*c,1)
  r.M[k]=m
for k,c in {'metal':(.43,.52,.59),'dark':(.09,.14,.20),'soft':(.85,.60,.37),'blue':(.16,.48,.78),'red':(.75,.25,.20),'white':(.79,.85,.86),'black':(.03,.04,.06),'copper':(.60,.34,.18),'glass':(.46,.72,.78),'base':(.22,.30,.36)}.items():mat(k,c)
def rm(n):
 ob=bpy.data.objects.get(n)
 if ob:bpy.data.objects.remove(ob,do_unlink=True)
def box(n,p,s,m='metal',e='assumption'):return r.box(n,p,s,m,e,bevel=.014)
def cyl(n,p,rad,dep,m='metal',axis='Z',ev='assumption'):return r.cyl(n,p,rad,dep,m,axis,evidence=ev)
def tube(n,points,radius=.025,material='dark',ev='assumption'):
 cu=bpy.data.curves.new(n,'CURVE');cu.dimensions='3D';cu.resolution_u=40;cu.bevel_depth=radius;cu.bevel_resolution=4
 sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
 for p,xyz in zip(sp.bezier_points,points):p.co=xyz;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 ob=bpy.data.objects.new(n,cu);bpy.context.collection.objects.link(ob);cu.materials.append(r.M[material]);return r.tag(ob,ev)
def seg(n,a,b,rad=.035,m='metal',ev='assumption'):return r.segment(n,a,b,rad,m,ev)
def look(pos,target,size):
 for o in list(bpy.data.objects):
  if o.type=='CAMERA':bpy.data.objects.remove(o,do_unlink=True)
 r.camera(pos,target,size)
def mesh_limits(n,axis):
 ob=bpy.data.objects[n];v=[(ob.matrix_world@x.co)[axis] for x in ob.data.vertices];return min(v),max(v)

def robot():
 # v04 actual column beam remains; only opposing working surfaces change.
 for label in ('lower','upper'):
  coupon=bpy.data.objects[f'Soft_coupon_{label}_clamped']
  z=.77 if label=='lower' else 2.39
  for y in (-.13,.13):
   jaw=bpy.data.objects[f'{label}_jaw_at_{y}']
   jaw.dimensions=(.36,.15,.32);jaw.location=(0,y,z)
   jaw['owner']=f'{label}_circular_grip_body'
   jaw['face_note']='opposed flat jaw reaches coupon face; normal-force magnitude unknown'
  for j,x in enumerate((-.13,.13)):
   rib=box(f'{label}_jaw_outer_rail_{j}',(x,0,z),(.035,.37,.26),'dark')
   rib['identity']='visible clamping assembly outline, not a separate specimen'
  coupon['gripped_end_note']='finite z overlap and lateral opposing near-face; no proven clamping load'
 look((5.3,-8,4.5),(0,0,1.57),6.2)

def optics():
 # Fig.1a depicts a recognizable soft scope with distal window; Fig.1c the distinct rear 3-fiber coupler.
 # v03 terminal was only a metal annulus with no closed head; keep shaft but add physical distal housing.
 tip=Vector((2.93,.83,.50))
 rm('Distal_viewing_annulus')
 body=cyl('Distal_endoscope_head_housing',tuple(tip),.135,.30,'dark',axis='Y',ev='source-visible')
 body['evidence_detail']='Fig.1a distal viewing head silhouette; exact size/optical elements schematic'
 window=cyl('Distal_optical_end_window',(tip.x,tip.y-.166,tip.z),.092,.022,'glass',axis='Y',ev='source-visible')
 window['owner']=body.name;window['function_limit']='outer transparent window only, no ray/optical transmission asserted'
 rim=r.torus('Distal_head_outer_rim',(tip.x,tip.y-.178,tip.z),.112,.018,'metal',axis='Y',evidence='assumption');rim['owner']=body.name
 # Rear coupler already exists, fit each independent fiber into a separate visible ferrule/plug.
 for i,x in enumerate((.85,1.15,1.45)):
  plug=bpy.data.objects[f'MLE_fiber_plug_{i}'];collar=bpy.data.objects[f'Coupler_visible_collar_{i}']
  plug['owner']='Colonoscopic_coupler';plug['inserted_through']='Coupler_visible_collar_'+str(i)
  collar['owner']='Colonoscopic_coupler';collar['status']='external metal sleeve, no asserted internal port geometry'
 # The shaft is still an outer tube. Its visible endpoint interpenetrates the distal housing.
 shaft=bpy.data.objects['Flexible_scope_outer_tube'];shaft['terminates_in']=body.name
 look((5.5,-8.6,5.6),(-.05,0,1.38),8.1)

def acoustics():
 # v03 dashes falsely read as hitting platform. No permanent physical beam colour or ray trace claimed.
 for i in range(4):rm(f'LDV_sampling_axis_{i}')
 sample=bpy.data.objects['Levitated_sample_noncontact'];sx,sy,sz=sample.location
 lens=bpy.data.objects['LDV_front_lens']
 lens['optic_axis']='vertical -Z toward top-center of levitated sample; no mechanical support'
 # Segments with small gaps for a sampling-path overlay; terminate visibly at the sample top surface.
 top=mesh_limits(sample.name,2)[1];front=mesh_limits(lens.name,2)[0]
 path=tube('LDV_to_levitated_sample_sampling_path',[(sx,sy,front),(sx,sy,2.56),(sx,sy,2.20),(sx,sy,1.88),(sx,sy,top)],.010,'red','assumption')
 path['status']='visual alignment graphic from underside of LDV lens to measured sample surface; colour not measured light'
 sample['noncontact_basis']='Tiny-Lev photographic source Fig.1c; levitated, no physical rod'
 look((4.4,-7.6,5.0),(0,0,1.48),5.5)

def energy():
 # Keep existing MFC bodies and rear cell fittings. Replace source free ends with external schematic source plugs.
 for gas in ('CO2_cathode','Ar_anode'):
  obj=bpy.data.objects[f'{gas}_gas_source_to_MFC'];sp=obj.data.splines[0]
  start=Vector(sp.bezier_points[0].co);mx=bpy.data.objects[f'{gas}_MFC'].location.x
  # Assumed source outside paper's apparatus; visually owned face, not an invented branded gas cylinder.
  housing=box(f'{gas}_assumed_source_panel',(start.x,start.y+.145,start.z),(.36,.21,.29),'base','assumption')
  housing['not_in_source']='Representative supply boundary for Methods-specified CO2/Ar; no cylinder/model claimed'
  socket=cyl(f'{gas}_source_visible_socket',(start.x,start.y-.004,start.z),.060,.075,'metal',axis='Y',ev='assumption')
  socket['owner']=housing.name
  # Actual cap toward MFC is at y=start.y-.0415; move only first curve point.
  front=mesh_limits(socket.name,1)[0];sp.bezier_points[0].co.y=front
  obj['source_owner']=socket.name
  # Retain two distinct gas colour families (other material might be source-schematic, not gas colour fact).
  mfc=bpy.data.objects[f'{gas}_MFC'];mfc['two_faces']='rear supply inlet and front cell-facing outlet; flow direction illustrative'
  inport=bpy.data.objects[f'{gas}_MFC_inlet_socket'];outport=bpy.data.objects[f'{gas}_MFC_outlet_socket']
  inport['owner']=mfc.name;outport['owner']=mfc.name
  cell=bpy.data.objects[f'{gas}_back_gas_stub'];cell['owner']='NOM_membrane_free_flow_cell';cell['port_limit']='external sleeve, no hidden bore shown'
  obj['sequence']='assumed source socket -> MFC inlet';bpy.data.objects[f'{gas}_MFC_to_cell_rear']['sequence']='MFC outlet -> cell external rear fitting'
 look((6.7,-8,7.0),(0,.45,.60),9.5)

def thermal():
 # v03 seams existed but right x-end was open in pixels. Close end with REAL mesh cap, not a label.
 x=2.315
 outline=[(-.77,.38),(-.74,.61),(-.66,.76),(-.48,.80),(0,.82),(.48,.80),(.66,.76),(.74,.61),(.77,.38)]
 # Thin closed face across opening, curved upper silhouette shares the top foil's family.
 vs=[(x,y,z) for y,z in outline]+[(x,-.77,.24),(x,.77,.24)]
 faces=[tuple(range(len(outline)))+(len(outline)+1,len(outline))]
 me=bpy.data.meshes.new('East_final_foil_endcap_mesh');me.from_pydata(vs,[],faces);me.update()
 obj=bpy.data.objects.new('East_final_closed_foil_endcap',me);bpy.context.collection.objects.link(obj);obj.data.materials.append(r.M['metal']);r.tag(obj,'text-supported')
 obj.modifiers.new('Editable film thickness','SOLIDIFY').thickness=.028
 obj['state']='FINAL SEALED. wick must not be visible through right end; geometry is illustrative thin folded film.'
 # Rear and front edge strips add a visible continuous perimeter across the end-cap.
 seam=box('East_final_fold_over_seam',(2.323,0,.43),(.060,1.56,.062),'white','text-supported')
 seam['owner']=obj.name
 look((5.4,-8.4,4.8),(0,0,.43),7.5)

CASES={'02_robotics':('v04','v05',robot),'13_biomed_optics':('v03','v04',optics),'14_acoustic_alt':('v03','v04',acoustics),'16_energy_nature':('v03','v04',energy),'20_thermal':('v03','v04',thermal)}
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
if len(args)!=1 or args[0] not in CASES:raise SystemExit('one supported case ID required')
case=args[0];parent,v,fix=CASES[case]
if bpy.context.scene.get('revision_version')!=parent:raise RuntimeError('incorrect source scene version for '+case)
out=root/'cases'/case/v
if out.exists():raise RuntimeError('refusing overwrite '+str(out))
fix();bpy.context.view_layer.update();sc=bpy.context.scene;sc['revision_version']=v;sc['visual_review']='pending_external_pixel_review';sc['revision_basis']='third external visual review of previous version';sc['unknowns']='Representative geometry only; no hidden function, seal, true force or size asserted'
out.mkdir(parents=True);bpy.ops.wm.save_as_mainfile(filepath=str(out/'scene.blend'));print('STAGE5_SAVED',case,v,flush=True)
