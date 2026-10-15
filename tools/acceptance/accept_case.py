"""Shared fail-closed Blender acceptance; case-specific coverage is frozen separately."""
import argparse,hashlib,json,subprocess,datetime,os
from pathlib import Path
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def validate(report,scene,expected):
 reasons=[]
 if not isinstance(report,dict):return ['Report must be an object']
 checks=report.get('checks')
 if not isinstance(checks,list) or not checks:return ['Missing/empty coverage']
 if not all(isinstance(c,dict) for c in checks):return ['Malformed checks']
 ids=[c.get('id') for c in checks]
 if len(ids)!=len(expected) or set(str(i) for i in ids)!=set(expected):reasons.append('Coverage ID set/count mismatch')
 if any(c.get('status')!='PASS' for c in checks):reasons.append('Non-PASS checks')
 if report.get('sha256')!=sha(scene):reasons.append('Scene hash mismatch')
 if report.get('scene')!=str(Path(scene).resolve()):reasons.append('Scene path mismatch')
 counts=report.get('counts')
 if not isinstance(counts,dict) or counts.get('FAIL')!=0 or counts.get('PASS')!=len(checks):reasons.append('Count mismatch')
 return reasons

def run(scene,out,contract,blender,timeout):
 scene=Path(scene).resolve();out=Path(out).resolve();contract=Path(contract).resolve()
 c=json.loads(contract.read_text());expected=c['expected_check_ids'];audit=(contract.parent/c['audit_script']).resolve()
 if not expected or len(set(expected))!=len(expected):raise ValueError('Empty/duplicate contract')
 if sha(audit)!=c['audit_sha256']:raise ValueError('Frozen auditor hash mismatch')
 out.mkdir(parents=True,exist_ok=False);started=datetime.datetime.now().astimezone().isoformat()
 try:before=sha(scene)
 except OSError as e:
  status={'status':'FAIL','reasons':['Input scene unavailable: '+str(e)],'exit_code':2,'started_at':started,'finished_at':datetime.datetime.now().astimezone().isoformat(),'scene':str(scene),'scene_sha256_before':None,'scene_sha256_after':None,'audit_started':False,'contract_sha256':sha(contract),'runner_sha256':sha(__file__),'scope':c['scope']}
  (out/'gate.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n');return status
 report=out/'geometry.json';cmd=[blender,'-b',str(scene),'--python-exit-code','1','--python',str(audit),'--',str(report)]
 reason=[]
 with (out/'execution.log').open('w') as log:
  try:code=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,timeout=timeout).returncode
  except subprocess.TimeoutExpired:reason.append('Audit interrupted at wall-time budget');code=124
  except OSError as e:reason.append('Blender startup failed: '+str(e));code=127
 if code:reason.append('Process did not complete successfully')
 try:reason+=validate(json.loads(report.read_text()),scene,expected)
 except (OSError,ValueError,TypeError) as e:reason.append('Missing/malformed report: '+str(e))
 after=sha(scene)
 if before!=after:reason.append('Saved scene changed during read-only audit')
 status={'status':'FAIL' if reason else 'PASS','reasons':reason,'exit_code':code,'started_at':started,'finished_at':datetime.datetime.now().astimezone().isoformat(),'scene':str(scene),'scene_sha256_before':before,'scene_sha256_after':after,'audit_sha256':sha(audit),'contract_sha256':sha(contract),'runner_sha256':sha(__file__),'command':cmd,'coverage_required':len(expected),'scope':c['scope']}
 (out/'gate.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n');return status
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('scene');p.add_argument('out');p.add_argument('--contract',required=True);p.add_argument('--blender',default=os.environ.get('AGH_BLENDER', 'blender'));p.add_argument('--timeout',type=float,default=180);a=p.parse_args()
 try:s=run(a.scene,a.out,a.contract,a.blender,a.timeout)
 except FileExistsError:raise SystemExit('Refusing existing run directory; preserve evidence and choose new path')
 print(json.dumps(s,ensure_ascii=False));raise SystemExit(0 if s['status']=='PASS' else 2)
