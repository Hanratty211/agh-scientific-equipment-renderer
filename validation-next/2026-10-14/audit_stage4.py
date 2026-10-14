"""Independent saved-scene geometry audit: finite interfaces/supports, not pixels or function.
Blender -b scene.blend --python audit_stage4.py -- CASE_ID report.json
"""
import bpy,sys,json,hashlib,math
from pathlib import Path
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:];case=args[0];output=Path(args[1]);bpy.context.view_layer.update();bpy.context.evaluated_depsgraph_get().update();o=bpy.data.objects
checks={};limits=[]
def bbox(name,a):
 obj=o[name];vals=[(obj.matrix_world@Vector(c))[a] for c in obj.bound_box];return min(vals),max(vals)
def mesh_bounds(name,a):
 obj=o[name];vals=[(obj.matrix_world@v.co)[a] for v in obj.data.vertices];return min(vals),max(vals)
def curve_ends(name):
 obj=o[name];sp=obj.data.splines[0];p=[sp.bezier_points[0].co,sp.bezier_points[-1].co] if sp.type=='BEZIER' else [sp.points[0].co.xyz,sp.points[-1].co.xyz];return obj.matrix_world@p[0],obj.matrix_world@p[1]
def overlap(a,b):return a[0]<=b[1] and b[0]<=a[1]
def near(a,b,tol=.012):return abs(a-b)<=tol
if case=='02_robotics':
 for x in (-1,1):
  g=bbox(f'Linear_guide_{x}',2);top=bbox('Testing_machine_upper_frame',2);bottom=bbox('Testing_machine_lower_frame',2)
  checks[f'guide_{x}_upper_contact']=overlap(g,top);checks[f'guide_{x}_lower_contact']=overlap(g,bottom)
 for label in ('lower','upper'):
  s=bbox(f'Soft_coupon_{label}_clamped',2);j=bbox(f'{label}_jaw_at_-0.13',2);checks[f'{label}_coupon_into_jaw']=overlap(s,j)
 limits=['Overlap only, no grip force/material constitutive model']
elif case=='08_biomedical':
 surf=bbox('Conductive_silicone_P1',0),bbox('Conductive_silicone_P1',1);pad=bbox('P1_measurement_point',0),bbox('P1_measurement_point',1)
 checks['pad_xy_inside_P1']=all(surf[i][0]<=pad[i][0]<=pad[i][1]<=surf[i][1] for i in (0,1))
 for i in range(6):
  c=o[f'P1_continuous_fan_{i}'];pts=[c.matrix_world@p.co for p in c.data.splines[0].bezier_points]
  checks[f'fan_{i}_inside_P1_xy']=all(surf[0][0]<=v.x<=surf[0][1] and surf[1][0]<=v.y<=surf[1][1] for v in pts)
  checks[f'fan_{i}_ends_on_pad_xy']=pad[0][0]<=pts[-1].x<=pad[0][1] and pad[1][0]<=pts[-1].y<=pad[1][1]
 lead,_=curve_ends('P1_external_lead_flexible');socket=mesh_bounds('P1_visible_lead_socket',1);checks['lead_begins_socket_face']=near(lead.y,socket[0],.005)
 limits=['Only control points and visible pad/sleeve proximity; no electrical continuity or through-layer contact']
elif case=='13_biomed_optics':
 for i in range(3):
  a,b=curve_ends(f'Flexible_fiber_source_to_probe_{i}');s=mesh_bounds(f'Illuminator_exterior_plug_{i}',1);t=mesh_bounds(f'MLE_fiber_plug_{i}',1)
  checks[f'fiber_{i}_source_face']=near(a.y,s[0],.008);checks[f'fiber_{i}_back_connector']=near(b.y,t[0],.008)
  checks[f'fiber_{i}_bezier']='BEZIER'==o[f'Flexible_fiber_source_to_probe_{i}'].data.splines[0].type
 limits=['Three separate flexible exterior curves only; no optical coupling/insertion depth confirmation']
elif case=='14_acoustic_alt':
 arm=bbox('LDV_overhead_arm',0);head=bbox('LDV_optical_head',0);stand=bbox('LDV_floor_mount_column',2);base=bbox('LDV_mount_base',2)
 checks['stand_to_base']=overlap(stand,base);checks['arm_to_head_x']=overlap(arm,head);checks['arm_to_stand_x']=overlap(arm,bbox('LDV_floor_mount_column',0))
 checks['LDV_above_sample']=o['LDV_optical_head'].location.z>o['Levitated_sample_noncontact'].location.z
 limits=['Mount schematic only; shaft support and alignment unverified by pixels']
elif case=='16_energy_nature':
 for key in ('CO2_cathode','Ar_anode'):
  a,b=curve_ends(key+'_gas_source_to_MFC');c,d=curve_ends(key+'_MFC_to_cell_rear')
  checks[key+'_source_to_MFC_in']=near(b.y,mesh_bounds(key+'_MFC_inlet_socket',1)[1],.015)
  checks[key+'_MFC_out_to_curve']=near(c.y,mesh_bounds(key+'_MFC_outlet_socket',1)[0],.015)
  checks[key+'_curve_to_cell_rear']=near(d.y,mesh_bounds(key+'_back_gas_stub',1)[1],.015)
  checks[key+'_two_independent_curves']=all(n in o for n in (key+'_gas_source_to_MFC',key+'_MFC_to_cell_rear'))
 limits=['All sockets are representative external fittings, not bores, MFC function or mass flow']
elif case=='17_rf_nature':
 sub=bbox('Dielectric_substrate',2);ground=bbox('Ground_plane',2);rad=bbox('Dielectric_resonator_conical_radiator',2)
 checks['substrate_ground_face']=near(sub[1],ground[0],.015);checks['radiator_ground_surface']=near(rad[0],ground[1],.025)
 f=bbox('Copper_feed_footprint',1);t=bbox('Copper_feed_to_DRA_base',1);co=bbox('Feed_edge_connector',1)
 checks['connector_to_feed_y']=overlap(f,co);checks['feed_to_tip_y']=overlap(f,t)
 checks['two_existing_ground_boolean_modifiers']=not any(n.startswith('Elliptical_slot_cutter_') for n in o.keys())
 limits=['Geometric contact/overlap only; grounding and RF current not validated']
elif case=='20_thermal':
 checks['folded_skin_mesh']='Flexible_alplastic_folded_skin' in o;checks['four_thin_seams']=all('Foil_heat_seam_'+n in o for n in ('front','rear','west','east_final'))
 checks['old_rigid_blocks_removed']=not any(n.startswith('Heat_seal_') for n in o.keys())
 checks['same_wick_in_scene']=any(n.startswith('Copper_wick_warp_') for n in o.keys())
 limits=['Foil represented by editable thin shell and seams, not proven flexibility/microstructure or internal flow']
elif case=='15_biomed_energy':
 b=bbox('PL_silicone_encapsulation',2);pcb=bbox('Flexible_printed_circuit',2);pv=bbox('Photovoltaic_cell',2);skin=bbox('Upper_silicone_skin',2)
 checks['stack_order']=b[0]<pcb[0]<pv[0]<skin[0]
 checks['common_patch_center']=all(abs(o[n].location.x)<.001 and abs(o[n].location.y)<.001 for n in ('PL_silicone_encapsulation','Flexible_printed_circuit','Photovoltaic_cell','Upper_silicone_skin'))
 checks['old_standoff_removed']=not any(n.startswith('Patch_alignment_spacer_') for n in o.keys())
 limits=['Exploded visual stack only; electrical contact and sealing unknown']
else:raise RuntimeError(case)
file=Path(bpy.data.filepath);rep={'case':case,'scene_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'checks':checks,'fails':[k for k,v in checks.items() if not v],'limits':limits,'visual_review':'NOT_PERFORMED'}
output.write_text(json.dumps(rep,ensure_ascii=False,indent=2));print('STAGE4_AUDIT',case,rep['fails'],flush=True)
if rep['fails']:raise SystemExit(2)
