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
record_case('kind_medium_mismatch',lambda d:d['connections'][0].__setitem__('kind','optical'),'FAIL','KIND_MEDIUM_CONTRADICTION')
record_case('nan_support_tolerance',lambda d:d['supports'][0].__setitem__('tolerance',float('nan')),'FAIL','SUPPORT_TOLERANCE_INVALID')
record_case('infinite_port_tolerance',lambda d:d['ports'][0].__setitem__('surface_tolerance',float('inf')),'FAIL','PORT_TOLERANCE_INVALID')
record_case('bool_connection_tolerance',lambda d:d['connections'][0].__setitem__('tolerance',True),'FAIL','CONNECTION_TOLERANCE_INVALID')
record_case('bad_owner_type',lambda d:d['ports'][0].__setitem__('owner',[]),'FAIL','PORT_OWNER_BAD_ID')
record_case('bad_required_type',lambda d:d['task'].__setitem__('required_components',[{}]),'FAIL','REQUIRED_BAD_ID')
record_case('bad_kind_type',lambda d:d['connections'][0].__setitem__('kind',[]),'FAIL','CONNECTION_KIND')
record_case('task_kind_list',lambda d:d['task'].__setitem__('kind',[]),'FAIL','TASK_KIND')
record_case('port_medium_dict',lambda d:d['ports'][0].__setitem__('medium',{}),'FAIL','PORT_MEDIUM')
record_case('task_outputs_list',lambda d:d['task'].__setitem__('outputs',[]),'FAIL','OUTPUTS_TYPE')
def one_component(d):
 d['task']['required_components']=['base'];d['task']['required_connections']=[];d['task']['required_supports']=[]
 d['components']=[d['components'][0]];d['ports']=[];d['connections']=[];d['supports']=[];d['labels']=[];d['task']['outputs']['annotations']='none'
record_case('single_component_no_interfaces',one_component,'UNKNOWN','NO_PORTS')
record_case('unknown_size_basis',lambda d:d['components'][0].__setitem__('size_basis','unknown'),'UNKNOWN','SIZE_BASIS_UNKNOWN')
record_case('nonphysical_medium_not_inferred',lambda d:(d['connections'][0].__setitem__('kind','field'),d['connections'][0].__setitem__('medium','unknown')),'UNKNOWN','NONPHYSICAL_ROUTE_OBJECT')
with tempfile.TemporaryDirectory() as tmp:
 tmp=Path(tmp);scene=tmp/'fixture.blend';make=ROOT/'examples/make_synthetic_scene.py';audit=ROOT/'scripts/audit_saved_scene.py';label=ROOT/'scripts/make_svg_labels.py'
 build=subprocess.run([args.blender,'--background','--python',str(make),'--',str(scene)],capture_output=True,text=True)
 rows.append({'name':'make_scene','expected_exit':0,'actual_exit':build.returncode,'pass':build.returncode==0 and scene.exists()})
 if scene.exists():
  # Different saved scenes, no regeneration from historic research case.
  script=tmp/'mutate.py';script.write_text('''import bpy,sys\nfrom mathutils import Vector\nmode=sys.argv[-2];target=sys.argv[-1]\nif mode=="endpoint":\n o=bpy.data.objects["rod_curve"];o.location.x+=.5\nelif mode=="horizontal":\n cam=bpy.context.scene.camera;o=bpy.data.objects["plate_mesh"];o.location+=cam.matrix_world.to_quaternion()@Vector((7,0,0))\nelif mode=="vertical":\n cam=bpy.context.scene.camera;o=bpy.data.objects["plate_mesh"];o.location+=cam.matrix_world.to_quaternion()@Vector((0,7,0))\nelif mode=="support":\n o=bpy.data.objects["plate_mesh"];o.location.z+=1\nelif mode=="face_interior_contact":\n o=bpy.data.objects["plate_mesh"];o.dimensions=(4,4,.16);bpy.context.view_layer.objects.active=o;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)\nelif mode=="viewport_hidden":\n bpy.data.objects["plate_mesh"].hide_viewport=True\nelif mode=="object_render_hidden":\n bpy.data.objects["plate_mesh"].hide_render=True\nelif mode=="single_excluded":\n o=bpy.data.objects["plate_mesh"];c=bpy.data.collections.new("OnlyExcluded");bpy.context.scene.collection.children.link(c);c.objects.link(o)\n for old in list(o.users_collection):\n  if old!=c:old.objects.unlink(o)\n def visit(n):\n  if n.collection==c:n.exclude=True\n  for child in n.children:visit(child)\n visit(bpy.context.view_layer.layer_collection)\nelif mode=="alternate_included":\n o=bpy.data.objects["plate_mesh"];c=bpy.data.collections.new("ExcludedAlias");bpy.context.scene.collection.children.link(c);c.objects.link(o)\n def visit(n):\n  if n.collection==c:n.exclude=True\n  for child in n.children:visit(child)\n visit(bpy.context.view_layer.layer_collection)\nbpy.ops.wm.save_as_mainfile(filepath=target)\n''')
  for name,mode,expected,code in [('valid_scene',None,'UNVERIFIED','ENDPOINTS'),('world_endpoint_mismatch','endpoint','FAIL','ENDPOINTS'),('horizontal_outside','horizontal','FAIL','HORIZONTAL'),('vertical_outside','vertical','FAIL','VERTICAL'),('support_gap','support','UNVERIFIED','SUPPORT'),('face_interior_contact','face_interior_contact','UNVERIFIED','SUPPORT')]:
   if name=='support_gap':mode='support'
   # Render inclusion is deliberately UNVERIFIED even if hide_render=False.
   check_expected='PASS' if name=='valid_scene' else expected
   path=scene if mode is None else tmp/(name+'.blend');rep=tmp/(name+'.json')
   if mode is not None:
    proc=subprocess.run([args.blender,'--background',str(scene),'--python',str(script),'--',mode,str(path)],capture_output=True,text=True)
    if proc.returncode or not path.exists():rows.append({'name':name,'pass':False,'mutation_exit':proc.returncode});continue
   proc=subprocess.run([args.blender,'--background',str(path),'--python',str(audit),'--',str(ROOT/'examples/valid_record.json'),'--report',str(rep)],capture_output=True,text=True)
   data=json.loads(rep.read_text()) if rep.exists() else {'status':'NO_REPORT','checks':[]}
   checks=[x for x in data['checks'] if x['code']==code and (name!='horizontal_outside' and name!='vertical_outside' or x['subject']=='plate')]
   depth=[x for x in data['checks'] if x['code']=='CLIP_DEPTH' and x['subject']=='plate']
   ok=(proc.returncode==({'PASS':0,'FAIL':2,'UNVERIFIED':3}[expected]) and any(x['status']==check_expected for x in checks))
   if name not in ('support_gap','face_interior_contact'):ok=ok and data['status']==expected
   else:ok=any(x['status']=='UNVERIFIED' for x in checks) and all(x!='SUPPORT:stack' for x in data.get('failures',[])) and proc.returncode!=0
   if name in ('horizontal_outside','vertical_outside'):ok=ok and bool(depth) and depth[0]['status']=='PASS'
   if name=='face_interior_contact':ok=ok and bool(checks) and checks[0]['detail'].get('sampled_vertex_to_surface_min',0)>base['supports'][0]['tolerance']
   rows.append({'name':name,'expected':expected,'actual':data['status'],'exit':proc.returncode,'target_checks':checks,'clip_depth':depth,'pass':ok})
  for name,mode,want in [('viewport_hidden','viewport_hidden','UNVERIFIED'),('object_render_hidden','object_render_hidden','FAIL'),('single_excluded','single_excluded','FAIL'),('alternate_included','alternate_included','UNVERIFIED')]:
   path=tmp/(name+'.blend');rep=tmp/(name+'_audit.json')
   mutation=subprocess.run([args.blender,'--background',str(scene),'--python',str(script),'--',mode,str(path)],capture_output=True,text=True)
   proc=subprocess.run([args.blender,'--background',str(path),'--python',str(audit),'--',str(ROOT/'examples/valid_record.json'),'--report',str(rep)],capture_output=True,text=True) if path.exists() else mutation
   data=json.loads(rep.read_text()) if rep.exists() else {'status':'NO_REPORT','checks':[]}
   matches=[x for x in data['checks'] if x['code']=='COMPONENT_RENDER' and x['subject']=='plate']
   ok=mutation.returncode==0 and bool(matches) and matches[0]['status']==want
   if name=='viewport_hidden':ok=ok and matches[0]['detail'].get('included_paths_checked',0)>=1 and 'object.hide_render' not in str(matches[0])
   if name=='object_render_hidden':ok=ok and matches[0]['detail'].get('known_exclusion')=='object.hide_render'
   if name=='single_excluded':ok=ok and matches[0]['detail'].get('path_count')==1
   if name=='alternate_included':ok=ok and data['status']!='FAIL' and matches[0]['detail'].get('included_paths_checked',0)>=1
   rows.append({'name':name,'expected_render':want,'actual_render':matches,'audit_status':data['status'],'pass':ok})
  for name,mutation,expected,code,subject in [
    ('port_tolerance_absent',lambda d:d['ports'][0].pop('surface_tolerance'),'UNVERIFIED','PORT_OWNER_SURFACE','a'),
    ('route_tolerance_absent',lambda d:d['connections'][0].pop('tolerance'),'UNVERIFIED','ENDPOINTS','rod'),
    ('route_tolerance_nan',lambda d:d['connections'][0].__setitem__('tolerance',float('nan')),'FAIL','STATIC_RECORD',''),
    ('route_tolerance_bool',lambda d:d['connections'][0].__setitem__('tolerance',True),'FAIL','STATIC_RECORD',''),
    ('required_route_missing',lambda d:(d['connections'][0].__setitem__('object','missing_route'),d['connections'][0].__setitem__('required',False)),'FAIL','ROUTE_OBJECT','rod')]:
   d=copy.deepcopy(base);mutation(d);rec=tmp/(name+'.json');rec.write_text(json.dumps(d));rep=tmp/(name+'_audit.json')
   proc=subprocess.run([args.blender,'--background',str(scene),'--python',str(audit),'--',str(rec),'--report',str(rep)],capture_output=True,text=True)
   data=json.loads(rep.read_text()) if rep.exists() else {'status':'NO_REPORT','checks':[]}
   matches=[x for x in data['checks'] if x['code']==code and x['subject']==subject]
   if code=='STATIC_RECORD':matches=data.get('record_issues',{}).get('errors',[])
   ok=data['status']==expected and proc.returncode=={'PASS':0,'FAIL':2,'UNVERIFIED':3}[expected] and (bool(matches) if code=='STATIC_RECORD' else any(x['status']==expected for x in matches))
   rows.append({'name':name,'expected':expected,'actual':data['status'],'target_checks':matches,'exit':proc.returncode,'pass':ok})
  d=copy.deepcopy(base);one_component(d);rec=tmp/'one_component.json';rec.write_text(json.dumps(d));rep=tmp/'one_component_audit.json'
  proc=subprocess.run([args.blender,'--background',str(scene),'--python',str(audit),'--',str(rec),'--report',str(rep)],capture_output=True,text=True)
  data=json.loads(rep.read_text()) if rep.exists() else {}
  rows.append({'name':'single_component_no_interfaces_audit','pass':proc.returncode==3 and data.get('status')=='UNVERIFIED' and not data.get('failures') and any('NO_PORTS' in x for x in data.get('unverified',[]))})
  for name,mutation,code in [('audit_bad_task_kind',lambda d:d['task'].__setitem__('kind',[]),'TASK_KIND'),('audit_bad_port_medium',lambda d:d['ports'][0].__setitem__('medium',{}),'PORT_MEDIUM'),('audit_bad_outputs',lambda d:d['task'].__setitem__('outputs',[]),'OUTPUTS_TYPE')]:
   d=copy.deepcopy(base);mutation(d);rec=tmp/(name+'.json');rec.write_text(json.dumps(d));rep=tmp/(name+'_report.json')
   proc=subprocess.run([args.blender,'--background',str(scene),'--python',str(audit),'--',str(rec),'--report',str(rep)],capture_output=True,text=True)
   data=json.loads(rep.read_text()) if rep.exists() else {}
   ok=proc.returncode==2 and data.get('status')=='FAIL' and data.get('checks')==[] and code in [x['code'] for x in data.get('record_issues',{}).get('errors',[])]
   rows.append({'name':name,'expected':'FAIL_STATIC_NO_GEOMETRY','actual':data.get('status'),'exit':proc.returncode,'pass':ok})
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
