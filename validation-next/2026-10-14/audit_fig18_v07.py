"""Limited structural checks from independent Blender reload, not visual approval."""
import bpy,sys,json,hashlib
from pathlib import Path
from mathutils import Vector
out=Path(sys.argv[sys.argv.index('--')+1]);bpy.context.view_layer.update();bpy.context.evaluated_depsgraph_get().update();o=bpy.data.objects;checks={};a=[n.name for n in o if n.name.startswith('PIM_diagonal_weave_')];b=[n.name for n in o if n.name.startswith('CIM_diagonal_weave_')]
checks['two_complete_diagonal_families']=len(a)>=15 and len(b)>=15
checks['old_v06_family_removed']=not any(n.name.startswith(('PIM_interlaced_front_','CIM_interlaced_cross_')) for n in o)
checks['plates_exist']=all(f'Fig18_{s}_compression_plate' in o for s in ('upper','lower'))
checks['smooth_single_curve_per_object']=all(len(o[n].data.splines)==1 and o[n].data.splines[0].type=='BEZIER' and all(p.handle_left_type=='AUTO' and p.handle_right_type=='AUTO' for p in o[n].data.splines[0].bezier_points) for n in a+b)
checks['central_lanes_have_diagonal_span']=all((lambda points:max(p.co.x for p in points)-min(p.co.x for p in points)>.4 and max(p.co.z for p in points)-min(p.co.z for p in points)>.4)(o[n].data.splines[0].bezier_points) for n in a+b if int(n.rsplit('_',1)[1]) in range(4,13))
checks['both_ends_within_visible_face']=all(all(abs(pt.co.x)<=.671 and abs(pt.co.z-2.09)<=.671 for pt in (o[n].data.splines[0].bezier_points[0],o[n].data.splines[0].bezier_points[-1])) for n in a+b)
file=Path(bpy.data.filepath);report={'scene_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'counts':[len(a),len(b)],'checks':checks,'fails':[k for k,v in checks.items() if not v],'scope':'saved curves diagonal ranges, smooth handles, family count and retained compression plates only','unknown':'frame geometry not individually compared; visual read, 3D node bonding, actual depth and mechanics NOT VERIFIED','visual_review':'PENDING_EXTERNAL'}
out.write_text(json.dumps(report,ensure_ascii=False,indent=2));print('FIG18_V07_AUDIT',report['fails'],flush=True)
if report['fails']:raise SystemExit(2)
