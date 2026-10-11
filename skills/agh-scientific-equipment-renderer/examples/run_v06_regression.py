#!/usr/bin/env python3
"""Tiny synthetic PASS/FAIL/UNKNOWN regressions; no old-case render or visual acceptance.
python3 examples/run_v06_regression.py --blender /path/to/Blender --report /tmp/agh-v06-results.json
"""
import argparse,copy,json,subprocess,tempfile,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from validate_project_record import validate
ap=argparse.ArgumentParser();ap.add_argument('--blender',default='blender');ap.add_argument('--report',required=True);args=ap.parse_args()
base=json.loads((ROOT/'examples/valid_record.json').read_text());rows=[]
def record_case(name,mutator,expect,code=None):
 d=copy.deepcopy(base);mutator(d);result=validate(d)
 codes=[x['code'] for x in result['errors']+result['unknown']]
 ok=result['status']==expect and (not code or code in codes)
 rows.append({'name':name,'expected':expect,'actual':result['status'],'codes':codes,'pass':ok})
record_case('valid',lambda d:None,'PASS')
record_case('empty_scope',lambda d:[d['task'].__setitem__(k,[]) for k in ('required_components','required_connections','required_supports')],'UNKNOWN','REQUIRED_SCOPE_EMPTY')
record_case('empty_record',lambda d:[d.__setitem__(k,[]) for k in ('components','ports','connections','supports')],'FAIL','REQUIRED_MISSING')
record_case('missing_component',lambda d:d['components'].pop(),'FAIL','REQUIRED_MISSING')
record_case('wrong_port_owner',lambda d:d['ports'][0].__setitem__('owner','nobody'),'FAIL','PORT_OWNER_MISSING')
record_case('medium_mismatch',lambda d:d['ports'][0].__setitem__('medium','fluid'),'FAIL','MEDIUM_CONTRADICTION')
record_case('required_connection_missing',lambda d:d['connections'].clear(),'FAIL','REQUIRED_MISSING')
record_case('support_missing',lambda d:d['supports'].clear(),'FAIL','REQUIRED_MISSING')
record_case('no_text_with_label',lambda d:d['task']['outputs'].__setitem__('annotations','none'),'FAIL','LABELS_FORBIDDEN')
with tempfile.TemporaryDirectory() as tmp:
 tmp=Path(tmp);scene=tmp/'fixture.blend';make=ROOT/'examples/make_synthetic_scene.py';audit=ROOT/'scripts/audit_saved_scene.py';label=ROOT/'scripts/make_svg_labels.py'
 build=subprocess.run([args.blender,'--background','--python',str(make),'--',str(scene)],capture_output=True,text=True)
 rows.append({'name':'make_scene','expected_exit':0,'actual_exit':build.returncode,'pass':build.returncode==0 and scene.exists()})
 if scene.exists():
  # Different saved scenes, no regeneration from historic research case.
  script=tmp/'mutate.py';script.write_text('''import bpy,sys\nfrom mathutils import Vector\nmode=sys.argv[-2];target=sys.argv[-1]\nif mode=="endpoint":\n o=bpy.data.objects["rod_curve"];o.location.x+=.5\nelif mode=="horizontal":\n cam=bpy.context.scene.camera;o=bpy.data.objects["plate_mesh"];o.location+=cam.matrix_world.to_quaternion()@Vector((7,0,0))\nelif mode=="vertical":\n cam=bpy.context.scene.camera;o=bpy.data.objects["plate_mesh"];o.location+=cam.matrix_world.to_quaternion()@Vector((0,7,0))\nelif mode=="support":\n o=bpy.data.objects["plate_mesh"];o.location.z+=1\nbpy.ops.wm.save_as_mainfile(filepath=target)\n''')
  for name,mode,expected,code in [('valid_scene',None,'PASS','ENDPOINTS'),('world_endpoint_mismatch','endpoint','FAIL','ENDPOINTS'),('horizontal_outside','horizontal','FAIL','HORIZONTAL'),('vertical_outside','vertical','FAIL','VERTICAL'),('support_gap','support','FAIL','SUPPORT')]:
   path=scene if mode is None else tmp/(name+'.blend');rep=tmp/(name+'.json')
   if mode is not None:
    proc=subprocess.run([args.blender,'--background',str(scene),'--python',str(script),'--',mode,str(path)],capture_output=True,text=True)
    if proc.returncode or not path.exists():rows.append({'name':name,'pass':False,'mutation_exit':proc.returncode});continue
   proc=subprocess.run([args.blender,'--background',str(path),'--python',str(audit),'--',str(ROOT/'examples/valid_record.json'),'--report',str(rep)],capture_output=True,text=True)
   data=json.loads(rep.read_text()) if rep.exists() else {'status':'NO_REPORT','checks':[]}
   checks=[x for x in data['checks'] if x['code']==code and (name!='horizontal_outside' and name!='vertical_outside' or x['subject']=='plate')]
   depth=[x for x in data['checks'] if x['code']=='CLIP_DEPTH' and x['subject']=='plate']
   ok=data['status']==expected and proc.returncode==(0 if expected=='PASS' else 2) and any(x['status']==expected for x in checks)
   if name in ('horizontal_outside','vertical_outside'):ok=ok and bool(depth) and depth[0]['status']=='PASS'
   rows.append({'name':name,'expected':expected,'actual':data['status'],'exit':proc.returncode,'target_checks':checks,'clip_depth':depth,'pass':ok})
  lbl=tmp/'labels.svg';proc=subprocess.run([args.blender,'--background',str(scene),'--python',str(label),'--',str(ROOT/'examples/valid_record.json'),str(lbl)],capture_output=True,text=True)
  markup=lbl.read_text() if lbl.exists() else ''
  rows.append({'name':'svg_real_label','pass':proc.returncode==0 and 'data-target="plate"' in markup and '<line ' in markup and '>Plate<' in markup})
  nt=copy.deepcopy(base);nt['task']['outputs']['annotations']='none';nt['labels']=[];ntr=tmp/'no_text.json';ntr.write_text(json.dumps(nt));forbidden=tmp/'forbidden.svg'
  proc=subprocess.run([args.blender,'--background',str(scene),'--python',str(label),'--',str(ntr),str(forbidden)],capture_output=True,text=True)
  rows.append({'name':'no_text_svg_rejected','pass':not forbidden.exists() and 'forbidden' in proc.stdout+proc.stderr})
result={'status':'PASS' if all(x['pass'] for x in rows) else 'FAIL','cases':rows,
        'not_covered':['visual_similarity','scientific_function','fluid_seal','true_mechanical_load','occlusion']}
Path(args.report).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
for x in rows:print(('PASS' if x['pass'] else 'FAIL'),x['name'],x.get('actual',''))
print('RESULT',result['status']);raise SystemExit(0 if result['status']=='PASS' else 1)
