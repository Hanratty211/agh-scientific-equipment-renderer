#!/usr/bin/env python3
"""Static optional project-record validation. No Blender required; no physical/visual PASS.
Usage: python3 validate_project_record.py record.json --report report.json
Exit 0 only for PASS, 2 for FAIL, 3 for UNKNOWN, 1 for invalid JSON/schema.
"""
import argparse, json
from pathlib import Path

SCHEMA='agh-equipment/0.6'
KINDS={'physical_setup','device','internal_state','repair','hybrid'}
MEDIA={'fluid','electric','optical','mechanical','rf','unknown'}
LINKS={'transport','electric','optical','mechanical','rf','field','logical','temporal','contact'}
PHYSICAL={'transport','electric','optical','mechanical','rf','contact'}

def validate(data):
 errors=[]; unknown=[]; checks=[]; dependent={}
 def fail(code, where):errors.append({'code':code,'where':where})
 def unsure(code, where):unknown.append({'code':code,'where':where})
 def ids(rows, key):
  out={}
  if not isinstance(rows,list):fail('NOT_LIST',key);return out
  for i,item in enumerate(rows):
   if not isinstance(item,dict) or not isinstance(item.get('id'),str) or not item['id']:
    fail('BAD_ID',f'{key}[{i}]');continue
   if item['id'] in out:fail('DUPLICATE_ID',f'{key}.{item["id"]}')
   out[item['id']]=item
  return out
 if not isinstance(data,dict):return {'status':'FAIL','errors':[{'code':'NOT_OBJECT','where':'$'}],'unknown':[],'checks':[],'dependent_records':{}}
 if data.get('schema')!=SCHEMA:fail('SCHEMA','schema')
 task=data.get('task');task=task if isinstance(task,dict) else {}
 if task.get('kind') not in KINDS:fail('TASK_KIND','task.kind')
 if not isinstance(task.get('scope'),str) or not task.get('scope').strip():unsure('SCOPE_UNDECLARED','task.scope')
 if task.get('kind')=='internal_state' and not task.get('operating_state'):unsure('STATE_REQUIRED','task.operating_state')
 outs=task.get('outputs',{});outs=outs if isinstance(outs,dict) else {}
 if not isinstance(outs.get('views'),list) or not outs['views']:unsure('VIEWS_UNDECLARED','task.outputs.views')
 if outs.get('annotations') not in ('none','svg'):unsure('ANNOTATION_MODE_UNDECLARED','task.outputs.annotations')
 if not task.get('operating_state'):unsure('OPERATING_STATE_UNDECLARED','task.operating_state')
 comps=ids(data.get('components',[]),'components');ports=ids(data.get('ports',[]),'ports');links=ids(data.get('connections',[]),'connections');supports=ids(data.get('supports',[]),'supports')
 required_fields=('required_components','required_connections','required_supports')
 if not any(task.get(k) for k in required_fields):unsure('REQUIRED_SCOPE_EMPTY','task')
 for field,table in [('required_components',comps),('required_connections',links),('required_supports',supports)]:
  entries=task.get(field,[])
  if not isinstance(entries,list):fail('REQUIRED_NOT_LIST',f'task.{field}');continue
  for id_ in entries:
   if id_ not in table:fail('REQUIRED_MISSING',f'task.{field}.{id_}')
 for id_,c in comps.items():
  dependent.setdefault(f'component:{id_}',{'supports':[],'ports':[],'connections':[],'labels':[],'object':c.get('object')})
  if not isinstance(c.get('object'),str) or not c['object']:unsure('OBJECT_UNBOUND',f'components.{id_}')
  if c.get('evidence','unknown') not in ('photo','paper','user','schematic','unknown'):fail('EVIDENCE_VALUE',f'components.{id_}')
  if c.get('evidence','unknown')=='unknown':unsure('EVIDENCE_UNKNOWN',f'components.{id_}')
  if c.get('size_basis','unknown') not in ('source','illustrative','unknown'):fail('SIZE_BASIS',f'components.{id_}')
  if c.get('parent') and c['parent'] not in comps:fail('COMPONENT_PARENT_MISSING',f'components.{id_}.parent')
  if c.get('state') and task.get('operating_state') and c['state']!=task['operating_state']:unsure('OTHER_STATE_COMPONENT',f'components.{id_}')
 for id_,p in ports.items():
  owner=p.get('owner');dependent[f'port:{id_}']={'connections':[],'labels':[],'owner':owner}
  if owner not in comps:fail('PORT_OWNER_MISSING',f'ports.{id_}.owner')
  else:dependent[f'component:{owner}']['ports'].append(id_)
  if not p.get('object'):unsure('PORT_OBJECT_UNBOUND',f'ports.{id_}.object')
  if p.get('medium') not in MEDIA:fail('PORT_MEDIUM',f'ports.{id_}.medium')
  if p.get('direction') not in ('in','out','bidirectional','unknown'):fail('PORT_DIRECTION',f'ports.{id_}.direction')
  if p.get('state') not in ('connected','open','unknown'):fail('PORT_STATE',f'ports.{id_}.state')
  if p.get('state')=='unknown' or p.get('medium')=='unknown' or p.get('direction')=='unknown':unsure('PORT_UNKNOWN',f'ports.{id_}')
  if p.get('state')=='open' and not p.get('open_reason'):unsure('OPEN_REASON_UNKNOWN',f'ports.{id_}')
 used={id_:[] for id_ in ports}
 for id_,ln in links.items():
  a,b=ln.get('a'),ln.get('b');k=ln.get('kind');m=ln.get('medium')
  if k not in LINKS:fail('CONNECTION_KIND',f'connections.{id_}.kind')
  if m not in MEDIA:fail('CONNECTION_MEDIUM',f'connections.{id_}.medium')
  for end in (a,b):
   if end not in ports:fail('CONNECTION_ENDPOINT_MISSING',f'connections.{id_}.{end}')
   else:
    used[end].append(id_);dependent[f'port:{end}']['connections'].append(id_)
    owner=ports[end].get('owner')
    if owner in comps:dependent[f'component:{owner}']['connections'].append(id_)
  if a and a==b:fail('SELF_CONNECTION',f'connections.{id_}')
  if a in ports and b in ports and ports[a].get('owner')==ports[b].get('owner') and k in PHYSICAL:unsure('INTRA_COMPONENT_CONNECTION',f'connections.{id_}')
  if k in PHYSICAL:
   if not ln.get('object'):unsure('ROUTE_OBJECT_UNBOUND',f'connections.{id_}.object')
   if k in {'transport','electric','optical','mechanical','rf'} and m not in ('unknown',k if k!='transport' else 'fluid'):
    fail('KIND_MEDIUM_CONTRADICTION',f'connections.{id_}')
   for end in (a,b):
    if end not in ports:continue
    pm=ports[end].get('medium')
    if pm!='unknown' and m!='unknown' and pm!=m:fail('MEDIUM_CONTRADICTION',f'connections.{id_}.{end}')
    elif pm=='unknown' or m=='unknown':unsure('MEDIUM_UNKNOWN',f'connections.{id_}.{end}')
  if k in ('logical','field','temporal') and ln.get('object'):unsure('NONPHYSICAL_ROUTE_OBJECT',f'connections.{id_}')
 for id_,p in ports.items():
  if p.get('state')=='connected' and not used[id_]:fail('DECLARED_CONNECTED_UNUSED',f'ports.{id_}')
  if p.get('state')=='open' and used[id_]:fail('OPEN_PORT_USED',f'ports.{id_}')
 for id_,s in supports.items():
  child,parent=s.get('child'),s.get('parent')
  if child not in comps or parent not in comps:fail('SUPPORT_COMPONENT_MISSING',f'supports.{id_}')
  if child==parent:fail('SELF_SUPPORT',f'supports.{id_}')
  if not isinstance(s.get('tolerance'),(float,int)) or isinstance(s.get('tolerance'),bool) or s['tolerance']<0:unsure('SUPPORT_TOLERANCE_UNDECLARED',f'supports.{id_}')
  if child in comps:dependent[f'component:{child}']['supports'].append(id_)
  if parent in comps:dependent[f'component:{parent}']['supports'].append(id_)
 labels=ids(data.get('labels',[]),'labels')
 if task.get('outputs',{}).get('annotations')=='none' and labels:fail('LABELS_FORBIDDEN','labels')
 for id_,label in labels.items():
  target=label.get('target')
  if target not in comps and target not in ports:fail('LABEL_TARGET_MISSING',f'labels.{id_}')
  elif target in comps:dependent[f'component:{target}']['labels'].append(id_)
  else:
   dependent[f'port:{target}']['labels'].append(id_)
   owner=ports[target].get('owner')
   if owner in comps:dependent[f'component:{owner}']['labels'].append(id_)
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
