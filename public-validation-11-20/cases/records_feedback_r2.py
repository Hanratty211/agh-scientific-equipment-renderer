"""Preserve whole source components, ports, and route semantic IDs in 16/19.
Other four cases retain prior records; R2 images are new independent reload renders.
"""
import json
from pathlib import Path
root=Path(__file__).resolve().parent
for n,old,new in ((16,'v04','v05'),(19,'v05','v06')):
 d=next(root.glob(f'{n}_*'));r=json.loads((d/f'record_{old}.json').read_text())
 r['task']['scope']+=' R2 bounded external lead smoothing only; no added internal topology.'
 r['r2_review']='public-validation-11-20/PHYSICAL_FEEDBACK_R2.md'
 r['r2_status']='not externally pixel-approved after R2; final images rendered from reloaded saved scene'
 r['unknown_interfaces']+=['Bezier exterior run preserves original endpoints; tangent and visible near-shell seating do not verify manufacturer terminal pinout, insulated clearance, circuit or physical load.']
 r['task']['outputs']['views']=['overview']
 (d/f'record_{new}.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
 print(n,len(r['components']),len(r['ports']),len(r['connections']))
