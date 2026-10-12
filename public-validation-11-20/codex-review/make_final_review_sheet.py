"""Codex comparison artifact only; pixel verdict remains in external review record."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
import json,hashlib
root=Path(__file__).resolve().parents[1];meta=json.loads((root/'targets.json').read_text())['papers'];hashes={x['id']:x for x in json.loads((root/'codex-review/images_latest_hashes.json').read_text())}
canvas=Image.new('RGB',(1500,4220),'#f5f6f8');draw=ImageDraw.Draw(canvas)
for j,p in enumerate(meta):
 v=hashes[p['id']]['version'];y=j*380
 draw.text((18,y+9),f"{p['id']} {p['slug']} | SOURCE / AGH {v} | limited external schematic stage",fill='#143047')
 for k,path in enumerate((root/p['target_file'],Path(hashes[p['id']]['render']))):
  im=Image.open(path).convert('RGB');im=ImageOps.contain(im,(718,326));x=k*750+(750-im.width)//2;canvas.paste(im,(x,y+35+(326-im.height)//2))
y=3830;draw.text((18,y),'18 v06 supplementary isolated detail views: actual same scene; not all visible in overview',fill='#143047')
for j,n in enumerate((12,13,14)):
 im=Image.open(root/'cases/18_electrochemical_stack'/f'cell_{n}_detail_v06.png').convert('RGB');im=ImageOps.contain(im,(470,315));canvas.paste(im,(j*500+(500-im.width)//2,y+35));draw.text((j*500+20,y+360),f'Module {n} — hidden unrelated layers only in this supplementary view',fill='#143047')
p=root/'final_reference_vs_latest_review.png';canvas.save(p)
(root/'codex-review/final_review_sheet_manifest.json').write_text(json.dumps({'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':canvas.size,'source_hashes':hashes,'meaning':'comparison sheet; finite external judgments in EXTERNAL_VALIDATION_STATUS.md'},indent=2))
print(p,canvas.size)
