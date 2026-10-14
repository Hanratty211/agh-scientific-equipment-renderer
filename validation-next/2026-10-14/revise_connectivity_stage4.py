"""Stage 4: one saved scene in, one higher version out; old files never overwritten.
Only exterior/support/editable geometric relations justified by source or marked assumptions.
Usage: blender -b cases/ID/vXX/scene.blend --python revise_connectivity_stage4.py -- ID
"""
import bpy,sys,math
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parent;sys.path.insert(0,str(root))
import render_core as r
r.M.clear()
for mat in bpy.data.materials:
 if mat.name.startswith('MAT_'):r.M[mat.name[4:]]=mat

def material(name,rgba):
 if name not in r.M:
  m=bpy.data.materials.new('MAT_'+name);m.diffuse_color=(*rgba,1);m.use_nodes=True
  p=m.node_tree.nodes.get('Principled BSDF')
  if p:p.inputs['Base Color'].default_value=(*rgba,1)
  r.M[name]=m
 return r.M[name]
for key,col in {'metal':(.43,.52,.59),'dark':(.09,.14,.20),'soft':(.85,.60,.37),'copper':(.60,.34,.18),'blue':(.16,.48,.78),'black':(.03,.04,.06),'red':(.75,.25,.20),'white':(.79,.85,.86),'base':(.22,.30,.36),'glass':(.46,.72,.78),'yellow':(.85,.72,.29),'screen':(.10,.45,.52)}.items():material(key,col)

def remove(name):
 ob=bpy.data.objects.get(name)
 if ob:bpy.data.objects.remove(ob,do_unlink=True)
def limits(name,axis):
 ob=bpy.data.objects[name];return min((ob.matrix_world@Vector(v)).__getitem__(axis) for v in ob.bound_box),max((ob.matrix_world@Vector(v)).__getitem__(axis) for v in ob.bound_box)
def tube(name,points,rad,mat,evidence,owner='',note=''):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=32;cu.bevel_depth=rad;cu.bevel_resolution=4
 spl=cu.splines.new('BEZIER');spl.bezier_points.add(len(points)-1)
 for p,xyz in zip(spl.bezier_points,points):p.co=xyz;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 ob=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(ob);cu.materials.append(r.M[mat]);r.tag(ob,evidence,owner)
 ob['source_or_limit']=note;return ob
def panel(name,loc,scale,mat='metal',evidence='assumption'):
 return r.box(name,loc,scale,mat,evidence,bevel=.01)
def frame(name,a,b,radius=.04,mat='metal',evidence='assumption'):
 return r.segment(name,a,b,radius,mat,evidence)
def camera(pos,target,size):
 for ob in list(bpy.data.objects):
  if ob.type=='CAMERA':bpy.data.objects.remove(ob,do_unlink=True)
 return r.camera(pos,target,size)

def robot():
 # v03 guide posts and new bearing helper both stopped before upper machine beam.
 top=bpy.data.objects['Testing_machine_upper_frame'];bottom=bpy.data.objects['Testing_machine_lower_frame']
 z_top=limits(top.name,2)[0];z_bottom=limits(bottom.name,2)[1]
 for x in (-1,1):
  old=bpy.data.objects[f'Linear_guide_{x}'];old.location.z=(z_bottom+z_top)/2;old.dimensions.z=(z_top-z_bottom)+.05
  remove(f'Guide_bearing_{x}')
  sleeve=frame(f'Upper_guide_socket_{x}',(x,0,z_top-.11),(x,0,z_top+.045),.087,'dark')
  sleeve['owner']='Testing_machine_upper_frame';sleeve['assumption']='socket form representative, structural load not established'
 for lab in ('lower','upper'):
  specimen=bpy.data.objects[f'Soft_coupon_{lab}_clamped']
  specimen['visible_grip_relation']='Two opposed jaw faces bracket coupon end with finite insertion into circular grip'
  for y in (-.13,.13):
   jaw=bpy.data.objects[f'{lab}_jaw_at_{y}'];jaw['contact_owner']=specimen.name
 camera((5.3,-8,4.5),(0,0,1.57),6.2)

def biomedical():
 p1=bpy.data.objects['Conductive_silicone_P1'];p1_lo,p1_hi=limits(p1.name,0);p1_front=limits(p1.name,1)[0]
 # Existing six isolated tracks reached outside P1 and did not meet the measuring pad: remove all.
 for ob in list(bpy.data.objects):
  if ob.name.startswith('P1_conductive_pattern_'):bpy.data.objects.remove(ob,do_unlink=True)
 remove('Test_wire_visible_segment');remove('P1_external_test_contact')
 pad=bpy.data.objects['P1_measurement_point'];pad.location=(0,-.04,.847)
 pad['owner']='Conductive_silicone_P1';pad['status']='visible representative measurement pad, electrical resistance unknown'
 # Trace fan lies on the actual P1 mesh plane, follows inside its footprint and converges to pad edge.
 for i,x in enumerate((-.70,-.42,-.14,.14,.42,.70)):
  trace=tube(f'P1_continuous_fan_{i}',[(x,.23,.827),(x,.09,.827),(x*.35,-.015,.827),(0,-.04,.827)],.010,'copper','assumption','Conductive_silicone_P1','Routing representative; all control points inside P1 footprint; terminates in pad.')
 # From pad front towards an actual small top contact; external black lead starts at its outer face.
 contact=r.cyl('P1_visible_lead_socket',(0,-.10,.873),.050,.09,'metal',axis='Y',evidence='assumption');contact['owner']='Conductive_silicone_P1'
 lead=tube('P1_external_lead_flexible',[(0,-.145,.873),(0,-.33,.89),(.04,-.48,.94),(.22,-.62,1.00)],.020,'black','assumption','P1_visible_lead_socket','Outside visible segment only; solder/through-layer bonding unverified.')
 # Pull substrate/adhesive closer to P1 to read as one stack without asserting true micrometer thickness.
 bpy.data.objects['Double_sided_silicone_adhesive'].location.z=.65
 bpy.data.objects['Skin_like_substrate'].location.z=.43
 for n in ('Double_sided_silicone_adhesive','Skin_like_substrate'):bpy.data.objects[n]['stack_note']='schematic compressed visual gap, thickness not measured'
 camera((4.8,-6.9,5.1),(0,0,.52),5.3)

def optics():
 # Source has three separate back-probe ferrules; leave existing metal plugs/collars untouched.
 for i,x in enumerate((.85,1.15,1.45)):
  remove(f'Fiber_source_to_scope_{i}')
  sy=-.54;ex=-1.66+i*.25
  plug=bpy.data.objects[f'MLE_fiber_plug_{i}'];rear=min((plug.matrix_world@v.co).y for v in plug.data.vertices)
  fiber=tube(f'Flexible_fiber_source_to_probe_{i}',[(ex,sy,.64),(ex,-1.12,.54),(-.87+i*.25,-1.79,.47),(-.02+i*.23,-1.91,.70),(.51+i*.16,-1.55,1.15),(x,rear,1.26)],.027,['blue','red','yellow'][i],'source-visible',f'MLE_fiber_plug_{i}','Three independent soft curves, connector exterior only; no merged optical path.')
  fiber['source_owner']=f'Illuminator_exterior_plug_{i}';fiber['target_owner']=plug.name
  bpy.data.objects[f'Coupler_visible_collar_{i}']['owner']='Colonoscopic_coupler'
 # Rebuild previously polygonal scope shaft as soft exterior continuation, not inner bundle.
 remove('Flexible_scope_outer_tube')
 tube('Flexible_scope_outer_tube',[(1.24,-.02,.94),(1.65,.40,1.20),(2.22,.91,1.16),(2.67,.95,.75),(2.93,.83,.50)],.11,'dark','source-visible','Colonoscopic_coupler','Externally seen flexible shaft only; internal optical route unknown.')
 camera((5.5,-8.6,5.6),(-.05,0,1.38),8.1)

def acoustics():
 # Fig.1c supports LDV top-facing-down setup, not its actual bracket make/model.
 frame('LDV_floor_mount_column',(1.48,.85,-.14),(1.48,.85,3.18),.084,'metal')
 panel('LDV_mount_base',(1.48,.85,-.12),(.78,.67,.15),'base')
 frame('LDV_overhead_arm',(1.48,.85,3.17),(.20,.20,3.17),.060,'metal')
 frame('LDV_vertical_adjuster',(.20,.20,3.17),(0,0,2.99),.072,'dark')
 collar=r.cyl('LDV_head_clamp',(0,0,2.97),.18,.11,'metal');collar['owner']='LDV_vertical_adjuster';collar['status']='visible approximate support, not measured optical alignment hardware'
 bpy.data.objects['LDV_optical_head']['mount_owner']='LDV_head_clamp'
 bpy.data.objects['Levitated_sample_noncontact']['source']='Fig.1c Tiny-Lev noncontact levitation; no solid rod invented'
 camera((4.4,-7.6,5.0),(0,0,1.48),5.5)

def energy():
 # Gas lines: separate gas source→MFC input and MFC output→cell rear sleeve.
 for key in ('CO2_cathode','Ar_anode'):
  remove(key+'_external_gas')
  mfc=bpy.data.objects[key+'_MFC'];mx=mfc.location.x;z=mfc.location.z-.15
  # MFC body y=1.80 ±.18. Cylinders attach to its two physical Y faces.
  inlet=r.cyl(key+'_MFC_inlet_socket',(mx,2.015,z),.056,.070,'metal',axis='Y',evidence='assumption')
  outlet=r.cyl(key+'_MFC_outlet_socket',(mx,1.585,z),.056,.070,'metal',axis='Y',evidence='assumption')
  inlet['owner']=mfc.name;outlet['owner']=mfc.name
  source_x=-.55 if key.startswith('CO2') else 2.48
  tube(key+'_gas_source_to_MFC',[(source_x,2.67,z+.15),(source_x,2.46,z+.09),(mx,2.23,z+.03),(mx,2.05,z)],.027,'yellow' if key.startswith('CO2') else 'green_route','text-supported',inlet.name,'External gas feed; source upstream equipment not specified.')
  # Existing cell back stub sits y=.71 with +Y cap=.78. End at cap, not at a proxy ring.
  stub=bpy.data.objects[key+'_back_gas_stub'];cap=max((stub.matrix_world@v.co).y for v in stub.data.vertices)
  tube(key+'_MFC_to_cell_rear',[(mx,1.55,z),(mx,1.34,z-.06),(mx,1.03,z-.08),(mx,cap,z)],.029,'yellow' if key.startswith('CO2') else 'green_route','text-supported',stub.name,'Rear exterior gas entry only. No bore/inner gas path/seal asserted.')
  for ob in (inlet,outlet,stub):ob['port_status']='externally visible schematic sleeve, bore and regulator function unverified'
 camera((6.7,-8,7.0),(0,.45,.60),9.5)

def rf():
 # Fig1a-c has substrate/ground as actual layers; do not falsely collapse ground conductor into missing substrate.
 # Place both in a coherent laminate instead of floating/offset slab. Current sheet dimensions retained.
 sub=bpy.data.objects['Dielectric_substrate'];ground=bpy.data.objects['Ground_plane']
 sub.location=(0,0,.20);sub.dimensions=(3.48,2.27,.16)  # top .28
 ground.location=(0,0,.292);ground.dimensions=(3.48,2.27,.024) # bottom .28 (touch)
 ground['layer_note']='ground plane with existing Boolean double elliptical slots; touching substrate upper face'
 radiator=bpy.data.objects['Dielectric_resonator_conical_radiator']
 # Original mesh base .43 + v02 shift -.13 => .30, here ground top=.304; small seated base overlap.
 radiator.location.z-=.010
 radiator['mount_note']='base seats on top of ground/substrate stack. No RF performance inference.'
 rim=bpy.data.objects['DRA_toroidal_rim'];rim.location.z-=.010
 # Reduce white/translucent appearance by material value, not fake metal contact.
 mat=material('mounted_dielectric',(.29,.54,.67));radiator.data.materials.clear();radiator.data.materials.append(mat);rim.data.materials.clear();rim.data.materials.append(mat)
 for n in ('Microstrip_feed_trace','Feed_to_resonator_contact'):remove(n)
 connector=bpy.data.objects['Feed_edge_connector'];connector.location=(0,-1.24,.345)
 # Surface copper path continuous up to radiating base edge in exposed schematic (routing assumption).
 path=panel('Copper_feed_footprint',(0,-.63,.339),(.13,1.14,.018),'copper');path['owner']='Dielectric_substrate'
 tip=panel('Copper_feed_to_DRA_base',(0,-.015,.339),(.13,.26,.018),'copper');tip['owner']='Dielectric_resonator_conical_radiator';tip['limit']='simplified electrical contact, characteristic impedance unknown'
 camera((5,-7.7,5.3),(0,0,.56),6.0)

def thermal():
 # Preserve v02 separate preseal process scene; final-state foil wrapper only.
 upper=bpy.data.objects['Flexible_al_plastic_top_foil'];lower=bpy.data.objects['Aluminum_plastic_lower_casing']
 # Bent shallow foil rim/profile, no claims about true bend radius; thin triangulated shell is editable.
 mesh=bpy.data.meshes.new('Final_top_folded_foil_mesh')
 cross=[(-.76,.38),(-.72,.62),(-.66,.76),(-.48,.79),(0,.81),(.48,.79),(.66,.76),(.72,.62),(.76,.38)]
 vs=[];faces=[]
 for x in (-2.30,2.30):
  for y,z in cross:vs.append((x,y,z))
 n=len(cross)
 for i in range(n-1):faces.append((i,i+1,n+i+1,n+i))
 mesh.from_pydata(vs,[],faces);mesh.update()
 ob=bpy.data.objects.new('Flexible_alplastic_folded_skin',mesh);bpy.context.collection.objects.link(ob);ob.data.materials.append(r.M['metal']);r.tag(ob,'text-supported')
 ob.modifiers.new('Editable thin shell','SOLIDIFY').thickness=.021
 ob['shape_note']='thin illustrative flexible aluminium-plastic casing fold; no measured flexural modulus or layer thickness'
 # Remove v02 thick four rigid wall blocks, replace flat heat-sealed foils along all four sides.
 for n0 in ('north','south','west','east_final'):remove('Heat_seal_'+n0)
 for y,key in ((-.73,'front'),(.73,'rear')):
  p=panel('Foil_heat_seam_'+key,(0,y,.39),(4.69,.10,.038),'white','text-supported');p['seam_state']='final heat seal, fold continuation approximate'
 for x,key in ((-2.31,'west'),(2.31,'east_final')):
  p=panel('Foil_heat_seam_'+key,(x,0,.39),(.10,1.52,.038),'white','text-supported');p['seam_state']='fourth east edge sealed after venting/vacuum/DI water fill'
 lower.location.z=.24;lower.dimensions.z=.024
 # v02 upper slab was flat, now show folded editable upper foil only.
 remove('Flexible_al_plastic_top_foil');remove('East_edge_process_port_symbol')
 camera((5.4,-8.4,4.8),(0,0,.43),7.5)

def wearable_energy():
 # Keep Fig3a exploded state but only small paper-unspecified clearance; all layers share one patch footprint.
 upper=bpy.data.objects['Upper_silicone_skin'];upper.location=(0,0,1.12)
 base=bpy.data.objects['PL_silicone_encapsulation'];base.location=(0,0,.18)
 board=bpy.data.objects['Flexible_printed_circuit'];board.location=(0,0,.39)
 pv=bpy.data.objects['Photovoltaic_cell'];pv.location=(0,0,.92)
 edge=bpy.data.objects['PV_module_edge'];edge.location=(0,0,.956)
 for i,x in enumerate((-1.22,1.22)):
  bat=bpy.data.objects[f'LiPo_battery_{i}'];bat.location=(x,-.03,.73);bat.dimensions=(.71,.88,.125)
  seat=bpy.data.objects[f'Battery_seat_{i}'];seat.location=(x,-.03,.60);seat.dimensions=(.74,.92,.06)
  bat['identity']='LiPo pouch schematic, distinct from photovoltaic cell; capacity/contacts unknown'
 for n in ('BLE_SoC','PPG_module'):
  ob=bpy.data.objects[n];ob['owner']='Flexible_printed_circuit';ob['attachment']='on board, lead/contact internal unknown'
 # Remove four visually misleading long stand-offs in exploded illustration; do not assert real screws.
 for i in range(2):
  for j in range(2):remove(f'Patch_alignment_spacer_{i}_{j}')
 for n in ('Upper_silicone_skin','Photovoltaic_cell','Flexible_printed_circuit','PL_silicone_encapsulation'):
  bpy.data.objects[n]['footprint_note']='aligned same patch center; vertical exploded offsets are illustrative only'
 camera((4.9,-7.1,5.0),(0,0,.62),6.1)

CASES={'02_robotics':(robot,'v03','v04'),'08_biomedical':(biomedical,'v02','v03'),'13_biomed_optics':(optics,'v02','v03'),'14_acoustic_alt':(acoustics,'v02','v03'),'16_energy_nature':(energy,'v02','v03'),'17_rf_nature':(rf,'v02','v03'),'20_thermal':(thermal,'v02','v03'),'15_biomed_energy':(wearable_energy,'v04','v05')}
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
if len(args)!=1 or args[0] not in CASES:raise SystemExit('usage: blender -b saved.blend --python revise_connectivity_stage4.py -- CASE_ID')
case=args[0];fn,parent,v=CASES[case]
if bpy.context.scene.get('revision_version')!=parent:raise RuntimeError(f'wrong parent for {case}: expected {parent} got {bpy.context.scene.get("revision_version")}')
fn();bpy.context.view_layer.update();sc=bpy.context.scene;sc['revision_version']=v;sc['visual_review']='pending_new_external_review';sc['revision_basis']='second user-reported external visual audit of parent version';sc['limits']='Scene geometry and paper-visible layout only. No hidden pathways, physical connection forces, fluid seals, or image acceptance.'
out=root/'cases'/case/v
if out.exists():raise RuntimeError('target version already exists: refusing overwrite '+str(out))
out.mkdir(parents=True);bpy.ops.wm.save_as_mainfile(filepath=str(out/'scene.blend'));print('STAGE4_SAVED',case,v,flush=True)
