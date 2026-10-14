"""Batch-specific, source-bounded real editable 3D assemblies; not functional CAD.
Run: blender -b --python build_cases.py -- CASE_ID v01
Every position/size here is a visual modeling assumption unless scene object notes say otherwise.
Text-first cases 16,18,20 deliberately do not inspect figure pixels for v01.
"""
import sys, math, json
from pathlib import Path
from mathutils import Vector
import bpy
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import render_core as r
CASES={x['id']:x for x in json.loads((ROOT/'selected_cases.json').read_text())}

def grid_mesh(name,w,h,z,cols=3,rows=2,mat='soft'):
 verts=[];faces=[]
 for j in range(rows+1):
  for i in range(cols+1):verts.append((-w/2+w*i/cols,-h/2+h*j/rows,z+0.03*math.sin(i*2)*math.sin(j*2)))
 for j in range(rows):
  for i in range(cols):
   a=j*(cols+1)+i;faces.append((a,a+1,a+cols+2,a+cols+1))
 mesh=bpy.data.meshes.new(name+'_mesh');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(o);o.data.materials.append(r.M[mat]);r.tag(o,'source-visible');o.modifiers.new('Editable shell','SOLIDIFY').thickness=.045;return o

def robot():
 r.box('Testing_machine_lower_frame',(0,0,.04),(2.5,1.0,.17),'metal');r.box('Testing_machine_upper_frame',(0,0,3.2),(2.5,1.0,.17),'metal')
 for x in (-1,1):r.cyl(f'Linear_guide_{x}',(x,0,1.6),.045,3.15,'metal')
 for z,n in ((.52,'Lower'),(2.64,'Upper')):
  r.box(n+'_jaw_carriage',(0,0,z),(.98,.76,.25),'base');r.box(n+'_clamp_front',(0,-.31,z+(.15 if n=='Lower' else -.15)),(.53,.11,.14),'metal','source-visible')
 r.box('Multimaterial_soft_coupon_lower',(0,0,1.18),(.16,.19,.93),'blue','source-visible')
 r.box('Multimaterial_soft_coupon_upper',(0,0,2.02),(.16,.19,.79),'soft','source-visible')
 r.camera((6,-10,5),(0,0,1.6),6.5)

def microfluidics():
 r.box('Five_syringe_drive_chassis',(1.9,.7,.11),(3.35,1.02,.24),'base','source-visible')
 r.box('Rack_clasp',(1.9,-.11,.70),(3.25,.12,.16),'metal','source-visible')
 r.box('Chip_carrier',(-1.2,-1.05,.03),(1.65,1.18,.12),'base','source-visible')
 r.box('Transparent_microfluidic_chip',(-1.2,-1.05,.14),(1.43,.96,.075),'glass','source-visible')
 for i in range(5):
  x=.62+i*.63;r.pump(x,.60,.55,i)
  dst=(-1.62+i*.20,-.65,.23)
  r.open_port(f'Chip_inlet_{i}',dst,.045,'Y','Transparent_microfluidic_chip')
  r.route(f'External_fluid_tube_{i}',[(x,.13,.85),(x,-.35,1.03),(-.2+i*.09,-.55,.92),dst],.021,'blue','text-supported')
  r.cyl(f'Syringe_hub_connector_{i}',(x,.15,.85),.075,.16,'metal',axis='Y',evidence='source-visible')
  r.open_port(f'Chip_outlet_{i}',(-1.62+i*.20,-1.55,.23),.042,'Y','Transparent_microfluidic_chip')
 r.camera((6,-9,7),(0,-.25,.55),7.2)

def wearable():
 r.box('Skin_like_substrate',(0,0,.13),(3.0,1.40,.13),'soft','source-visible')
 r.box('Double_sided_silicone_adhesive',(0,0,.44),(2.75,1.27,.045),'glass','text-supported')
 grid_mesh('Conductive_silicone_P1',2.54,.55,.81,cols=12,rows=3,mat='dark')
 for n,x in enumerate((-1.05,1.05)):
  r.cyl(f'Electrode_contact_{n}',(x,0,.85),.10,.045,'copper','source-visible')
  r.route(f'Electrode_lead_{n}',[(x,0,.86),(x,-.6,.95),(x*1.25,-1.0,1.04)],.025,'black','source-visible')
 r.camera((4,-7,5),(0,0,.41),5.5)

def endoscopy():
 # Cart & clinical host from Fig.1a; connector detail from Fig.1c.
 for z,n in ((.12,'lower'),(1.10,'middle'),(2.03,'top')):r.box(f'Clinical_cart_{n}_shelf',(-1.55,0,z),(2.05,1.30,.11),'metal','source-visible')
 for x in (-2.4,-.7):
  for y in (-.46,.46):r.segment('Cart_post_'+str(x)+str(y),(x,y,.20),(x,y,2.10),.045)
 r.box('Clinical_imaging_host',(-1.55,.04,1.48),(1.2,.84,.47),'base','source-visible');r.box('Clinical_host_screen',(-1.55,-.40,1.52),(.67,.02,.26),'screen')
 r.box('MLE_illumination_source',(-1.40,-.02,.62),(1.25,.9,.50),'base','source-visible')
 r.box('Clinical_monitor',(-1.15,.12,2.86),(1.4,.09,.89),'dark','source-visible');r.box('Monitor_glass',(-1.15,.06,2.86),(1.18,.018,.72),'screen')
 r.cyl('Colonoscopic_coupler',(1.15,-.42,1.03),.35,.80,'dark',axis='Y',evidence='source-visible')
 for i,x in enumerate((.85,1.15,1.45)):
  r.open_port(f'MLE_connector_optic_port_{i}',(x,-.89,1.26),.074,'Y','Colonoscopic_coupler')
  r.cyl(f'MLE_fiber_plug_{i}',(x,-1.03,1.26),.076,.18,'metal',axis='Y',evidence='source-visible')
  r.route(f'External_patch_fiber_{i}',[(x,-1.10,1.26),(x,-1.45,1.64),(.25+i*.12,-2,1.20),(-1.4,-.51,.62)],.025,['blue','red','yellow'][i],'source-visible')
 r.route('Flexible_scope_outer_tube',[(1.24,-.02,.94),(1.65,.51,1.18),(2.2,1.0,1.30),(2.68,1.15,.64),(2.92,.84,.50)],.12,'dark','source-visible')
 r.torus('Distal_viewing_annulus',(2.95,.83,.50),.11,.030,'metal','Y','source-visible')
 r.camera((5,-9,6),(-.15,0,1.4),8.0)

def acoustics():
 r.box('Vibration_shaker',(0,0,.26),(1.55,1.20,.52),'base','source-visible');r.cyl('Shaker_piston',(0,0,.64),.28,.31,'metal')
 for z,n in ((.84,'lower'),(2.22,'upper')):
  r.box(f'TinyLev_{n}_plate',(0,0,z),(1.38,.72,.13),'metal','source-visible')
  for j in range(12):
   x=-.57+(j%6)*.23;y=-.20+(j//6)*.40
   r.cyl(f'Transducer_{n}_{j}',(x,y,z+(.09 if n=='lower' else -.09)),.071,.13,'dark',evidence='source-visible')
 for x in (-.62,.62):r.segment(f'TinyLev_side_support_{x}',(x,0,.9),(x,0,2.16),.032,'metal')
 r.cyl('Levitated_sample_noncontact',(0,0,1.55),.11,.10,'soft',evidence='source-visible')
 r.box('LDV_optical_head',(0,-1.42,2.60),(.52,.56,.42),'dark','source-visible');r.cyl('LDV_front_lens',(0,-1.72,2.60),.11,.05,'glass',axis='Y')
 r.camera((5,-8,5),(0,0,1.36),5.5)

# Case-to-function routing only; each routine builds geometry in Blender.
from build_more import sensor_power, electrolyzer, antenna, mechanical, thermal
ROUTINES={
 '02_robotics':robot,'04_microfluidics':microfluidics,
 '08_biomedical':wearable,'13_biomed_optics':endoscopy,
 '14_acoustic_alt':acoustics,'15_biomed_energy':sensor_power,
 '16_energy_nature':electrolyzer,'17_rf_nature':antenna,
 '18_mechanical_nature':mechanical,'20_thermal':thermal,
}

def build(case,version):
 if case not in ROUTINES:raise SystemExit('unknown case '+case)
 if version!='v01':raise SystemExit('first pass only; revisions have their own explicit scripts')
 r.setup();ROUTINES[case]()
 spec=CASES[case];sc=bpy.context.scene
 sc['source_doi']=next(x['doi'] for x in json.loads((ROOT/'candidate_metadata.json').read_text()) if x['id']==case)
 sc['source_location']=spec['figure'];sc['input_type']=spec['kind'];sc['source_basis']='text-only' if spec['kind']=='D' else 'figure-and-caption';sc['assumption']='all geometry units/placements are illustrative, not measured CAD'
 sc['review_status']='unreviewed_low_cost_preview';sc['unknowns']=spec['limit']
 out=ROOT/'cases'/case/version;out.mkdir(parents=True,exist_ok=True)
 bpy.context.view_layer.update();sc.camera.data.lens=50
 bpy.ops.wm.save_as_mainfile(filepath=str(out/'scene.blend'))
 print('SAVED_CASE',case,version,'OBJECTS',len(bpy.data.objects),'SCENE',out/'scene.blend',flush=True)

if __name__=='__main__':
 args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
 if len(args)!=2:raise SystemExit('usage: blender -b --python build_cases.py -- CASE v01')
 build(*args)
