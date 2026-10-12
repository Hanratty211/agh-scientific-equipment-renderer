"""Codex review aid: assemble unchanged reference and version PNGs; no visual verdict."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,sys,hashlib
root=Path(__file__).resolve().parents[1]
version=sys.argv[1] if len(sys.argv)>1 else 'v02'
papers=json.loads((root/'targets.json').read_text())['papers']
out=Path(__file__).resolve().parent
canvas=Image.new('RGB',(2000,2250),'#eeeeee');draw=ImageDraw.Draw(canvas);seen=[]
for j,p in enumerate(papers):
 actual_version=('v06' if p['id']==18 else 'v04' if p['id'] in (14,15,19) else 'v03') if version=='latest' else version
 source=root/p['target_file'];render=root/'cases'/f"{p['id']}_{p['slug']}"/f'overview_{actual_version}.png'
 im=Image.open(render).convert('RGB');im.thumbnail((970,410));x=j%2*1000;y=j//2*450
 canvas.paste(im,(x+(1000-im.width)//2,y+30));draw.text((x+12,y+6),f"{p['id']} {p['slug']} {actual_version}",fill='black')
 pair=Image.new('RGB',(1600,900),'#f2f2f2');pd=ImageDraw.Draw(pair)
 for k,path in enumerate([source,render]):
  ii=Image.open(path).convert('RGB');ii.thumbnail((780,840));pair.paste(ii,(k*800+(800-ii.width)//2,40+(840-ii.height)//2));pd.text((k*800+15,8),'REFERENCE' if k==0 else f'AGH {actual_version.upper()}',fill='black')
 pair.save(out/f"pair_{p['id']}_{version}.png")
 seen.append({'id':p['id'],'version':actual_version,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
              'render_sha256':hashlib.sha256(render.read_bytes()).hexdigest(),'source':str(source),'render':str(render),
              'meaning':'Review aid prepared only; actual pixel inspection and verdict recorded separately.'})
canvas.save(out/f'ten_{version}_contact.png')
(out/f'images_{version}_hashes.json').write_text(json.dumps(seen,indent=2))
print('Prepared ten reference/output pairs:',version)
