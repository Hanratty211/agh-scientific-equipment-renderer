"""R1 records, copied from frozen prior versions, preserving all source-required scope.
Only remove array→amp because direct reading of Fig5(b) shows no such line; array
power drive remains open UNKNOWN, explicitly recorded, not silently passed.
"""
import json
from pathlib import Path
root=Path(__file__).resolve().parent
for n,old,new in ((12,'v04','v05'),(14,'v05','v06'),(17,'v04','v05')):
 d=next(root.glob(f'{n}_*'));r=json.loads((d/f'record_{old}.json').read_text());ports={x['id']:x for x in r['ports']};components={x['id']:x for x in r['components']}
 r['task']['scope']+=' R1 correction after user actual pixel review; use v'+new+' saved scene; not user-approved yet.'
 r['r1_feedback']='public-validation-11-20/PHYSICAL_FEEDBACK_R1.md'
 r['r1_status']='not visually approved; mesh/interface audit is limited geometry only'
 r['task']['outputs']['views']=['overview']
 if n==12:
  for k in ('upper','lower'):
   # Source component ID remains the physical syringe pump housing. Port owner
   # is its actual metal nozzle, not a far-away barrel or floating QA marker.
   components['c1' if k=='upper' else 'c2']['object']=k+' syringe pump'
   ports[k+'-pump']['object']=k+' pump open outlet seat'
   new_id='c11' if k=='upper' else 'c12'
   r['components'].append({'id':new_id,'label':k+' pump nozzle owner','object':k+' pump coax metal nozzle','evidence':'schematic','size_basis':'illustrative','state':r['task']['operating_state']})
   r['task']['required_components'].append(new_id)
   ports[k+'-pump']['owner']=new_id
  ports['laptop-data']['object']='laptop DATA data socket'
  r['unknown_interfaces']+=['Data port bore is a representative Blender boolean cut in the real laptop base, not a manufacturer-identified receptacle.']
  r['physical_chain_required']={'upper':'upper syringe pump mounted syringe barrel → upper pump barrel-end collar → upper pump coax metal nozzle → upper pump open outlet seat → upper pump to capillary','lower':'lower syringe pump mounted syringe barrel → lower pump barrel-end collar → lower pump coax metal nozzle → lower pump open outlet seat → lower pump to capillary'}
 if n==14:
  assert 'array-to-amp' in r['task']['required_connections']
  r['task']['required_connections'].remove('array-to-amp')
  r['connections']=[x for x in r['connections'] if x['id']!='array-to-amp']
  ports['array']['state']='open';ports['array']['open_reason']='Fig.5(b) does not draw array to measurement amplifier; array drive type and interface unknown; former route rejected under source check.'
  ports.pop('amp-array');r['ports']=[x for x in r['ports'] if x['id']!='amp-array']
  ports['computer']['object']='laptop DATA data socket'
  r['r1_source_decision']={'Fig5b':'Source inspected locally in Preview: microphone cable→amp (4)→oscilloscope (5); camera (2)→computer (6). No visible array→amp route.','array_to_amp':'REJECTED, not evidence of electric drive; prior array-to-amp kept in v05 history','amp_to_scope':'diagram source visible; BNC signal-input mesh representative because scope unnamed'}
  r['unknown_interfaces']+=['Array-drive circuit and even array cable terminal not shown. No invented feed to measurement amp.']
 if n==17:
  components['c7']['object']='right pump coax metal nozzle'
  ports['pump-pneumatic']['object']='right pump open outlet seat'
  r['physical_chain_required']={'right_pump':'right syringe pump mounted syringe barrel → right pump barrel-end collar → right pump coax metal nozzle → right pump open outlet seat → sample to pump visible pneumatic segment'}
 r['r1_unverified']=['Actual source pixel similarity, commercial port model, full cable occlusion, electrical/flow operation not certified by record']
 (d/f'record_{new}.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 print(n,new,len(r['ports']),len(r['connections']))
