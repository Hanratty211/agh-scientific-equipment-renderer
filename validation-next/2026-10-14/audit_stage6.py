"""Stage6 saved-scene geometry sanity, not pixel acceptance or function.
Blender -b scene.blend --python audit_stage6.py -- CASE report.json
"""
import bpy,sys,math,hashlib,json
from pathlib import Path
from mathutils import Vector
case,path=sys.argv[sys.argv.index('--')+1:];bpy.context.view_layer.update();bpy.context.evaluated_depsgraph_get().update();o=bpy.data.objects;checks={};unknown=[]
def bounds(name,axis):
 ob=o[name];vals=[(ob.matrix_world@Vector(c))[axis] for c in ob.bound_box];return min(vals),max(vals)
def evaluated_nearest_ray(name,origin,direction,distance=5):
 ob=o[name];deps=bpy.context.evaluated_depsgraph_get();ev=ob.evaluated_get(deps)
 # Object.ray_cast expects local coordinates; transform ray once using inverse world matrix.
 inv=ev.matrix_world.inverted();p=inv@Vector(origin);d=(inv.to_3x3()@Vector(direction)).normalized()
 return ev.ray_cast(p,d,distance=distance)
if case=='13_biomed_optics':
 checks['three_independent_rear_fibers']=all(f'Flexible_fiber_source_to_probe_{i}' in o for i in range(3))
 shaft=o['Flexible_scope_outer_tube'];sp=shaft.data.splines[0];end=shaft.matrix_world@sp.bezier_points[-1].co
 checks['shaft_to_sleeve']=math.dist(end,o['Distal_scope_shaft_sleeve'].location)<.10
 checks['slender_head_exists']=all(n in o for n in ['Distal_scope_tapered_neck','Distal_long_scope_head','Distal_front_bezel','Distal_optical_front_window'])
 checks['longer_than_previous_short_cap']=(bounds('Distal_long_scope_head',1)[1]-bounds('Distal_long_scope_head',1)[0])>(bounds('Distal_scope_shaft_sleeve',1)[1]-bounds('Distal_scope_shaft_sleeve',1)[0])
 checks['front_window_on_head_axis']=abs(o['Distal_optical_front_window'].location.x-o['Distal_long_scope_head'].location.x)<.002 and abs(o['Distal_optical_front_window'].location.z-o['Distal_long_scope_head'].location.z)<.002
 unknown=['three rear fibers do not prove internal coupling; distal optical design and exact dimensions unknown']
elif case=='14_acoustic_alt':
 top=o['TinyLev_upper_plate'];target=o['Levitated_sample_noncontact'];bore=o['Top_plate_bore_visible_rim'];beam_obj=o['LDV_to_levitated_sample_sampling_path'];sp=beam_obj.data.splines[0];start=beam_obj.matrix_world@sp.bezier_points[0].co;end=beam_obj.matrix_world@sp.bezier_points[-1].co
 checks['bore_and_target_xy']=math.dist((bore.location.x,bore.location.y),(target.location.x,target.location.y))<.002
 checks['ray_xy_centered']=math.dist((end.x,end.y),(target.location.x,target.location.y))<.002
 # A ray toward the plate center should miss the actual evaluated boolean mesh; a nearby ray should hit.
 plate_top=max((top.matrix_world@Vector(c)).z for c in top.bound_box)
 hit_center=evaluated_nearest_ray('TinyLev_upper_plate',(target.location.x,target.location.y,plate_top+.25),(0,0,-1))[0]
 hit_solid=evaluated_nearest_ray('TinyLev_upper_plate',(target.location.x+.28,target.location.y,plate_top+.25),(0,0,-1))[0]
 checks['center_ray_passes_real_aperture']=not hit_center;checks['offaxis_ray_hits_solid_plate']=bool(hit_solid)
 checks['lens_above_target']=start.z>end.z
 unknown=['hole radius/photographic appearance approximate; optical focus, spot wavelength and sound pressure not verified']
elif case=='18_mechanical_nature':
 checks['seven_continuous_wavy_families']=all(f'PIM_wavy_visible_strand_{j}' in o and f'CIM_wavy_cross_strand_{j}' in o for j in range(7))
 checks['straight_v03_rods_removed']=not any(n.startswith(('PIM_vertical_visible_strand_','CIM_cross_visible_strand_')) for n in o.keys())
 for j in range(7):
  for family in ('PIM_wavy_visible_strand_','CIM_wavy_cross_strand_'):
   sp=o[family+str(j)].data.splines[0];checks[f'{family}{j}_single_bezier']=len(o[family+str(j)].data.splines)==1 and sp.type=='BEZIER' and len(sp.bezier_points)==49
 checks['plates_retained']=all(f'Fig18_{x}_compression_plate' in o for x in ('upper','lower'))
 checks['no_parent_coupon']='Parent_material_Type_IV_coupon' not in o
 unknown=['20x20 mm face only; true internal interweave junctions and depth unverified; no strength/memory test']
else:raise RuntimeError('case')
file=Path(bpy.data.filepath);d={'case':case,'scene_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'checks':checks,'fails':[k for k,v in checks.items() if not v],'unknown':unknown,'visual_review':'PENDING_NEW_EXTERNAL'}
Path(path).write_text(json.dumps(d,indent=2,ensure_ascii=False));print('STAGE6_AUDIT',case,d['fails'],flush=True)
if d['fails']:raise SystemExit(2)
