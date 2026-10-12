"""Local-only six-case contact sheet from HASH-VERIFIED reloaded overview PNGs.
No source/publisher media embedded; proof manifest tracks all six input hashes.
"""
import json,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
root=Path(__file__).resolve().parent;manifest=json.loads((root.parent/'physical_feedback_r2_manifest.json').read_text());cols=3;cw,ch=850,625
sheet=Image.new('RGB',(cols*cw,2*ch),(246,248,250));draw=ImageDraw.Draw(sheet)
for i,case in enumerate(manifest['cases']):
 path=Path(case['images'][0]['path']);assert hashlib.sha256(path.read_bytes()).hexdigest()==case['images'][0]['sha256']
 im=Image.open(path).convert('RGB');im.thumbnail((cw-32,ch-85));x=(i%cols)*cw+(cw-im.width)//2;y=(i//cols)*ch+46
 sheet.paste(im,(x,y));draw.text(((i%cols)*cw+14,(i//cols)*ch+14),f"Case {case['case']}   {case['version']} saved-scene reload R2",fill=(20,32,46))
 draw.text(((i%cols)*cw+14,(i//cols)*ch+ch-28),f"overview SHA256 {case['images'][0]['sha256'][:18]}...",fill=(65,79,95))
out=root.parent/'physical_feedback_r2_six_overviews.png';sheet.save(out)
proof={'author':'AGH','sheet':str(out),'sheet_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'layout':'3 columns x 2 rows, whole saved-scene-reloaded previews','entries':[{'case':x['case'],'image':x['images'][0]['path'],'sha256':x['images'][0]['sha256']} for x in manifest['cases']],'pixel_scope':'layout/contact sheet only; no manufacturer CAD or system function acceptance'}
(root.parent/'physical_feedback_r2_six_overviews.json').write_text(json.dumps(proof,indent=2,ensure_ascii=False)+'\n')
print('SHEET',out,proof['sheet_sha256'])
