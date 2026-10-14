#!/usr/bin/env python3
"""Check a standalone skill folder: local links, files, forbidden media/case records.
Only synthetic fixtures and abstract teaching counterexamples may accompany methods.
"""
from pathlib import Path
import re,sys,yaml

def inspect_release(root):
 root=root.resolve();issues=[];files=[p for p in root.rglob('*') if p.is_file()];links=0
 forbidden={'.pdf','.png','.jpg','.jpeg','.tiff','.svg','.blend','.blend1','.gif','.webp','.zip','.pyc'}
 archived={'validation_2026_10_14.md','evidence_index.md','public_validation_11_20.md','pitfalls_and_fixes.md','v06_results.json','behavior_results.txt'}
 for p in root.rglob('*'):
  rel=str(p.relative_to(root))
  if p.is_dir() and p.name in {'__pycache__','cases','sources','demo-assets','skill-evidence'}:issues.append('forbidden directory '+rel)
  if p.is_file() and (p.suffix.lower() in forbidden or p.name in archived or p.name.endswith(('.log','_LOCAL.md'))):issues.append('forbidden file '+rel)
 for p in files:
  if p.suffix=='.md':
   text=p.read_text(encoding='utf-8')
   for target in re.findall(r'\]\(([^)]+)\)',text):
    if target.startswith(('https://','http://','mailto:','#')):continue
    target=target.split('#',1)[0]
    if not target:continue
    links+=1;dest=(p.parent/target).resolve()
    if not dest.is_relative_to(root) or not dest.exists():issues.append('broken/outside link '+str(p.relative_to(root))+' -> '+target)
 fm=(root/'SKILL.md').read_text(encoding='utf-8')
 match=re.match(r'\A---\n(.*?)\n---\n',fm,re.S)
 if not match:issues.append('frontmatter missing')
 else:
  data=yaml.safe_load(match[1]);
  if not isinstance(data,dict) or data.get('name')!='agh-scientific-equipment-renderer' or not data.get('description'):issues.append('frontmatter invalid')
  if '# 科研装置三维渲染｜v1.1' not in fm:issues.append('entry version mismatch')
 print('PACKAGE',len(files),'files;',links,'local links;',len(issues),'issues')
 for issue in issues:print('FAIL',issue)
 return issues

if __name__=='__main__':sys.exit(1 if inspect_release(Path(__file__).resolve().parents[1]) else 0)
