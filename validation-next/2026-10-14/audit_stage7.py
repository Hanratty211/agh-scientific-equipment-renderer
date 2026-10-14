"""Reloaded scene limited geometry QA; no claim of visibility, optical performance or weave bonds.
Blender -b scene.blend --python audit_stage7.py -- CASE report.json
"""
import bpy,sys,json,hashlib,math
from pathlib import Path
from mathutils import Vector
case,out=sys.argv[sys.argv.index('--')+1:];bpy.context.view_layer.update();bpy.context.evaluated_depsgraph_get().update();o=bpy.data.objects;checks={};unknown=[]
def bounds(n,a):
 ob=o[n];v=[(ob.matrix_world@Vector(c))[a] for c in ob.bound_box];return min(v),max(v)
def eps(a,b,t=.018):return abs(a-b)<t
if case=='13_biomed_optics':
 body=o['Distal_long_scope_head'];nose=o['Distal_tapered_optic_nose'];win=o['Distal_visible_clear_optical_face']
 checks['three_independent_rear_fibers']=all(f'Flexible_fiber_source_to_probe_{i}' in o for i in range(3))
 checks['sleeve_to_body_chain']=all(n in o for n in ('Distal_scope_shaft_sleeve','Distal_scope_tapered_neck','Distal_long_scope_head'))
 checks['front_rim_and_glass']=all(n in o for n in ('Distal_window_outer_lens_ring','Distal_window_inner_lens_ring','Distal_window_black_throat','Distal_visible_clear_optical_face'))
 checks['window_aligned_on_head_axis']=eps(win.location.x,body.location.x,.003) and eps(win.location.z,body.location.z,.003)
 checks['window_proud_of_nose']=bounds(win.name,1)[1]<bounds(nose.name,1)[0]+.050
 checks['nasal_taper_real_mesh']=len(nose.data.vertices)>=90 and any(m.type=='SOLIDIFY' for m in nose.modifiers)
 unknown=['glass visibility/brightness is a pixel judgement; exact optics, light throughput and head dimensions not supplied']
elif case=='18_mechanical_nature':
 checks['dense_two_families']=all(f'PIM_dense_wavy_{j}' in o and f'CIM_dense_wavy_{j}' in o for j in range(13))
 checks['old_knotted_family_removed']=not any(n.startswith(('PIM_wavy_visible_strand_','CIM_wavy_cross_strand_')) for n in o.keys())
 for family in ('PIM_dense_wavy_','CIM_dense_wavy_'):
  checks[family+'_single_smooth_splines']=all(len(o[family+str(j)].data.splines)==1 and o[family+str(j)].data.splines[0].type=='BEZIER' and len(o[family+str(j)].data.splines[0].bezier_points)==73 for j in range(13))
 checks['compression_plates_unchanged']=all('Fig18_'+p+'_compression_plate' in o for p in ('upper','lower'))
 checks['fig18_visible_face_metadata']='20x20mm' in bpy.context.scene.get('stage7_note','')
 unknown=['front density/pixel legibility remains for external reviewer; strand crossings, joint bonds, real 3D thickness and load not verified']
else:raise RuntimeError('unsupported case')
file=Path(bpy.data.filepath);report={'case':case,'scene_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'checks':checks,'fails':[n for n,v in checks.items() if not v],'unknown':unknown,'visual_review':'PENDING_EXTERNAL'}
Path(out).write_text(json.dumps(report,ensure_ascii=False,indent=2));print('STAGE7_AUDIT',case,report['fails'],flush=True)
if report['fails']:raise SystemExit(2)
