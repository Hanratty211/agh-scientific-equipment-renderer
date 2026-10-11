"""Counts only declared route/owner-surface checks in actual v0.6 saved-scene report.
Does NOT infer full original scope or pixel visibility from PASS geometry.
"""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
for d in sorted((ROOT/'cases').glob('[12][0-9]_*')):
 if not d.is_dir() or not (d/'audit_scene_v03.json').exists():continue
 rec=json.loads((d/'record_v03.json').read_text());a=json.loads((d/'audit_scene_v03.json').read_text());checks=a['checks']
 def rows(code):return [x for x in checks if x['code']==code]
 def tally(items):return {'PASS':sum(x['status']=='PASS' for x in items),'FAIL':sum(x['status']=='FAIL' for x in items),'UNVERIFIED':sum(x['status']=='UNVERIFIED' for x in items)}
 data={'case':d.name,'declared_components':len(rec['components']),
  'declared_ports':len(rec['ports']),'declared_routes':len(rec['connections']),
  'owner_surface_checks':tally(rows('PORT_OWNER_SURFACE')),
  'visible_route_endpoint_checks':tally(rows('ENDPOINTS')),
  'audit_status':a['status'],'audit_failures':a['failures'],
  'limits':['route endpoint proximity does not prove optical law, physical transport or hidden topology',
            'routes omitted from record have NOT been audited','current render inclusion and visual resemblance UNVERIFIED']}
 (d/'route_coverage_v03.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print(d.name,data['declared_routes'],data['visible_route_endpoint_checks'])
