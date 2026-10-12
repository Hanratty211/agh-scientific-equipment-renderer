"""Offline hash and pixel-difference verification; no rendering or Blender mutation.
A same-pixel PNG may have a different SHA due to metadata, record both.
"""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageChops,ImageStat
root=Path(__file__).resolve().parent;old={12:'v05',13:'v04',14:'v06',16:'v04',17:'v05',19:'v05'};new={12:'v05',13:'v04',14:'v06',16:'v05',17:'v05',19:'v06'}
rows=[]
for n,v in new.items():
 d=next(root.glob(f'{n}_*'));render=json.loads((d/f'render_{v}_reloaded_r2.json').read_text());scene=Path(render['scene']);assert scene.is_file() and hashlib.sha256(scene.read_bytes()).hexdigest()==render['scene_sha256']
 for image in render['images']:
  f=Path(image['path']);assert f.is_file() and hashlib.sha256(f.read_bytes()).hexdigest()==image['sha256']
 report=d/f'audit_reloaded_r2_{v}.json';audit=json.loads(report.read_text());assert audit['status']=='UNVERIFIED' and len(audit['failures'])==0
 extra={'case':n,'version':v,'scene':str(scene),'scene_sha256':render['scene_sha256'],'images':render['images'],'audit':{'status':audit['status'],'declared_failures':audit['failures'],'path':str(report)}}
 if n in (12,14,16,17,19):
  check=json.loads((d/f'check_r2_reloaded_{v}.json').read_text());assert check['status']=='LIMITED_GEOMETRY_PASS' and not any(row['status']=='FAIL' for row in check['checks']);extra['limited_geometry']={'status':check['status'],'checks':len(check['checks']),'path':str(d/f'check_r2_reloaded_{v}.json')}
 else:extra['limited_geometry']={'status':'prior check only','path':str(d/'physical_mesh_v04.json')}
 prev=d/f'overview_{old[n]}.png';a=Image.open(prev).convert('RGB');b=Image.open(render['images'][0]['path']).convert('RGB');assert a.size==b.size
 diff=ImageChops.difference(a,b)
 extra['prior_overview_observation']={'file':str(prev),'sha256':hashlib.sha256(prev.read_bytes()).hexdigest(),'current_reloaded_same_RGB_pixels':diff.getbbox() is None,'RGB_diff_bbox':diff.getbbox(),'mean_abs_RGB':sum(ImageStat.Stat(diff).mean)/3}
 rows.append(extra)
rear=dummy=next(root.glob('12_*'))/'detail_camera_data_rear_v05_reloaded_r2.json';r=json.loads(rear.read_text());assert hashlib.sha256(Path(r['scene']).read_bytes()).hexdigest()==r['scene_sha256'] and hashlib.sha256(Path(r['image']).read_bytes()).hexdigest()==r['image_sha256'];rows[0]['images'].append({'label':'camera_data_rear_positive_Y_oblique','path':r['image'],'sha256':r['image_sha256'],'camera':r['camera'],'no_hide':r['no_object_or_render_state_mutations']})
result={'author':'AGH','scope':'six saved-scene-reloaded low-cost representative previews; no commercial CAD/functional validation','cases':rows,'renderer':'Blender 5.1.2 background, independent subprocess reload for each saved scene','previous_stage':'R1 first-pass images and user historical observation retained without overwrite','visual_authority':'user reviewed six reloaded overviews and main details as representative low-cost preview; newly-added rear camera detail still pending user check','external_probe_authority':'Codex probe and runtime comparison separate from AGH scene checks'}
out=root.parent/'physical_feedback_r2_manifest.json';out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print('R2_MANIFEST',out,'cases',len(rows),'images',sum(len(row['images']) for row in rows))
