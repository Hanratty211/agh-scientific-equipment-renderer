"""Codex independent rerun of saved-scene audit; expected UNVERIFIED exits retained."""
import json,hashlib,subprocess,sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
root=Path(__file__).resolve().parents[1];proj=root.parent
exe='/Applications/Blender.app/Contents/MacOS/Blender'
audit=proj/'skills/agh-scientific-equipment-renderer/scripts/audit_saved_scene.py'
versions={} if '--v03-only' in sys.argv else {14:'v04',15:'v04',18:'v06',19:'v04'}
def one(case):
 id_=int(case.name[:2]);v=versions.get(id_,'v03');scene=case/f'scene_{v}.blend';record=case/f'record_{v}.json';out=root/'codex-review'/f'independent_audit_{id_}_{v}.json'
 args=[exe,'--background',str(scene),'--python',str(audit),'--',str(record),'--report',str(out)]
 r=subprocess.run(args,text=True,capture_output=True,timeout=120);(out.with_suffix('.log')).write_text(r.stdout+r.stderr)
 report=json.loads(out.read_text()) if out.exists() else {'status':'TOOL_ERROR','failures':[r.stderr]};rec=json.loads(record.read_text()) if record.exists() else {}
 return {'case':id_,'version':v,'exit':r.returncode,'status':report['status'],'failures':report.get('failures',[]),'ports':len(rec.get('ports',[])),'connections':len(rec.get('connections',[])),'supports':len(rec.get('supports',[])),'scene_sha256':hashlib.sha256(scene.read_bytes()).hexdigest() if scene.exists() else None,'record_sha256':hashlib.sha256(record.read_bytes()).hexdigest() if record.exists() else None,'report':str(out),'unknown':report.get('unverified',[])}
with ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(one,sorted((root/'cases').glob('[12][0-9]_*'))))
(root/('codex-review/independent_audit_v03_summary.json' if '--v03-only' in sys.argv else 'codex-review/independent_audit_summary.json')).write_text(json.dumps(rows,indent=2))
print(json.dumps([{k:r[k] for k in ('case','version','status','ports','connections','failures')} for r in rows],indent=2))
