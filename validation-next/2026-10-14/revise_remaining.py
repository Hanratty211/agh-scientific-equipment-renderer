"""Non-destructive source-limited targeted revisions for the nine non-04 cases.
Run: blender -b cases/ID/v01-or-v03/scene.blend --python revise_remaining.py -- ID
Never infer unknown hidden channels, fixture loads, wiring or exact dimensions.
"""
import bpy,sys,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT))
import render_core as r
r.M.clear()
for m in bpy.data.materials:
 if m.name.startswith('MAT_'):r.M[m.name[4:]]=m

def rm(n):
 o=bpy.data.objects.get(n)
 if o:bpy.data.objects.remove(o,do_unlink=True)
def note(o,text):o['revision_note']=text;return o
def cams(pos,target,scale):
 for o in list(bpy.data.objects):
  if o.type=='CAMERA':bpy.data.objects.remove(o,do_unlink=True)
 r.camera(pos,target,scale)
def segment(n,a,b,rad=.03,mat='metal',ev='assumption'):
 return r.segment(n,a,b,rad,mat,ev)
def ellipse(n,center,scale,mat='metal',ev='assumption'):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,location=center);o=bpy.context.object;o.name=n;o.scale=scale;o.data.materials.append(r.M[mat]);return r.tag(o,ev)
def ensure(name,col):
 if name not in r.M:
  m=bpy.data.materials.new('MAT_'+name);m.diffuse_color=(*col,1);m.use_nodes=True
  bs=m.node_tree.nodes.get('Principled BSDF')
  if bs:bs.inputs['Base Color'].default_value=(*col,1)
  r.M[name]=m
 return r.M[name]
# Saved blends discard unused material presets: restore only required missing names without r.setup().
for key,col in {'dark':(.09,.14,.20),'metal':(.43,.52,.59),'blue':(.16,.48,.78),'soft':(.85,.60,.37),'white':(.79,.85,.86),'black':(.03,.04,.06),'red':(.75,.25,.20),'yellow':(.85,.72,.29),'copper':(.60,.34,.18),'base':(.22,.30,.36),'screen':(.10,.45,.52),'glass':(.46,.72,.78)}.items():ensure(key,col)
ensure('green_route',(.20,.66,.35));ensure('skin_warm',(.82,.54,.47))

def robot():
 # Actual cylindrical grips have opposed jaws around specimen ends; model both pair/pressure faces.
 for name in ('Lower_clamp_front','Upper_clamp_front','Multimaterial_soft_coupon_lower','Multimaterial_soft_coupon_upper'):rm(name)
 for x in (-1,1):
  segment(f'Guide_bearing_{x}',(x,-.16,.50),(x,-.16,2.70),.072,'metal')
 for lab,z in (('lower',.66),('upper',2.51)):
  r.cyl(f'{lab}_circular_grip_body',(0,0,z),.35,.24,'dark',evidence='source-visible')
  for y in (-.13,.13):
   r.box(f'{lab}_jaw_at_{y}',(0,y,z+(.11 if lab=='lower' else -.11)),(.24,.13,.20),'metal','source-visible',bevel=.018)
 # Soft coupon dimensions are illustrative; embed ends between jaws, not hovering near faces.
 lower=r.box('Soft_coupon_lower_clamped',(0,0,1.21),(.105,.12,1.17),'blue','source-visible',bevel=.025)
 upper=r.box('Soft_coupon_upper_clamped',(0,0,2.07),(.105,.12,.78),'soft','source-visible',bevel=.025)
 lower['grip_contact']='lower jaw z=.55-.80 / specimen begins z=.625';upper['grip_contact']='upper jaw z=2.29-2.73 / specimen ends z=2.46'
 cams((5.3,-8,4.5),(0,0,1.57),6.2)

def wearable():
 # Fig.3 left only; neighbouring photograph informs outer appearance, not interior joints.
 for i in range(2):
  rm(f'Electrode_contact_{i}');rm(f'Electrode_lead_{i}')
 r.box('P1_measurement_point',(0,-.04,.855),(.23,.19,.045),'copper','source-visible',bevel=.015)
 for j,x in enumerate((-.69,-.42,-.14,.14,.42,.69)):
  r.route(f'P1_conductive_pattern_{j}',[(x,.20,.855),(x,.32,.855),(x*.82,.42,.855)],.013,'copper','assumption')
 # Distinguish physical substrate, thin adhesive and conductive P1 without mistaking a wire for a bonded socket.
 for name,reason in [('Skin_like_substrate','Fig3 artificial-skin substrate'),('Double_sided_silicone_adhesive','Fig3 adhesive layer'),('Conductive_silicone_P1','Fig3 upper P1')]:
  if name in bpy.data.objects:bpy.data.objects[name]['source_label']=reason
 r.cyl('P1_external_test_contact',(0,-.37,.855),.075,.028,'copper',evidence='assumption')
 r.route('Test_wire_visible_segment',[(0,-.37,.855),(0,-.55,.90),(.18,-.80,.94),(.60,-1.03,.95)],.019,'black','assumption')['unknown']='external test lead continues out of frame; hidden bond not modeled'
 cams((4.8,-6.9,5.1),(0,0,.50),5.3)

def endoscopy():
 # One joined cart: posts already exist, add screen bracket, shelf equipment feet and casters.
 r.box('Monitor_bracket_beam',(-1.15,.12,2.31),(.12,.14,.60),'metal','assumption')
 r.box('Monitor_v_mount',(-1.15,.11,2.62),(.76,.07,.26),'metal','assumption')
 for j,x in enumerate((-2.36,-.72)):
  for k,y in enumerate((-.46,.46)):
   r.cyl(f'Cart_caster_{j}_{k}',(x,y,-.07),.09,.20,'dark',axis='Y',evidence='assumption')
 for i,x in enumerate((.85,1.15,1.45)):
  rm(f'MLE_connector_optic_port_{i}');rm(f'External_patch_fiber_{i}')
  # Source side fiber begins on face of illumination source at front y=-.47 and ends at probe plug back face.
  r.cyl(f'Illuminator_exterior_plug_{i}',(-1.66+i*.25,-.49,.64),.058,.10,'metal',axis='Y',evidence='assumption')
  pts=[(-1.66+i*.25,-.54,.64),(-1.4+i*.18,-1.00,.74),(-.2+i*.18,-1.65,.92),(.3+i*.13,-1.51,1.44),(x,-1.12,1.26)]
  r.route(f'Fiber_source_to_scope_{i}',pts,.026,['blue','red','yellow'][i],'source-visible')['unknown']='plug/connector is exterior only; internal light propagation not modeled'
  r.cyl(f'Coupler_visible_collar_{i}',(x,-.90,1.26),.071,.06,'metal',axis='Y',evidence='assumption')
 # Move only probe external curve to segmented soft continuation; not an invented internal bundle.
 rm('Flexible_scope_outer_tube')
 cu=r.route('Flexible_scope_outer_tube',[(1.24,-.02,.94),(1.64,.35,1.23),(2.16,.82,1.21),(2.70,.96,.77),(2.93,.83,.50)],.11,'dark','source-visible')
 cams((5.5,-8.6,5.6),(-.05,0,1.38),8.1)

def acoustics():
 # Align LDV optical axis vertically down over non-contact levitated sample and shaker.
 o=bpy.data.objects['LDV_optical_head'];o.location=(0,0,3.06)
 lens=bpy.data.objects['LDV_front_lens'];lens.location=(0,0,2.83);lens.rotation_euler=(0,0,0)
 target=bpy.data.objects['Levitated_sample_noncontact'];target.location=(0,0,1.55);target['support_status']='noncontact acoustic levitation claimed in source; no physical rod'
 # Narrow dashed visual axis via separated segments; not assert beam wavelength/visible colour.
 for i in range(4):segment(f'LDV_sampling_axis_{i}',(0,0,2.67-i*.19),(0,0,2.58-i*.19),.006,'red','assumption')
 cams((4.4,-7.6,5.0),(0,0,1.48),5.5)

def wearable_energy():
 # Source Fig3a is exploded but a single patch: reset each plane around one common center and show support.
 upper=bpy.data.objects['Upper_silicone_skin'];upper.location=(0,0,1.40)
 upper['placement']='top open-window cover, small exploded offset; NOT physical thickness measurement'
 base=bpy.data.objects['PL_silicone_encapsulation'];base.location.z=.13
 board=bpy.data.objects['Flexible_printed_circuit'];board.location.z=.43
 for n,x in enumerate((-1.22,1.22)):
  b=bpy.data.objects[f'LiPo_battery_{n}'];b.location=(x,-.03,.76)
  # Pouch rests visually over board via small spacer; wiring/contacts not represented.
  r.box(f'Battery_seat_{n}',(x,-.03,.64),(.72,.91,.08),'soft','assumption',bevel=.025)
 pv=bpy.data.objects['Photovoltaic_cell'];pv.location=(0,0,1.11)
 edge=bpy.data.objects['PV_module_edge'];edge.location=(0,0,1.148)
 for n in ('PPG_module','BLE_SoC'):
  if n in bpy.data.objects:bpy.data.objects[n]['relation_note']='on fPCB schematic surface; no wire bond/through-hole proven'
 # Support the cover over all components in exploded view with four short locator posts, not electrical connections.
 for i,x in enumerate((-1.67,1.67)):
  for j,y in enumerate((-.83,.83)):
   segment(f'Patch_alignment_spacer_{i}_{j}',(x,y,.55),(x,y,1.30),.020,'white','assumption')
 cams((4.9,-7.1,5.0),(0,0,.72),6.2)

def electrolyzer():
 # Methods p9 distinguishes continuously pumped electrolyte and CO2/Ar on cathode/anode backs.
 for n in ('External_single_pass_reservoir','External_receiving_vessel','Single_pass_inlet_tube','Single_pass_cell_to_vessel'):
  rm(n)
 # The source specifies upstream supply but not a pictured vessel: leave pump intake as out-of-frame open line.
 r.route('Fresh_electrolyte_supply_segment',[(-3.55,-.67,.44),(-3.00,-.66,.49),(-2.61,-.49,.44)],.027,'blue','text-supported')['source']='Methods p9 single-pass electrolyte; upstream tank outside scope'
 rm('Single_pass_pump_to_cell')
 r.route('Electrolyte_pump_to_cell',[(-1.62,-.48,.43),(-.81,-.55,.80),(.12,-.43,.85),(.59,-.12,.53)],.035,'blue','text-supported')['unknown']='cell fitting schematic only, internal liquid channel not shown'
 r.route('Spent_electrolyte_off_frame',[(1.97,-.12,.53),(2.35,-.57,.70),(3.13,-.57,.72)],.035,'blue','text-supported')['unknown']='unobserved receiving vessel omitted'
 cell=bpy.data.objects['NOM_membrane_free_flow_cell']
 for lab,z,x,mat in [('CO2_cathode',.82,.92,'yellow'),('Ar_anode',.34,1.58,'green_route')]:
  # Both gas entries explicitly from REAR face of cell (y=.64 for base whose center .3 and depth .68).
  y=.64;port=r.cyl(f'{lab}_back_gas_stub',(x,y+.07,z),.056,.14,'metal',axis='Y',evidence='assumption')
  port['face_contact']='rear y=.64 of NOM flow-cell body; exterior stub, no bore'
  mfc=r.box(f'{lab}_MFC',(x,1.80,z+.15),(.48,.36,.32),'base','text-supported',bevel=.03)
  r.box(f'{lab}_MFC_screen',(x,1.61,z+.17),(.23,.015,.12),'screen','assumption',bevel=.01)
  r.route(f'{lab}_external_gas',[(-.55 if lab.startswith('CO2') else 2.48,2.65,z+.15),(x,2.30,z+.15),(x,1.98,z+.15),(x,1.62,z+.15),(x,1.11,z),(x,.78,z)],.025,mat,'text-supported')['unknown']='external gas segment only; controller internals not modeled'
 cell['flow_note']='Liquid face and two back gas faces are distinct; sealed gas/aqueous channels unknown.'
 cams((6.7,-8,7.0),(0,.45,.60),9.5)

def antenna():
 # v01 already has a real Boolean double ground slot; only remove floating radiating body/board split.
 radiator=bpy.data.objects['Dielectric_resonator_conical_radiator'];radiator.location.z-=.13
 rim=bpy.data.objects['DRA_toroidal_rim'];rim.location.z-=.13
 sub=bpy.data.objects['Dielectric_substrate'];sub['v02_scope']='single primary substrate with slotted ground and mounted central DRA; dielectric heights illustrative'
 feed=bpy.data.objects['Microstrip_feed_trace'];feed.location=(0,-.75,.335);feed.dimensions.y=1.31
 connector=bpy.data.objects['Feed_edge_connector'];connector.location=(0,-1.26,.36)
 r.box('Feed_to_resonator_contact',(0,-.08,.39),(.13,.28,.075),'copper','assumption',bevel=.01)['unknown']='representative metal contact, source dimensions/electric matching unknown'
 cams((5,-7.7,5.3),(0,0,.56),6.0)

def mechanical():
 # Methods p9 ASTM D638 Type IV is explicitly for parent materials, NOT a PIM lattice sample.
 for o in list(bpy.data.objects):
  if o.name.startswith('PIM_chain_'):bpy.data.objects.remove(o,do_unlink=True)
 for n in ('lower_jaw_working_face','upper_jaw_working_face'):rm(n)
 # Editable watertight outline extruded to a dogbone, no ASTM dimensional claims.
 verts2=[(-.24,.94),(.24,.94),(.24,1.20),(.095,1.38),(.095,2.61),(.24,2.79),(.24,3.02),(-.24,3.02),(-.24,2.79),(-.095,2.61),(-.095,1.38),(-.24,1.20)]
 verts=[(x,y,z) for y in (-.08,.08) for x,z in verts2];n=len(verts2)
 faces=[tuple(range(n-1,-1,-1)),tuple(range(n,n*2))]
 for i in range(n):faces.append((i,(i+1)%n,(i+1)%n+n,i+n))
 mesh=bpy.data.meshes.new('Parent_material_Type_IV_mesh');mesh.from_pydata(verts,[],faces);mesh.update()
 o=bpy.data.objects.new('Parent_material_Type_IV_coupon',mesh);bpy.context.collection.objects.link(o);o.data.materials.append(r.M['soft']);r.tag(o,'text-supported')
 o['scope']='ASTM D638 Type IV parent-material specimen ONLY. Not PIM or CIM architecture.'
 # V-shaped opposing jaws have visible overlap with dogbone enlarged ends.
 for name,z in [('lower',1.06),('upper',2.91)]:
  for j,y in enumerate((-.145,.145)):
   jaw=r.box(f'{name}_grip_face_{j}',(0,y,z),(.50,.14,.25),'metal','assumption',bevel=.015)
   jaw['physical_relation']='grip overlaps coupon wide end in z, y face at ±.075 close to coupon ±.08; clamp force unverified'
 cams((6,-8.6,5.6),(0,0,1.95),6.6)

def thermal():
 # Flexible laminated foil main scene FINAL sealed state; pre-seal state is separately labeled detail.
 for n in ('Aluminum_plastic_back_wall','Aluminum_plastic_front_lip','Upper_casing_exposed_strip'):
  rm(n)
 lower=bpy.data.objects['Aluminum_plastic_lower_casing'];lower.location=(0,0,.26);lower.dimensions=(4.60,1.5,.035)
 # Mesh warp/weft retained as editable schematic cutaway; not shown through opaque final foil.
 for ob in bpy.data.objects:
  if ob.name.startswith(('Copper_wick_warp_','Copper_wick_weft_')):
   ob['cutaway_only']='hidden behind opaque final casing; independent pre-seal detail needed to view the same saved geometry'
 upper=r.box('Flexible_al_plastic_top_foil',(0,0,.71),(4.62,1.52,.035),'metal','text-supported',bevel=.012)
 upper['transparency']='opaque exterior; internal vapor-liquid path NOT visible'
 for name,loc,scale in [('north',(0,.72,.48),(4.68,.11,.46)),('south',(0,-.72,.48),(4.68,.11,.46)),('west',(-2.28,0,.48),(.13,1.54,.46)),('east_final',(2.28,0,.48),(.13,1.54,.46))]:
  r.box('Heat_seal_'+name,loc,scale,'white','text-supported',bevel=.017)
 # Charging port/final side are process metadata, not a permanent open pipe.
 r.cyl('East_edge_process_port_symbol',(2.31,0,.50),.060,.14,'metal',axis='X',evidence='assumption')['process_status']='historical temporary opening during filling; final external edge sealed'
 for n in ('Heater_contact_end','Cooling_contact_end'):rm(n)
 cams((5.5,-8.2,4.5),(0,0,.42),7.5)

FIX={'02_robotics':robot,'08_biomedical':wearable,'13_biomed_optics':endoscopy,'14_acoustic_alt':acoustics,'15_biomed_energy':wearable_energy,'16_energy_nature':electrolyzer,'17_rf_nature':antenna,'18_mechanical_nature':mechanical,'20_thermal':thermal}
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
if len(args)!=1 or args[0] not in FIX:raise SystemExit('expected one non-04 case id')
case=args[0];FIX[case]();sc=bpy.context.scene
version='v04' if case=='15_biomed_energy' else 'v02'
sc['revision_version']=version;sc['visual_review']='external_human_review_pending';sc['revision_basis']='user-reported external human review of prior source/render pair';sc['unknown']='Illustrative dimensions/appearance; only visible/Methods-supported structures; no functional approval.'
bpy.context.view_layer.update();dest=ROOT/'cases'/case/version;dest.mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(dest/'scene.blend'));print('TARGETED_SAVED',case,version,dest/'scene.blend',flush=True)
