"""Saved Fig18 v06 limited geometric audit, not image/memory-mechanics validation."""
import bpy,sys,json,hashlib
from pathlib import Path
out=Path(sys.argv[sys.argv.index('--')+1]);bpy.context.view_layer.update();bpy.context.evaluated_depsgraph_get().update();o=bpy.data.objects;checks={}
checks['15_plus_15_continuous_families']=all(f'PIM_interlaced_front_{j}' in o and f'CIM_interlaced_cross_{j}' in o for j in range(15))
checks['old_regular_v05_removed']=not any(n.startswith(('PIM_dense_wavy_','CIM_dense_wavy_')) for n in o.keys())
checks['saved_plate_pair']=all(f'Fig18_{label}_compression_plate' in o for label in ('upper','lower'))
checks['fig18_only']='Fig18' in bpy.context.scene.get('source_location','') and 'Fig19' not in bpy.context.scene.get('source_location','')
checks['bezier_c1_continuity']=all(len(o[f'{family}_{j}'].data.splines)==1 and o[f'{family}_{j}'].data.splines[0].type=='BEZIER' and all(p.handle_left_type=='AUTO' and p.handle_right_type=='AUTO' for p in o[f'{family}_{j}'].data.splines[0].bezier_points) for family in ('PIM_interlaced_front','CIM_interlaced_cross') for j in range(15))
checks['broader_than_v05_bevel']=all(o[f'{family}_{j}'].data.bevel_depth>=.015 for family in ('PIM_interlaced_front','CIM_interlaced_cross') for j in range(15))
file=Path(bpy.data.filepath);report={'scene_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'checks':checks,'fails':[k for k,v in checks.items() if not v],'scope':'curve families, smooth handles, width and plate preservation only','unknown':'actual 3D crossing, node bonding, depth, appearance and material strength NOT VERIFIED','visual_review':'PENDING_EXTERNAL'}
out.write_text(json.dumps(report,indent=2,ensure_ascii=False));print('FIG18_V06_AUDIT',report['fails'],flush=True)
if report['fails']:raise SystemExit(2)
