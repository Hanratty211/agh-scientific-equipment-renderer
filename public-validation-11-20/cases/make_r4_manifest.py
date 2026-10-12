"""Preserve four R3 image and scene hashes; replace only 12/16 versions."""
import json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parent.parent
prior=json.loads((root/'physical_feedback_r3_manifest.json').read_text());new=[]
for row in prior['cases']:
 n=row['case']
 if n not in (12,16):new.append(row.copy());continue
 d=next((root/'cases').glob(f'{n}_*'));v='v06' if n==12 else 'v07';R=json.loads((d/f'render_{v}_reloaded_r4.json').read_text());assert R['case']==n
 rec={'case':n,'version':v,'scene':R['scene'],'scene_sha256':R['scene_sha256'],'images':R['images'],
 'prior_failed_detail':{'case12':'detail_camera_data_rear_v05_reloaded_r2.png','case16':'detail_both_insulated_entries_v06_reloaded_r3.png'}['case12' if n==12 else 'case16'],
 'audit':{'path':str(d/f'audit_scene_{v}.json'),'status':'UNVERIFIED','declared_failures':[]},
 'limited_real_geometry':{'path':str(d/f'check_real_endpoints_{v}.json'),'status':'LIMITED_REAL_GEOMETRY_PASS'},
 'visual_judgment':'User rejected prior detail for visible gap/exposed bright tail; new detail awaits user pixel review; not accepted.',
 'unknown':['Specific product connector material/dimensions','Actual electrical/pressure function','Hidden internal routing']}
 new.append(rec)
r={'author':'AGH','case_scope':'ONLY 12 camera rear chain and two 16 exterior lead terminations; remaining four R3 image/scene assets exactly reused','user_visual_status':'prior details rejected; new two details PENDING user reading','geometry_status':'limited real meshes/world Bezier sampling; not visual/function approval','prior_manifest':'public-validation-11-20/physical_feedback_r3_manifest.json','cases':new}
for row in r['cases']:
 assert hashlib.sha256(Path(row['scene']).read_bytes()).hexdigest()==row['scene_sha256']
 for im in row['images']:assert hashlib.sha256(Path(im['path']).read_bytes()).hexdigest()==im['sha256']
(root/'physical_feedback_r4_manifest.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n');print('r4',[(x['case'],x['version'],len(x['images'])) for x in new])
