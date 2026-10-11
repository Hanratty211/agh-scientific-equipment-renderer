#!/usr/bin/env python3
"""Static optional project-record validation. No Blender required; no physical/visual PASS.
Usage: python3 validate_project_record.py record.json --report report.json
Exit 0 only for PASS, 2 for FAIL, 3 for UNKNOWN, 1 for invalid JSON/schema.
"""
import argparse, json, math
from pathlib import Path

SCHEMA='agh-equipment/0.6'
KINDS={'physical_setup','device','internal_state','repair','hybrid'}
MEDIA={'fluid','electric','optical','mechanical','rf','unknown'}
LINKS={'transport','electric','optical','mechanical','rf','field','logical','temporal','contact'}
PHYSICAL={'transport','electric','optical','mechanical','rf','contact'}
KIND_MEDIA={'transport':'fluid','electric':'electric','optical':'optical','mechanical':'mechanical','rf':'rf'}
def identifier(value):return isinstance(value,str) and bool(value.strip())
def finite_nonnegative(value):return isinstance(value,(float,int)) and not isinstance(value,bool) and math.isfinite(value) and value>=0

def validate(data):
 errors=[]; unknown=[]; checks=[]; dependent={}
 def fail(code, where):errors.append({'code':code,'where':where})
 def unsure(code, where):unknown.append({'code':code,'where':where})
 def ids(rows, key):
  out={}
  if not isinstance(rows,list):fail('NOT_LIST',key);return out
  for i,item in enumerate(rows):
   if not isinstance(item,dict) or not identifier(item.get('id')):
    fail('BAD_ID',f'{key}[{i}]');continue
   if item['id'] in out:fail('DUPLICATE_ID',f'{key}.{item["id"]}')
   out[item['id']]=item
  return out
 if not isinstance(data,dict):return {'status':'FAIL','errors':[{'code':'NOT_OBJECT','where':'$'}],'unknown':[],'checks':[],'dependent_records':{}}
 if data.get('schema')!=SCHEMA:fail('SCHEMA','schema')
 if 'task' in data and not isinstance(data['task'],dict):fail('TASK_TYPE','task')
 task=data.get('task');task=task if isinstance(task,dict) else {}
 if not identifier(task.get('kind')) or task['kind'] not in KINDS:fail('TASK_KIND','task.kind')
 if not isinstance(task.get('scope'),str) or not task.get('scope').strip():unsure('SCOPE_UNDECLARED','task.scope')
 if task.get('kind')=='internal_state' and not task.get('operating_state'):unsure('STATE_REQUIRED','task.operating_state')
 outs=task.get('outputs',{});outs=outs if isinstance(outs,dict) else {}
 if 'outputs' in task and not isinstance(task['outputs'],dict):fail('OUTPUTS_TYPE','task.outputs')
 if 'views' in outs and not isinstance(outs['views'],list):fail('VIEWS_TYPE','task.outputs.views')
 if not isinstance(outs.get('views'),list) or not outs['views']:unsure('VIEWS_UNDECLARED','task.outputs.views')
 if 'annotations' in outs and (not identifier(outs['annotations']) or outs['annotations'] not in ('none','svg')):fail('ANNOTATION_MODE_INVALID','task.outputs.annotations')
 elif 'annotations' not in outs:unsure('ANNOTATION_MODE_UNDECLARED','task.outputs.annotations')
 if 'operating_state' in task and not identifier(task['operating_state']):fail('OPERATING_STATE_TYPE','task.operating_state')
 if not task.get('operating_state'):unsure('OPERATING_STATE_UNDECLARED','task.operating_state')
 comps=ids(data.get('components',[]),'components');ports=ids(data.get('ports',[]),'ports');links=ids(data.get('connections',[]),'connections');supports=ids(data.get('supports',[]),'supports')
 required_fields=('required_components','required_connections','required_supports')
 if not any(isinstance(task.get(k),list) and task[k] for k in required_fields):unsure('REQUIRED_SCOPE_EMPTY','task')
 for field,table in [('required_components',comps),('required_connections',links),('required_supports',supports)]:
  entries=task.get(field,[])
  if not isinstance(entries,list):fail('REQUIRED_NOT_LIST',f'task.{field}');continue
  for i,id_ in enumerate(entries):
   if not identifier(id_):fail('REQUIRED_BAD_ID',f'task.{field}[{i}]')
   elif id_ not in table:fail('REQUIRED_MISSING',f'task.{field}.{id_}')
 for id_,c in comps.items():
  dependent.setdefault(f'component:{id_}',{'supports':[],'ports':[],'connections':[],'labels':[],'object':c.get('object')})
  if not identifier(c.get('object')):unsure('OBJECT_UNBOUND',f'components.{id_}')
  if not identifier(c.get('evidence','unknown')) or c.get('evidence','unknown') not in ('photo','paper','user','schematic','unknown'):fail('EVIDENCE_VALUE',f'components.{id_}')
  if c.get('evidence','unknown')=='unknown':unsure('EVIDENCE_UNKNOWN',f'components.{id_}')
  if not identifier(c.get('size_basis','unknown')) or c.get('size_basis','unknown') not in ('source','illustrative','unknown'):fail('SIZE_BASIS',f'components.{id_}')
  elif c.get('size_basis','unknown')=='unknown':unsure('SIZE_BASIS_UNKNOWN',f'components.{id_}')
  if c.get('parent') is not None:
   if not identifier(c['parent']):fail('COMPONENT_PARENT_BAD_ID',f'components.{id_}.parent')
   elif c['parent'] not in comps:fail('COMPONENT_PARENT_MISSING',f'components.{id_}.parent')
  if c.get('state') and task.get('operating_state') and c['state']!=task['operating_state']:unsure('OTHER_STATE_COMPONENT',f'components.{id_}')
 for id_,p in ports.items():
  owner=p.get('owner');dependent[f'port:{id_}']={'connections':[],'labels':[],'owner':owner}
  if not identifier(owner):fail('PORT_OWNER_BAD_ID',f'ports.{id_}.owner')
  elif owner not in comps:fail('PORT_OWNER_MISSING',f'ports.{id_}.owner')
  else:dependent[f'component:{owner}']['ports'].append(id_)
  if not identifier(p.get('object')):unsure('PORT_OBJECT_UNBOUND',f'ports.{id_}.object')
  if not identifier(p.get('medium')) or p['medium'] not in MEDIA:fail('PORT_MEDIUM',f'ports.{id_}.medium')
  if not identifier(p.get('direction')) or p['direction'] not in ('in','out','bidirectional','unknown'):fail('PORT_DIRECTION',f'ports.{id_}.direction')
  if not identifier(p.get('state')) or p['state'] not in ('connected','open','unknown'):fail('PORT_STATE',f'ports.{id_}.state')
  if p.get('state')=='unknown' or p.get('medium')=='unknown' or p.get('direction')=='unknown':unsure('PORT_UNKNOWN',f'ports.{id_}')
  if p.get('state')=='open' and not p.get('open_reason'):unsure('OPEN_REASON_UNKNOWN',f'ports.{id_}')
  if 'surface_tolerance' in p and not finite_nonnegative(p['surface_tolerance']):fail('PORT_TOLERANCE_INVALID',f'ports.{id_}')
 used={id_:[] for id_ in ports}
 for id_,ln in links.items():
  a,b=ln.get('a'),ln.get('b');k=ln.get('kind');m=ln.get('medium')
  if not identifier(k) or k not in LINKS:fail('CONNECTION_KIND',f'connections.{id_}.kind')
  if not identifier(m) or m not in MEDIA:fail('CONNECTION_MEDIUM',f'connections.{id_}.medium')
  for side,end in (('a',a),('b',b)):
   if not identifier(end):fail('CONNECTION_ENDPOINT_BAD_ID',f'connections.{id_}.{side}')
   elif end not in ports:fail('CONNECTION_ENDPOINT_MISSING',f'connections.{id_}.{side}.{end}')
   else:
    used[end].append(id_);dependent[f'port:{end}']['connections'].append(id_)
    owner=ports[end].get('owner')
    if identifier(owner) and owner in comps:dependent[f'component:{owner}']['connections'].append(id_)
  if identifier(a) and a==b:fail('SELF_CONNECTION',f'connections.{id_}')
  if identifier(a) and identifier(b) and a in ports and b in ports and ports[a].get('owner')==ports[b].get('owner') and identifier(k) and k in PHYSICAL:unsure('INTRA_COMPONENT_CONNECTION',f'connections.{id_}')
  if identifier(k) and k in PHYSICAL:
   if not identifier(ln.get('object')):unsure('ROUTE_OBJECT_UNBOUND',f'connections.{id_}.object')
   if k in KIND_MEDIA and m not in ('unknown',KIND_MEDIA[k]):fail('KIND_MEDIUM_CONTRADICTION',f'connections.{id_}')
   if k=='contact' and m!='unknown':unsure('CONTACT_MEDIUM_NOT_INFERRED',f'connections.{id_}')
   for end in (a,b):
    if not identifier(end) or end not in ports:continue
    pm=ports[end].get('medium')
    if pm!='unknown' and m!='unknown' and pm!=m:fail('MEDIUM_CONTRADICTION',f'connections.{id_}.{end}')
    elif pm=='unknown' or m=='unknown':unsure('MEDIUM_UNKNOWN',f'connections.{id_}.{end}')
  if identifier(k) and k in ('logical','field','temporal'):
   if m!='unknown':unsure('NONPHYSICAL_MEDIUM_NOT_VALIDATED',f'connections.{id_}')
   if ln.get('object'):unsure('NONPHYSICAL_ROUTE_OBJECT',f'connections.{id_}')
  if 'tolerance' in ln and not finite_nonnegative(ln['tolerance']):fail('CONNECTION_TOLERANCE_INVALID',f'connections.{id_}')
 for id_,p in ports.items():
  if p.get('state')=='connected' and not used[id_]:fail('DECLARED_CONNECTED_UNUSED',f'ports.{id_}')
  if p.get('state')=='open' and used[id_]:fail('OPEN_PORT_USED',f'ports.{id_}')
 for id_,s in supports.items():
  child,parent=s.get('child'),s.get('parent')
  if not identifier(child) or not identifier(parent):fail('SUPPORT_REFERENCE_BAD_ID',f'supports.{id_}')
  elif child not in comps or parent not in comps:fail('SUPPORT_COMPONENT_MISSING',f'supports.{id_}')
  if identifier(child) and child==parent:fail('SELF_SUPPORT',f'supports.{id_}')
  if 'tolerance' not in s:unsure('SUPPORT_TOLERANCE_UNDECLARED',f'supports.{id_}')
  elif not finite_nonnegative(s['tolerance']):fail('SUPPORT_TOLERANCE_INVALID',f'supports.{id_}')
  if identifier(child) and child in comps:dependent[f'component:{child}']['supports'].append(id_)
  if identifier(parent) and parent in comps:dependent[f'component:{parent}']['supports'].append(id_)
 labels=ids(data.get('labels',[]),'labels')
 if outs.get('annotations')=='none' and labels:fail('LABELS_FORBIDDEN','labels')
 for id_,label in labels.items():
  target=label.get('target')
  if not identifier(target):fail('LABEL_TARGET_BAD_ID',f'labels.{id_}')
  elif target not in comps and target not in ports:fail('LABEL_TARGET_MISSING',f'labels.{id_}')
  elif target in comps:dependent[f'component:{target}']['labels'].append(id_)
  else:
   dependent[f'port:{target}']['labels'].append(id_)
   owner=ports[target].get('owner')
   if identifier(owner) and owner in comps:dependent[f'component:{owner}']['labels'].append(id_)
 if task.get('required_connections') and not links:fail('REQUIRED_CONNECTIONS_EMPTY','connections')
 if task.get('required_supports') and not supports:fail('REQUIRED_SUPPORTS_EMPTY','supports')
 if not comps:unsure('NO_COMPONENTS','components')
 if not ports:unsure('NO_PORTS','ports')
 if not links:unsure('NO_CONNECTIONS','connections')
 if not supports:unsure('NO_SUPPORTS','supports')
 checks.append({'name':'record_references','status':'PASS' if not errors and not unknown else 'UNVERIFIED' if not errors else 'FAIL'})
 return {'status':'FAIL' if errors else 'UNKNOWN' if unknown else 'PASS','errors':errors,'unknown':unknown,'checks':checks,'dependent_records':dependent,
         'not_checked':['saved_scene_geometry','visual_legibility','functional_transport','occlusion','physics']}

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('record');ap.add_argument('--report');args=ap.parse_args()
 try:result=validate(json.loads(Path(args.record).read_text(encoding='utf-8')))
 except (OSError,ValueError) as e:result={'status':'FAIL','errors':[{'code':'READ_ERROR','where':str(e)}],'unknown':[],'checks':[],'dependent_records':{}}
 text=json.dumps(result,ensure_ascii=False,indent=2)
 if args.report:Path(args.report).write_text(text+'\n',encoding='utf-8')
 print(text);return {'PASS':0,'FAIL':2,'UNKNOWN':3}[result['status']]
if __name__=='__main__':raise SystemExit(main())
