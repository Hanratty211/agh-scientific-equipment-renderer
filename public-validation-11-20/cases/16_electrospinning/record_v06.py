"""Copy v05 full source scope; only two existing wall boundary owner identities change."""
import json
from pathlib import Path
p=Path(__file__).resolve().parent;r=json.loads((p/'record_v05.json').read_text())
r['task']['scope']+=' R3 two sidewall entry boundaries use actual open bores, representative insulating mounting sleeves, short exterior cable boots. No internal route or engineered safety rating.'
r['task']['outputs']['views']=['overview']
r['r3_limit']={'scope':'the two already declared external wall-entry boundaries only','wall':'true cylindrical cuts in existing Perspex mesh','sleeves':'representative geometry/size/insulation only; sealing and dielectric/HV rating unverified','internal_to_needle_collector':'NOT_MODELED','old_v05':'preserved with both colored tips visibly exposed and prior endpoint audit records'}
for comp in r['components']:
 if comp['id']=='c1':comp['object']='clear Perspex side'
for port in r['ports']:
 if port['id'] in ('chamber-red','chamber-green'):
  port['object']= 'chamber red boundary' if port['id']=='chamber-red' else 'chamber green boundary'
  port['evidence_note']='Actual cable-facing annulus on illustrative insulating sleeve, not a colored proxy on transparent wall. Seating to real bored wall checked separately; HV performance unknown.'
  # Give the physical sleeve its OWN assembly identity, not a distant point on
  # the bored wall. Independent checker examines sleeve-to-wall installation.
  new_id='c14' if port['id']=='chamber-red' else 'c15'
  port['owner']=new_id
  r['components'].append({'id':new_id,'label':('positive' if new_id=='c14' else 'return')+' representative wall entry sleeve','object':('positive HV' if new_id=='c14' else 'return/ground')+' representative insulating mounting sleeve','evidence':'schematic','size_basis':'illustrative','state':r['task']['operating_state']})
  r['task']['required_components'].append(new_id)
  # Annulus centroid lies in its genuine hole: old centroid-based scene audit
  # cannot establish surface contact here. Omit tolerance => UNVERIFIED, then
  # rely on separate sampled real-mesh/boolean/axis checks (never inflate it).
  port.pop('surface_tolerance',None)
for conn in r['connections']:
 if conn['id'] in ('red-lead','green-lead'):
  conn['evidence_note']='Visible external cable enters representative strain relief within actual insulating sleeve; beyond wall intentionally absent. No seal/HV rating claim.'
  conn['tolerance']=.08
r['unknown_interfaces']+=['Both wall bores and insulator sleeves: shape/size/material class only illustration; installation detail, seal, creepage, HV voltage rating and actual connector identity NOT verified.','No hidden path from feedthrough to needle or collector constructed.']
(p/'record_v06.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
