"""Targeted saved-scene scope/real-geometry checks; *not* visual acceptance.
Usage blender -b scene.blend --python audit_stage5.py -- CASE report.json
"""
import bpy,sys,math,json,hashlib
from pathlib import Path
from mathutils import Vector
case,out=sys.argv[sys.argv.index('--')+1:];scene=bpy.context.scene;scene.view_layers[0].update();bpy.context.evaluated_depsgraph_get().update();o=bpy.data.objects;checks={};unknown=[]
def bounds(name,axis):
 ob=o[name];vals=[(ob.matrix_world@Vector(c))[axis] for c in ob.bound_box];return min(vals),max(vals)
def v_bounds(name,axis):
 ob=o[name];vals=[(ob.matrix_world@v.co)[axis] for v in ob.data.vertices];return min(vals),max(vals)
def endpoints(name):
 ob=o[name];sp=ob.data.splines[0];pts=sp.bezier_points if sp.type=='BEZIER' else sp.points
 return ob.matrix_world@Vector(pts[0].co[:3]),ob.matrix_world@Vector(pts[-1].co[:3])
def near(x,y,t=.012):return abs(x-y)<t
def ov(a,b):return a[0]<=b[1] and b[0]<=a[1]
if case=='02_robotics':
 for lab in ('lower','upper'):
  c=o[f'Soft_coupon_{lab}_clamped'];j0=o[f'{lab}_jaw_at_-0.13'];j1=o[f'{lab}_jaw_at_0.13']
  checks[lab+'_opposed_surfaces']=near(bounds(j0.name,1)[1],bounds(c.name,1)[0],.03) and near(bounds(j1.name,1)[0],bounds(c.name,1)[1],.03)
  checks[lab+'_axial_insert']=ov(bounds(j0.name,2),bounds(c.name,2)) and ov(bounds(j1.name,2),bounds(c.name,2))
  checks[lab+'_outer_rails']=all(f'{lab}_jaw_outer_rail_{j}' in o for j in (0,1))
 for x in (-1,1):checks[f'guide_{x}_upper_beam']=ov(bounds(f'Linear_guide_{x}',2),bounds('Testing_machine_upper_frame',2))
 unknown=['mechanical clamping force and manufacturer fixture shape unmeasured']
elif case=='13_biomed_optics':
 checks['physical_distal_head']='Distal_endoscope_head_housing' in o
 checks['distal_window_on_housing']=near(v_bounds('Distal_optical_end_window',1)[1],v_bounds('Distal_endoscope_head_housing',1)[0],.06)
 shaft_end=endpoints('Flexible_scope_outer_tube')[1];head=o['Distal_endoscope_head_housing']
 checks['shaft_in_distal_head']=math.dist(shaft_end,head.location)<.035
 for i in range(3):
  checks[f'independent_rear_ferrule_{i}']=all(name in o for name in (f'MLE_fiber_plug_{i}',f'Coupler_visible_collar_{i}',f'Flexible_fiber_source_to_probe_{i}'))
  a,b=endpoints(f'Flexible_fiber_source_to_probe_{i}');checks[f'fiber_{i}_back_ferrule']=near(b.y,v_bounds(f'MLE_fiber_plug_{i}',1)[0],.015)
 unknown=['internal optic/light transport, sealed insertion depth and viewing-window optics not measured']
elif case=='14_acoustic_alt':
 a,b=endpoints('LDV_to_levitated_sample_sampling_path');lens=v_bounds('LDV_front_lens',2);target=v_bounds('Levitated_sample_noncontact',2);s=o['Levitated_sample_noncontact'].location
 checks['path_starts_lens_bottom']=near(a.z,lens[0],.02)
 checks['path_hits_sample_top']=near(b.z,target[1],.02) and math.dist((b.x,b.y),(s.x,s.y))<.01
 checks['stand_base_head_chain']=all(n in o for n in ('LDV_mount_base','LDV_floor_mount_column','LDV_overhead_arm','LDV_head_clamp'))
 unknown=['this is graphic alignment only, not real laser wavelength, optical focus or levitation force']
elif case=='16_energy_nature':
 for g in ('CO2_cathode','Ar_anode'):
  start,end=endpoints(g+'_gas_source_to_MFC');mid,back=endpoints(g+'_MFC_to_cell_rear')
  checks[g+'_source_cap']=near(start.y,v_bounds(g+'_source_visible_socket',1)[0],.015)
  checks[g+'_MFC_input_cap']=near(end.y,v_bounds(g+'_MFC_inlet_socket',1)[1],.015)
  checks[g+'_MFC_output_cap']=near(mid.y,v_bounds(g+'_MFC_outlet_socket',1)[0],.015)
  checks[g+'_cell_rear_cap']=near(back.y,v_bounds(g+'_back_gas_stub',1)[1],.015)
  checks[g+'_owned_supply_panel']=o[g+'_source_visible_socket'].get('owner')==g+'_assumed_source_panel'
 unknown=['upstream source panel and sleeves are explicit assumptions; internal gas/aqueous routes and regulator action unverified']
elif case=='20_thermal':
 checks['physical_east_cap']='East_final_closed_foil_endcap' in o
 cap=bounds('East_final_closed_foil_endcap',0);wick=bounds('Copper_wick_warp_0_0',0)
 checks['cap_beyond_wick_x']=cap[0]>wick[1]
 checks['all_four_final_seams']=all('Foil_heat_seam_'+n in o for n in ('front','rear','west','east_final'))
 checks['preseal_objects_absent']=not any(n.startswith('Heat_seal_') for n in o.keys())
 unknown=['visibility through camera and real hermetic seal not tested; preseal view is separate scene']
elif case=='18_mechanical_nature':
 checks['fig18_face_dimensions_metadata']=scene.get('known_size','').startswith('20 mm x 20 mm')
 checks['seven_plus_seven_strands']=all(f'PIM_vertical_visible_strand_{j}' in o and f'CIM_cross_visible_strand_{j}' in o for j in range(7))
 checks['no_parent_TypeIV_in_fig18']='Parent_material_Type_IV_coupon' not in o
 checks['two_compression_plates']=all(f'Fig18_{lab}_compression_plate' in o for lab in ('lower','upper'))
 checks['fig18_scope_only']='Fig.18' in scene.get('source_location','') and 'NOT Fig17/19/20' in scene.get('source_location','')
 unknown=['lattice interweave bonds, 3D thickness, plate pressure and memory mechanics unknown']
else:raise RuntimeError(case)
file=Path(bpy.data.filepath);report={'case':case,'scene_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'checks':checks,'fails':[k for k,v in checks.items() if not v],'unknown':unknown,'visual_review':'NOT_PERFORMED','scope':'selected world-space interfaces/object identities; not image or function'}
Path(out).write_text(json.dumps(report,ensure_ascii=False,indent=2));print('STAGE5_AUDIT',case,report['fails'],flush=True)
if report['fails']:raise SystemExit(2)
