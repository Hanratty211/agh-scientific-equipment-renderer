import bpy,sys,json,hashlib
from pathlib import Path
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:];case,output=args
bpy.context.view_layer.update();bpy.context.evaluated_depsgraph_get().update();o=bpy.data.objects
checks={};notes=[]
def bounds(n,axis):
 obj=o[n];return (min((obj.matrix_world@v.co)[axis] for v in obj.data.vertices),max((obj.matrix_world@v.co)[axis] for v in obj.data.vertices))
def ends(n):
 obj=o[n];sp=obj.data.splines[0]; pts=[sp.bezier_points[0].co,sp.bezier_points[-1].co] if sp.type=='BEZIER' else [sp.points[0].co.xyz,sp.points[-1].co.xyz];return [obj.matrix_world@p for p in pts]
if case=='02_robotics':
 for g,c,z in [('lower','Soft_coupon_lower_clamped',.66),('upper','Soft_coupon_upper_clamped',2.51)]:
  lo,hi=bounds(c,2);jaws=[o[f'{g}_jaw_at_{y}'] for y in (-.13,.13)]; checks[g+'_coupon_z_inside_grip']=lo<z<hi;checks[g+'_jaw_pair']=len(jaws)==2
  # Jaw gap ±.065, specimen faces ±.06; check face clearance explicitly and do not claim clamp pressure.
  checks[g+'_face_gap_small']=abs(bounds(jaws[0].name,1)[1]-bounds(c,1)[0])<.02 and abs(bounds(jaws[1].name,1)[0]-bounds(c,1)[1])<.02
 notes+=['Jaw-specimen near-face, no force/contact stress evidence']
elif case=='13_biomed_optics':
 for i,x in enumerate((.85,1.15,1.45)):
  a,b=ends(f'Fiber_source_to_scope_{i}');source=bounds(f'Illuminator_exterior_plug_{i}',1);plug=bounds(f'MLE_fiber_plug_{i}',1)
  checks[f'fiber_{i}_source']=abs(a.y-source[0])<.005;checks[f'fiber_{i}_probe']=abs(b.y-plug[0])<.06
 notes+=['External coupler only, no optical transmission or internal seals']
elif case=='14_acoustic_alt':
 a=o['LDV_front_lens'].location;b=o['Levitated_sample_noncontact'].location
 checks['ldv_target_x_aligned']=abs(a.x-b.x)<.002;checks['ldv_target_y_aligned']=abs(a.y-b.y)<.002;checks['ldv_above_sample_shaker']=a.z>b.z>o['Vibration_shaker'].location.z
 notes+=['Spatial axis only, not laser focus or acoustic-force measurement']
elif case=='15_biomed_energy':
 checks['two_batteries']=all(f'LiPo_battery_{i}' in o for i in range(2));checks['pv_window_cover']=all(n in o for n in ['Upper_silicone_skin','Photovoltaic_cell','PL_silicone_encapsulation']);checks['four_visual_spacers']=all(f'Patch_alignment_spacer_{i}_{j}' in o for i in range(2) for j in range(2))
 notes+=['No electrical connections, seal or body contact audit']
elif case=='16_energy_nature':
 checks['unfounded_cups_removed']=not any('vessel' in n.lower() or 'reservoir' in n.lower() for n in o.keys());checks['two_gas_lines']=all(f'{n}_external_gas' in o for n in ['CO2_cathode','Ar_anode']);checks['two_mfc']=all(f'{n}_MFC' in o for n in ['CO2_cathode','Ar_anode']);checks['distinct_gas_liquid_lines']=all(n in o for n in ['Electrolyte_pump_to_cell','Spent_electrolyte_off_frame'])
 for n in ['CO2_cathode','Ar_anode']:
  end=ends(f'{n}_external_gas')[-1];stub=bounds(f'{n}_back_gas_stub',1);checks[n+'_rear_stub']=abs(end.y-stub[1])<.01
 notes+=['Liquid and gas geometry distinct; flow paths, channels and MFC function not checked']
elif case=='17_rf_nature':
 checks['single_substrate']=sum('substrate' in n.lower() for n in o.keys())==1;checks['ground_boolean_holes']=all('Ground_open_slot_'+str(i) not in o.keys() for i in (0,1)) and all('Elliptical_slot_cutter_'+str(i) not in o.keys() for i in (0,1));checks['feed_contact_exists']='Feed_to_resonator_contact' in o
 notes+=['Boolean topology and electromagnetic feed continuity require further inspection']
elif case=='18_mechanical_nature':
 checks['parent_material_coupon']='Parent_material_Type_IV_coupon' in o;checks['ladder_removed']=not any(n.startswith('PIM_chain_') for n in o.keys());checks['jaw_pairs']=all(f'{g}_grip_face_{i}' in o for g in ('upper','lower') for i in (0,1));checks['scope_property']='parent-material' in o['Parent_material_Type_IV_coupon']['scope']
 notes+=['ASTM type applies to parent materials, not PIM or CIM; grip force not tested']
elif case=='20_thermal':
 for n in ('north','south','west','east_final'):checks[n+'_seal_exists']='Heat_seal_'+n in o
 checks['top_and_bottom_foil']=all(n in o for n in ('Flexible_al_plastic_top_foil','Aluminum_plastic_lower_casing'))
 notes+=['Opaque final scene; wick not visible unless separate process detail; no inner flow check']
else:raise ValueError(case)
rep={'case':case,'scene_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'checks':checks,'fails':[k for k,v in checks.items() if not v],'limits':notes,'scope':'Identity/presence/selected world-space geometry only; not pixel or functional acceptance'}
Path(output).write_text(json.dumps(rep,ensure_ascii=False,indent=2));print('CASE_AUDIT',case,rep['fails'],flush=True)
if rep['fails']:sys.exit(2)
