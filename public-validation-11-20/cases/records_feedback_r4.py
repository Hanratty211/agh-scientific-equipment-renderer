"""Only endpoint geometry versions; preserve all whole apparatus IDs and topology."""
import json
from pathlib import Path
root=Path(__file__).resolve().parent
for n,old,new in ((12,'v05','v06'),(16,'v06','v07')):
 d=next(root.glob(f'{n}_*'));r=json.loads((d/f'record_{old}.json').read_text())
 r['task']['scope']+=' R4 boundary repair confined to one rear camera DATA mating chain (12) or two already present HV exterior tail insertions (16); no new internal route or equipment.'
 r['r4_source']='User directly viewed and rejected case12 R2 rear PNG for visible air gap and case16 R3 double-entry PNG for exposed colored ends. Those failed images/records remain frozen.'
 r['r4_assumptions']=['Representative geometry, not manufacturer connector CAD','Curved cable endpoint seating is visual/mechanical mesh illustration; electrical/fluid function and HV safety remain unverified','No new hidden route or instrument. New images still pending user pixel feedback.']
 if n==12:
  for c in r['connections']:
   if c['id']=='camera-data':
    c['evidence_note']='External cable begins inside actual +Y camera boot; socket→plug→boot installation audited separately from the exterior cable-to-laptop segment. Connector standard unverified.'
    c['a']='cam-cable-boot' # exterior route does not begin at buried socket; do not inflate tolerance
  r['components'].append({'id':'c13','label':'representative camera rear DATA strain relief','object':'camera representative DATA cable boot','evidence':'schematic','size_basis':'illustrative','state':r['task']['operating_state']})
  r['task']['required_components'].append('c13')
  r['ports'].append({'id':'cam-cable-boot','owner':'c13','object':'camera representative DATA cable boot','medium':'unknown','direction':'out','state':'connected','evidence_note':'Cable emerges from actual 3D buffer; center lies inside material, not on surface; dedicated saved-mesh probe checks full mating chain.'})
  r['ports']=[port if port['id']!='cam-data' else {**port,'state':'open','open_reason':'Socket occupied by plug/boot assembly, not a direct exterior wire endpoint; assembly seating independently checked.'} for port in r['ports']]
  for port in r['ports']:
   if port['id']=='cam-data':port['evidence_note']='Representative DATA socket positioned on actual camera rear panel (+Y); independent checker tests real mesh near face and plug/boot/cable chain.'
 else:
  for c in r['connections']:
   if c['id'] in ('red-lead','green-lead'):c['evidence_note']='Existing exterior lead last section coaxially enters black wall-entry strain relief; endpoint inside actual boot, no wire beyond sidewall.'
  r['r4_unknown']='Insulator dimensions/material identity, sealing, voltage rating and internal needle/collector path unverified.'
 (d/f'record_{new}.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
 print(n,old,'->',new,len(r['components']),len(r['connections']))
