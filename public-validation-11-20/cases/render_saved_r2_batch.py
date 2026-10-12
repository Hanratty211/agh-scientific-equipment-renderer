"""Orchestrate six INDEPENDENT Blender processes, each reopening its own saved scene.
Blender itself never saves the file during rendering. Fail fast; no output overwrite.
"""
import json,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parent
blender='/Applications/Blender.app/Contents/MacOS/Blender'
specs=json.loads((root/'r2_view_specs.json').read_text())
versions={12:'v05',13:'v04',14:'v06',16:'v05',17:'v05',19:'v06'}
for n,v in versions.items():
 d=next(root.glob(f'{n}_*'));suffix=f'{v}_reloaded_r2';scene=d/f'scene_{v}.blend';specpath=d/f'views_{suffix}.json';report=d/f'render_{suffix}.json';log=d/f'render_{suffix}.log'
 assert scene.is_file() and not report.exists() and not (d/f'overview_{suffix}.png').exists(),str(report)
 specpath.write_text(json.dumps(specs[str(n)],ensure_ascii=False,indent=2)+'\n')
 cmd=[blender,'--background','--python-exit-code','1',str(scene),'--python',str(root/'render_saved_r2.py'),'--',str(n),suffix,str(specpath),str(report)]
 with log.open('w') as fp:proc=subprocess.run(cmd,stdout=fp,stderr=subprocess.STDOUT)
 print('R2_RELOAD',n,'exit',proc.returncode,'report',report,flush=True)
 if proc.returncode:print(log.read_text()[-3500:],file=sys.stderr);raise SystemExit(proc.returncode)
